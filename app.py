"""
app.py  -  FoodLoop  ·  Main Streamlit Entry Point
Page states:  landing | auth | dashboard | analytics
"""
import streamlit as st

# ── Page config (must be the first Streamlit call) ──────────────────────────
st.set_page_config(
    page_title="FoodLoop – Rescue Surplus Food",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global stylesheet ───────────────────────────────────────────────────────
from styles import get_css
st.markdown(get_css(), unsafe_allow_html=True)

# ── Database ────────────────────────────────────────────────────────────────
import database
try:
    database.initialize()
except Exception as _e:      # never block the UI on a DB hiccup
    st.warning(f"⚠️ Database notice: {_e}")


# ── Session restore (survives a browser refresh) ────────────────────────────
def _restore_session_from_query():
    """Re-authenticate from ?session=<token> when session_state is fresh."""
    if st.session_state.get("authenticated"):
        return
    try:
        token = st.query_params.get("session")
    except Exception:
        token = None
    if not token:
        return
    try:
        user = database.get_user_by_session_token(token)
    except Exception:
        user = None
    if not user:
        # stale / invalid token → clean URL and fall back to the landing page
        try:
            st.query_params.clear()
        except Exception:
            pass
        return
    st.session_state.authenticated  = True
    st.session_state.user_id        = str(user.get("_id", ""))
    st.session_state.user_name      = user.get("name", "User")
    st.session_state.user_role      = user.get("role", "donor")
    st.session_state.is_verified    = bool(user.get("is_verified", False))
    st.session_state.reward_points  = int(user.get("reward_points", 0) or 0)
    st.session_state.session_token  = token
    try:
        view = st.query_params.get("view", "dashboard")
    except Exception:
        view = "dashboard"
    st.session_state.page = view if view in ("dashboard", "analytics") else "dashboard"
    st.session_state.auth_mode = "login"


_restore_session_from_query()

# ── Session defaults ────────────────────────────────────────────────────────
_DEFAULTS = {
    "page":         "landing",
    "auth_mode":    "login",
    "signup_role":  "donor",
    "authenticated": False,
    "user_id":      None,
    "user_name":    None,
    "user_role":    None,
    "is_verified":  False,
    "reward_points": 0,
    "session_token": None,
}
for _k, _v in _DEFAULTS.items():
    st.session_state.setdefault(_k, _v)

from views import landing, auth, donor, recipient, admin, analytics
from utils import get_logo_img

ROLE_META = {
    "donor":     ("Donor",  "fl-role-donor"),
    "recipient": ("NGO",    "fl-role-recipient"),
    "ngo":       ("NGO",    "fl-role-recipient"),
    "admin":     ("Admin",  "fl-role-admin"),
}


def _refresh_session_user():
    """Keep verification + reward points fresh from the database."""
    uid = st.session_state.get("user_id")
    if not uid:
        return
    try:
        user = database.get_user_by_id(uid)
    except Exception:
        user = None
    if user:
        st.session_state.user_name = user.get("name", st.session_state.user_name)
        st.session_state.is_verified = bool(user.get("is_verified", False))
        st.session_state.reward_points = int(user.get("reward_points", 0) or 0)


def _logout():
    """Explicit logout: invalidate the DB token, clear URL params, reset state."""
    token = st.session_state.get("session_token")
    if not token:
        try:
            token = st.query_params.get("session")
        except Exception:
            token = None
    try:
        database.clear_session_token(token)
    except Exception:
        pass
    try:
        st.query_params.clear()
    except Exception:
        pass
    for k, v in _DEFAULTS.items():
        st.session_state[k] = v
    st.session_state.page = "landing"
    st.rerun()


# ── Dashboard navbar ────────────────────────────────────────────────────────
def _render_dash_nav():
    _refresh_session_user()
    role       = st.session_state.get("user_role", "donor")
    role_label, role_class = ROLE_META.get(role, (str(role).capitalize(), "fl-role-donor"))
    user_name  = st.session_state.get("user_name") or "User"
    verified   = st.session_state.get("is_verified", False)
    logo       = get_logo_img(height=26, variant="white", margin_right=0)
    page       = st.session_state.get("page", "dashboard")

    verified_html = (
        '<span class="fl-verified">✅ Verified</span>' if verified
        else '<span class="fl-verified" style="background:#FEF3C7;color:#92400E;">⏳ Pending</span>'
    )

    with st.container(key="dash_nav"):
        c_brand, c_analytics, c_dash, c_logout = st.columns([5.4, 1.35, 1.15, 0.95])
        with c_brand:
            st.markdown(f"""
            <div class="fl-dash-user">
              <span style="width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#014BAA,#0264E0);
                    display:inline-flex;align-items:center;justify-content:center;overflow:hidden;
                    box-shadow:0 4px 12px rgba(1,75,170,.3);">{logo}</span>
              <span class="fl-nav-name" style="font-size:1.02rem;letter-spacing:-.3px;">FoodLoop</span>
              <span style="width:1px;height:20px;background:rgba(1,75,170,.12);margin:0 4px;"></span>
              <span class="fl-dash-name">{user_name}</span>
              {verified_html}
              <span class="fl-role-tag {role_class}">{role_label}</span>
            </div>
            """, unsafe_allow_html=True)
        with c_analytics:
            if st.button("📊 Impact Analytics", key="nav_analytics",
                         use_container_width=True,
                         type="primary" if page == "analytics" else "secondary"):
                st.session_state.page = "analytics"
                st.rerun()
        with c_dash:
            if st.button("🏠 Workspace", key="nav_dashboard",
                         use_container_width=True,
                         type="primary" if page == "dashboard" else "secondary"):
                st.session_state.page = "dashboard"
                st.rerun()
        with c_logout:
            if st.button("Log Out", key="nav_logout", use_container_width=True):
                _logout()


# ── Router ──────────────────────────────────────────────────────────────────
page = st.session_state.get("page", "landing")

if page == "landing":
    landing.render()

elif page == "auth":
    auth.render()

elif page in ("dashboard", "analytics"):
    if not st.session_state.get("authenticated"):
        st.session_state.page = "auth"
        st.session_state.auth_mode = "login"
        st.rerun()
    else:
        _render_dash_nav()
        if page == "analytics":
            analytics.render()
        else:
            role = st.session_state.get("user_role", "donor")
            if role == "donor":
                donor.render()
            elif role in ("recipient", "ngo"):
                recipient.render()
            elif role == "admin":
                admin.render()
            else:
                st.error(f"Unknown role: {role!r}")
                if st.button("Back to Home", key="unknown_role_home"):
                    _logout()

else:
    st.session_state.page = "landing"
    st.rerun()
