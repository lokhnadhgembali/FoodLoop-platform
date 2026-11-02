"""
views/auth.py  -  FoodLoop Split-Screen Login & Signup
Page state: st.session_state.page == "auth"
"""
import streamlit as st
import database
from utils import get_logo_img

DEMO_ACCOUNTS = {
    "donor":     ("mess@lpu.in",       "demo123"),
    "recipient": ("rha@ngo.org",       "demo123"),
    "admin":     ("admin@foodloop.in", "demo123"),
}

ROLE_OPTIONS = [
    ("donor",     "Donor"),
    ("recipient", "🤝 NGO / Recipient"),
    ("admin",     "🛡️ Admin"),
]

LOGIN_ROLE_OPTIONS = [
    ("donor",     "Donor"),
    ("recipient", "🤝 NGO"),
    ("admin",     "🛡️ Admin"),
]

ROLE_NAMES = {
    "donor":     "Donor (kitchen / mess)",
    "recipient": "NGO / Recipient",
    "admin":     "Admin",
}


# ── Session helpers ─────────────────────────────────────────────────────────
def _set_session(user: dict):
    st.session_state.authenticated = True
    st.session_state.user_id       = str(user.get("_id", ""))
    st.session_state.user_name     = user.get("name", "User")
    st.session_state.user_role     = user.get("role", "donor")
    st.session_state.is_verified   = bool(user.get("is_verified", False))
    st.session_state.reward_points = int(user.get("reward_points", 0) or 0)
    st.session_state.page          = "dashboard"
    _persist_session_token(user)


def _persist_session_token(user: dict):
    """Store a session token in the DB and mirror it into the URL so a
    browser refresh can restore the login (see app.py)."""
    try:
        token = database.start_session(user.get("_id"))
    except Exception:
        return
    st.session_state.session_token = token
    try:
        st.query_params["session"] = token
        st.query_params["view"] = "dashboard"
    except Exception:
        pass


def _login(email: str, password: str, expect_role: str | None = None):
    """Return (status, actual_role): "ok", "invalid", "mismatch" or "error"."""
    try:
        user = database.authenticate(email.strip().lower(), password)
    except Exception as exc:
        st.error(f"Login failed: {exc}")
        return "error", None
    if not user:
        return "invalid", None
    actual_role = user.get("role", "donor")
    if expect_role and actual_role != expect_role:
        return "mismatch", actual_role
    _set_session(user)
    return "ok", actual_role


def _set_mode(mode: str):
    st.session_state.auth_mode = mode
    st.rerun()


# ── Left panel ──────────────────────────────────────────────────────────────
def _render_left():
    logo = get_logo_img(height=24, variant="white", margin_right=0)

    st.markdown(f"""
    <div class="fl-auth-brand-badge">
      <span class="icon">{logo}</span>
      <span class="name">FoodLoop</span>
    </div>
    <div class="fl-auth-headline">Zero Food Waste,<br><span class="accent">Maximum Impact.</span></div>
    <div class="fl-auth-lead">
      A verified redistribution network for campus messes, commercial kitchens and NGOs
      across the Jalandhar–Phagwara corridor.
    </div>
    <div class="fl-glass-pill"><span class="icon">🛡️</span> Verified 4-digit PIN pickup protocol</div>
    <div class="fl-glass-pill"><span class="icon">📊</span> Real-time CO2e &amp; meal impact analytics</div>
    <div class="fl-glass-pill"><span class="icon">⏱️</span> Automated &lt; 2hr urgent expiry flagging</div>
    <div class="fl-glass-pill"><span class="icon">📜</span> Complete audit history of every donation</div>
    <div class="fl-auth-proof">
      Join 150+ campus messes, restaurants &amp; NGOs redistributing surplus on FoodLoop
    </div>
    <div class="fl-live-pill"><span class="dot"></span> Live Hub Active — Jalandhar-Phagwara corridor</div>
    """, unsafe_allow_html=True)


# ── Right panel ─────────────────────────────────────────────────────────────
def _render_login():
    logo = get_logo_img(height=30, variant="blue", margin_right=0)
    st.markdown(f"""
    <div style="margin-bottom:6px;">{logo}</div>
    <h2 class="fl-form-heading">Welcome Back</h2>
    <p class="fl-form-sub">Sign in to your dedicated FoodLoop workspace.</p>
    """, unsafe_allow_html=True)

    st.markdown('<span class="fl-field-label">Sign in as</span>', unsafe_allow_html=True)
    selected_role = st.session_state.get("login_role", "donor")
    with st.container(key="login_role_pills"):
        cols = st.columns(3)
        for col, (value, label) in zip(cols, LOGIN_ROLE_OPTIONS):
            with col:
                if st.button(
                    label,
                    key=f"login_role_{value}",
                    use_container_width=True,
                    type="primary" if selected_role == value else "secondary",
                ):
                    st.session_state.login_role = value
                    st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    email = st.text_input("Email address", key="login_email",
                          placeholder="name@organization.org")
    password = st.text_input("Password", type="password", key="login_pass",
                             placeholder="••••••••")

    if st.button("Log In to Dashboard", key="login_submit",
                 use_container_width=True, type="primary"):
        expected = st.session_state.get("login_role", "donor")
        if not email or not password:
            st.warning("Please enter your email and password.")
        else:
            status, actual = _login(email, password, expected)
            if status == "ok":
                st.rerun()
            elif status == "mismatch":
                label = next((lbl for val, lbl in LOGIN_ROLE_OPTIONS if val == actual), actual)
                st.error(
                    f"This account is registered as **{ROLE_NAMES.get(actual, actual)}**. "
                    f"Select **{label}** above, then log in again."
                )
            else:
                st.error("❌ Invalid email or password. Try one of the demo accounts below.")

    st.markdown('<div class="fl-demo-divider">Or instant demo access</div>',
                unsafe_allow_html=True)

    with st.container(key="demo_row"):
        d1, d2, d3 = st.columns(3)
        with d1:
            if st.button("Demo Donor", key="demo_donor", use_container_width=True):
                if _login(*DEMO_ACCOUNTS["donor"])[0] == "ok":
                    st.rerun()
                st.error("Demo donor account unavailable.")
        with d2:
            if st.button("🤝 Demo NGO", key="demo_ngo", use_container_width=True):
                if _login(*DEMO_ACCOUNTS["recipient"])[0] == "ok":
                    st.rerun()
                st.error("Demo NGO account unavailable.")
        with d3:
            if st.button("🛡️ Demo Admin", key="demo_admin", use_container_width=True):
                if _login(*DEMO_ACCOUNTS["admin"])[0] == "ok":
                    st.rerun()
                st.error("Demo admin account unavailable.")

    st.markdown('<div class="fl-link-row">New to FoodLoop?</div>', unsafe_allow_html=True)
    if st.button("Create an account instead", key="to_signup",
                 use_container_width=True):
        _set_mode("signup")


def _render_signup():
    logo = get_logo_img(height=30, variant="blue", margin_right=0)
    st.markdown(f"""
    <div style="margin-bottom:6px;">{logo}</div>
    <h2 class="fl-form-heading">Create Account</h2>
    <p class="fl-form-sub">Start rescuing surplus food or claiming meals for your community.</p>
    """, unsafe_allow_html=True)

    st.markdown('<span class="fl-field-label">Account Type</span>', unsafe_allow_html=True)
    selected_role = st.session_state.get("signup_role", "donor")
    with st.container(key="role_pills"):
        cols = st.columns(3)
        for col, (value, label) in zip(cols, ROLE_OPTIONS):
            with col:
                if st.button(
                    label,
                    key=f"role_{value}",
                    use_container_width=True,
                    type="primary" if selected_role == value else "secondary",
                ):
                    st.session_state.signup_role = value
                    st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    org_name = st.text_input("Organization / Username", key="reg_name",
                             placeholder="LPU Central Mess or Robin Hood Army")
    email = st.text_input("Email address", key="reg_email",
                          placeholder="name@organization.org")
    password = st.text_input("Password", type="password", key="reg_pass",
                             placeholder="Minimum 6 characters")
    phone = st.text_input("Phone & Campus / City Location", key="reg_phone",
                          placeholder="98765 43210 · LPU Campus, Phagwara")

    if st.button("Create Account", key="register_submit",
                 use_container_width=True, type="primary"):
        if not all([org_name.strip(), email.strip(), password, phone.strip()]):
            st.warning("Please fill in all fields to create your account.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")
        elif "@" not in email or "." not in email:
            st.error("Please enter a valid email address.")
        else:
            phone_part, _, location_part = phone.partition("·")
            try:
                user = database.create_user(
                    name=org_name.strip(),
                    email=email.strip().lower(),
                    password=password,
                    phone=phone_part.strip(),
                    address=(location_part or phone_part).strip(),
                    role=st.session_state.get("signup_role", "donor"),
                )
            except Exception as exc:
                st.error(f"Could not create account: {exc}")
                return
            if not user:
                st.error("❌ That email is already registered. Try logging in instead.")
            else:
                _set_session(user)
                st.rerun()

    st.markdown("""
    <div class="fl-link-row">
      Your account starts as <b>pending verification</b> — an admin reviews new organizations.
    </div>
    """, unsafe_allow_html=True)
    if st.button("Already have an account? Log in instead", key="to_login",
                 use_container_width=True):
        _set_mode("login")


# ── Render ──────────────────────────────────────────────────────────────────
def render():
    mode = st.session_state.get("auth_mode", "login")

    with st.container(key="auth_page"):
        left_col, right_col = st.columns([1.05, 1])

        with left_col:
            with st.container(key="auth_left"):
                if st.button("← Back to Home", key="auth_back"):
                    st.session_state.page = "landing"
                    st.rerun()
                _render_left()

        with right_col:
            with st.container(key="auth_right"):
                if mode == "signup":
                    _render_signup()
                else:
                    _render_login()
