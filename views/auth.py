"""
views/auth.py  –  FoodLoop Split-Screen Authentication
Handles login, registration, and demo logins.
"""
import streamlit as st
import database
from utils import get_logo_img

DEMO_ACCOUNTS = [
    ("🏫 Demo Donor – LPU Mess",   "mess@lpu.in",       "demo123", "donor"),
    ("🤝 Demo NGO – Robin Hood",   "rha@ngo.org",        "demo123", "ngo"),
    ("⚙️ Demo Admin – FoodLoop",   "admin@foodloop.in",  "demo123", "admin"),
]

def _set_session(user: dict):
    st.session_state.authenticated = True
    st.session_state.user_id       = str(user.get("_id", ""))
    st.session_state.user_name     = user.get("name", "User")
    st.session_state.user_role     = user.get("role", "donor")
    st.session_state.is_verified   = user.get("is_verified", True)
    st.session_state.page          = "dashboard"

def _demo_login(email: str, password: str):
    user = database.authenticate(email, password)
    if user:
        _set_session(user)
        st.rerun()
    else:
        st.error("Demo account not found. Make sure the DB is seeded.")

def render():
    logo_white = get_logo_img(height=52, variant="white", margin_right="0")
    logo_blue  = get_logo_img(height=40, variant="blue",  margin_right="0")
    mode = st.session_state.get("auth_mode", "login")

    left_col, right_col = st.columns([1.05, 1])

    # ── LEFT PANEL (dark navy) ───────────────────────────────────────────────
    with left_col:
        st.markdown(f"""
        <div class="fl-auth-left">
          <div class="fl-auth-back-btn-wrap" style="margin-bottom:32px;">
          </div>
          <div class="fl-auth-brand">
            {logo_white}
            <div style="margin-top:16px;">
              <div style="font-size:1.7rem;font-weight:900;color:white;line-height:1.1;">
                Zero Food Waste,<br><span style="color:#60A5FA;">Maximum Impact.</span>
              </div>
              <div style="font-size:0.9rem;color:#94A3B8;margin-top:12px;line-height:1.6;">
                Join 200+ kitchens and 80+ NGOs already reducing food waste across Punjab.
              </div>
            </div>
          </div>
          <div style="margin-top:40px;display:flex;flex-direction:column;gap:12px;">
            {"".join(f'<div class="fl-auth-pill">{pill}</div>' for pill in [
                "🔐 4-Digit PIN-Verified Handovers",
                "📡 Real-Time Expiry Tracking",
                "🌱 SDG 2 & SDG 12 Impact Ledger",
                "✅ Verified Donors & NGO Network",
            ])}
          </div>
          <div class="fl-auth-social-proof" style="margin-top:48px;">
            <div style="font-size:1.3rem;font-weight:900;color:white;">1,200+</div>
            <div style="font-size:0.75rem;color:#94A3B8;font-weight:600;">Meals Redistributed This Month</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("← Back to Home", key="auth_back"):
            st.session_state.page = "landing"
            st.rerun()

    # ── RIGHT PANEL (white form) ─────────────────────────────────────────────
    with right_col:
        st.markdown('<div class="fl-auth-right">', unsafe_allow_html=True)

        # Toggle tabs
        t1, t2 = st.tabs(["🔑 Log In", "🚀 Sign Up"])

        # ─── LOGIN TAB ──────────────────────────────────────────────────────
        with t1:
            st.markdown(f"""
            <div style="margin-bottom:8px;">
              {logo_blue}
              <h2 style="font-size:1.5rem;font-weight:800;color:#0F172A;margin-top:12px;">Welcome Back</h2>
              <p style="color:#64748B;font-size:0.88rem;">Sign in to your FoodLoop account</p>
            </div>""", unsafe_allow_html=True)

            email_l    = st.text_input("Email", key="login_email", placeholder="you@example.com")
            password_l = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")

            if st.button("Sign In →", key="login_submit", use_container_width=True, type="primary"):
                if not email_l or not password_l:
                    st.warning("Please enter your email and password.")
                else:
                    user = database.authenticate(email_l.strip(), password_l)
                    if user:
                        _set_session(user)
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password. Try a demo account below.")

            st.markdown("---")
            st.markdown("**⚡ 1-Click Demo Logins**")
            for label, email, pw, role in DEMO_ACCOUNTS:
                if st.button(label, key=f"demo_{role}", use_container_width=True):
                    _demo_login(email, pw)

        # ─── SIGNUP TAB ────────────────────────────────────────────────────
        with t2:
            st.markdown(f"""
            <div style="margin-bottom:8px;">
              {logo_blue}
              <h2 style="font-size:1.5rem;font-weight:800;color:#0F172A;margin-top:12px;">Create Account</h2>
              <p style="color:#64748B;font-size:0.88rem;">Join FoodLoop — it's free for NGOs and donors</p>
            </div>""", unsafe_allow_html=True)

            # Role selector
            st.markdown("**Select your role:**")
            r1, r2 = st.columns(2)
            role_options = [("🍲 Donor", "donor"), ("🤝 NGO / Recipient", "ngo")]
            for col, (rlabel, rval) in zip([r1, r2], role_options):
                current = st.session_state.get("signup_role", "donor")
                btn_type = "primary" if current == rval else "secondary"
                if col.button(rlabel, key=f"role_{rval}", use_container_width=True, type=btn_type):
                    st.session_state.signup_role = rval
                    st.rerun()

            selected_role = st.session_state.get("signup_role", "donor")
            name_label = "Organization / Kitchen Name" if selected_role == "donor" else "NGO / Organization Name"

            org_name  = st.text_input(name_label, key="reg_name", placeholder="e.g. LPU Central Mess")
            email_r   = st.text_input("Email", key="reg_email", placeholder="contact@org.com")
            password_r = st.text_input("Password", type="password", key="reg_pass", placeholder="Min. 6 characters")
            phone     = st.text_input("Phone Number", key="reg_phone", placeholder="+91 98765 43210")
            address   = st.text_input("City / Campus", key="reg_addr", placeholder="Jalandhar, Punjab")

            if st.button("Create Account →", key="register_submit", use_container_width=True, type="primary"):
                if not all([org_name, email_r, password_r, phone]):
                    st.warning("Please fill in all required fields.")
                elif len(password_r) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    db_role = "recipient" if selected_role == "ngo" else "donor"
                    user = database.create_user(
                        name=org_name.strip(),
                        email=email_r.strip().lower(),
                        password=password_r,
                        phone=phone.strip(),
                        address=address.strip(),
                        role=db_role,
                    )
                    if user:
                        st.success(f"✅ Account created! Welcome, {org_name}!")
                        _set_session(user)
                        st.rerun()
                    else:
                        st.error("❌ Email already registered. Please log in.")

        st.markdown('</div>', unsafe_allow_html=True)
