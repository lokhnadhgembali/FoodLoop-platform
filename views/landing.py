"""
views/landing.py  -  FoodLoop Modern SaaS Landing Page
Page state: st.session_state.page == "landing"
"""
import streamlit as st
import database
from utils import get_logo_img, fmt_num, fmt_kg


def _goto_auth(mode: str):
    st.session_state.auth_mode = mode
    st.session_state.page = "auth"
    st.rerun()


LEFT_FEATURES = [
    ("🤖", "AI Shelf-Life Check",   "Gemini-powered safety &amp; storage advice for every listing."),
    ("🔐", "4-Digit PIN Handshake", "Zero-leakage verified venue pickup, every single time."),
    ("✅", "Verified Organizations", "Cross-checked hostels, messes &amp; NGOs before they claim."),
]
RIGHT_FEATURES = [
    ("⏱️", "Urgent Expiry Alerts",  "&lt; 2hr priority countdown tags on near-expiry surplus."),
    ("⚡", "Real-Time Matching",     "Instant partial or full quantity claims from verified NGOs."),
    ("🌱", "SDG Impact Ledger",      "Live CO2e avoided &amp; meals saved on a public ledger."),
]


def _render_pill_nav():
    logo = get_logo_img(height=26, variant="white", margin_right=0)
    with st.container(key="landing_nav"):
        c_brand, c_login, c_signup = st.columns([5.4, 1, 1.15])
        with c_brand:
            st.markdown(f"""
            <div class="fl-nav-brand">
              <span class="fl-nav-icon">{logo}</span>
              <span class="fl-nav-name">FoodLoop</span>
              <span class="fl-loc-pill">📍 Jalandhar – Phagwara Hwy</span>
            </div>
            """, unsafe_allow_html=True)
        with c_login:
            if st.button("Log In", key="nav_login", use_container_width=True):
                _goto_auth("login")
        with c_signup:
            if st.button("Sign Up", key="nav_signup", use_container_width=True, type="primary"):
                _goto_auth("signup")


def _render_hero():
    st.markdown("""
    <div class="fl-hero">
      <div class="fl-status-pill">
        <span class="fl-status-dot"></span>
        ⚡ Smart Surplus Routing &amp; SDG-12 Engine Active
      </div>
      <h1>Rescue <span class="accent">Surplus</span> Food,<br>Nourish Your Community.</h1>
      <p>
        FoodLoop connects commercial kitchens, university messes, and hostels with verified NGOs
        using real-time expiry tracking and 4-digit PIN handshakes before edible food goes to waste.
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(key="hero_cta"):
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Create Free Account →", key="hero_signup",
                         use_container_width=True, type="primary"):
                _goto_auth("signup")
        with c2:
            if st.button("Log In", key="hero_login", use_container_width=True):
                _goto_auth("login")


def _engine_stack(features, side: str) -> str:
    """Build one column of three compact horizontal cards.

    Rendered as a single HTML block so the flex gap, alignment and staggered
    middle card are not affected by Streamlit's element spacing.
    """
    cards = []
    for i, (icon, title, desc) in enumerate(features):
        css = "engine-card stagger" if i == 1 else "engine-card"
        cards.append(f"""
        <div class="{css}">
          <div class="engine-icon">{icon}</div>
          <div class="engine-text">
            <div class="engine-title">{title}</div>
            <div class="engine-desc">{desc}</div>
          </div>
        </div>""")
    return f'<div class="engine-stack engine-stack-{side}">{"".join(cards)}</div>'


def _render_features():
    logo = get_logo_img(height=40, variant="white", margin_right=0)
    st.markdown("""
    <div class="fl-wrap" style="text-align:center;padding-top:44px;">
      <div style="font-size:0.72rem;font-weight:800;letter-spacing:2.2px;
                  text-transform:uppercase;color:#64748B;margin-bottom:8px;">
        The FoodLoop Engine
      </div>
      <h2 style="font-size:1.75rem;font-weight:800;color:#0F172A;letter-spacing:-0.8px;margin:0 0 6px;">
        Everything orbiting one mission
      </h2>
      <p style="color:#475569;font-size:0.92rem;margin:0;">
        Six systems working together to move surplus food before it expires.
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(key="orbit_stage"):
        left_col, hub_col, right_col = st.columns([1, 0.88, 1])

    with left_col:
        st.markdown(_engine_stack(LEFT_FEATURES, "left"), unsafe_allow_html=True)

    with hub_col:
        st.markdown(f"""
        <div class="fl-orbit-hub">
          <div class="fl-radar-ring r3"></div>
          <div class="fl-radar-ring r2"></div>
          <div class="fl-radar-ring r1"></div>
          <div class="fl-hub-glow"></div>
          <span class="fl-orbit-dot d1"></span>
          <span class="fl-orbit-dot d2"></span>
          <span class="fl-orbit-dot d3"></span>
          <span class="fl-orbit-dot d4"></span>
          <div class="fl-hub-core"><span>{logo or ""}</span></div>
        </div>
        <div class="fl-orbit-caption">Real-time surplus routing</div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown(_engine_stack(RIGHT_FEATURES, "right"), unsafe_allow_html=True)



def _render_impact_strip():
    try:
        stats = database.get_platform_stats()
    except Exception:
        stats = {}
    meals = stats.get("total_meals_saved", 0)
    kg    = stats.get("total_kg_diverted", 0.0)
    co2   = stats.get("total_co2_avoided", round(kg * 2.5, 1))
    users = len(database.get_all_users()) if hasattr(database, "get_all_users") else 0

    st.markdown(f"""
    <div class="fl-landing-strip">
      <div class="fl-strip-card">
        <div class="fl-strip-val">{fmt_num(meals)}</div>
        <div class="fl-strip-lbl">🍽️ Meals Saved</div>
      </div>
      <div class="fl-strip-card">
        <div class="fl-strip-val">{fmt_kg(float(kg))}</div>
        <div class="fl-strip-lbl">⚖️ Food Rescued</div>
      </div>
      <div class="fl-strip-card">
        <div class="fl-strip-val">{fmt_num(users)}</div>
        <div class="fl-strip-lbl">🏫 Organizations Onboard</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def _render_footer():
    st.markdown("""
    <div class="fl-landing-footer">
      FoodLoop · Bridging surplus food with hungry communities · Built for SDG 2 &amp; SDG 12
    </div>
    """, unsafe_allow_html=True)


def render():
    _render_pill_nav()
    _render_hero()
    _render_features()
    _render_impact_strip()
    _render_footer()
