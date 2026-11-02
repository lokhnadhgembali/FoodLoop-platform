"""
app.py  –  FoodLoop  ·  Main Streamlit Entry Point
Modern SaaS UI with three page states: landing | auth | dashboard | analytics
"""
import streamlit as st

# ── Page config (MUST be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="FoodLoop – Rescue Surplus Food",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject global CSS ───────────────────────────────────────────────────────
from styles import get_css
st.markdown(get_css(), unsafe_allow_html=True)

# ── Initialize session state defaults ──────────────────────────────────────
_defaults = {
    "page":          "landing",
    "auth_mode":     "login",
    "signup_role":   "donor",
    "authenticated": False,
    "user_id":       None,
    "user_name":     None,
    "user_role":     None,
    "is_verified":   False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Initialize database (seeding etc.) ─────────────────────────────────────
import database
try:
    database.initialize()
except Exception as e:
    st.warning(f"DB init warning: {e}")

# ── Import views ────────────────────────────────────────────────────────────
from views import landing, auth, donor, recipient, admin, analytics


# ── Dashboard top nav (shown when authenticated, not on analytics page) ────
def _render_dash_nav():
    from utils import get_logo_img
    logo_b64 = get_logo_img(height=32, variant="blue", margin_right="0")
    role_colors = {"donor": "#014BAA", "recipient": "#059669", "ngo": "#059669", "admin": "#7C3AED"}
    role_labels = {"donor": "Donor", "recipient": "NGO", "ngo": "NGO", "admin": "Admin"}
    role = st.session_state.get("user_role", "donor")
    role_color = role_colors.get(role, "#014BAA")
    role_label = role_labels.get(role, role.capitalize())
    user_name  = st.session_state.get("user_name", "User")
    verified   = st.session_state.get("is_verified", False)
    verified_badge = '<span style="color:#059669;font-size:0.75rem;font-weight:700;">✅ Verified</span>' if verified else ""

    st.markdown(f"""
    <div style="
      background:rgba(255,255,255,0.9);
      backdrop-filter:blur(20px);
      -webkit-backdrop-filter:blur(20px);
      border-bottom:1px solid rgba(1,75,170,0.08);
      padding:10px 32px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      position:sticky;top:0;z-index:900;
    ">
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:36px;height:36px;background:linear-gradient(135deg,#014BAA,#0264E0);
             border-radius:10px;display:flex;align-items:center;justify-content:center;
             overflow:hidden;box-shadow:0 4px 12px rgba(1,75,170,0.3);">
          {logo_b64}
        </div>
        <span style="font-size:1.15rem;font-weight:800;color:#014BAA;">FoodLoop</span>
      </div>
      <div style="display:flex;align-items:center;gap:16px;">
        <div style="text-align:right;">
          <div style="font-size:0.9rem;font-weight:700;color:#0F172A;">{user_name}</div>
          <div style="display:flex;align-items:center;gap:6px;justify-content:flex-end;">
            <span style="background:{role_color}15;color:{role_color};font-size:0.7rem;
                   font-weight:800;padding:2px 10px;border-radius:999px;letter-spacing:0.5px;">
              {role_label.upper()}
            </span>
            {verified_badge}
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Streamlit action buttons row
    nb1, nb2, nb3, nb4 = st.columns([6, 1.2, 1.2, 1])
    with nb2:
        if st.button("📊 Analytics", key="nav_analytics", use_container_width=True):
            st.session_state.page = "analytics"
            st.rerun()
    with nb3:
        # Demo role switcher
        roles_available = ["donor", "recipient", "admin"]
        current_idx = roles_available.index(role) if role in roles_available else 0
        new_role = st.selectbox(
            "Switch Role",
            options=roles_available,
            index=current_idx,
            key="role_switcher",
            label_visibility="collapsed",
        )
        if new_role != role:
            st.session_state.user_role = new_role
            st.session_state.page = "dashboard"
            st.rerun()
    with nb4:
        if st.button("Logout", key="nav_logout", use_container_width=True, type="secondary"):
            for k in ["authenticated", "user_id", "user_name", "user_role", "is_verified"]:
                st.session_state[k] = None if k != "authenticated" else False
            st.session_state.page = "landing"
            st.rerun()


# ── Main router ─────────────────────────────────────────────────────────────
page = st.session_state.get("page", "landing")

if page == "landing":
    landing.render()

elif page == "auth":
    auth.render()

elif page == "analytics":
    if not st.session_state.get("authenticated"):
        st.session_state.page = "landing"
        st.rerun()
    else:
        _render_dash_nav()
        analytics.render()

elif page == "dashboard":
    if not st.session_state.get("authenticated"):
        st.session_state.page = "landing"
        st.rerun()
    else:
        _render_dash_nav()
        role = st.session_state.get("user_role", "donor")
        if role == "donor":
            donor.render()
        elif role in ("recipient", "ngo"):
            recipient.render()
        elif role == "admin":
            admin.render()
        else:
            st.error(f"Unknown role: {role}")

else:
    # Fallback
    st.session_state.page = "landing"
    st.rerun()
