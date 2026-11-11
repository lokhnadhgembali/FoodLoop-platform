"""
views/landing.py  -  FoodLoop Landing Page
Page state: st.session_state.page == "landing"
"""
import streamlit as st
import database
from utils import get_logo_img, fmt_num, fmt_kg, icon


def _goto_auth(mode: str):
    st.session_state.auth_mode = mode
    st.session_state.page = "auth"
    st.rerun()


# Feature data: (icon_name, title, description)
FEATURES = [
    ("brain",        "AI shelf-life check",      "Gemini-powered safety and storage advice for every listing."),
    ("key",          "4-digit PIN handshake",     "Zero-leakage verified venue pickup confirmed by both parties."),
    ("shield-check", "Verified organisations",    "Cross-checked hostels, messes and NGOs before they can claim."),
    ("clock",        "Urgent expiry alerts",      "Under-2-hour priority countdown on near-expiry surplus."),
    ("zap",          "Real-time matching",        "Instant partial or full quantity claims from verified NGOs."),
    ("leaf",         "SDG impact ledger",         "Live CO₂e avoided and meals saved on a public impact log."),
]


def _render_nav():
    logo = get_logo_img(height=24, variant="white", margin_right=0)
    with st.container(key="landing_nav"):
        c_brand, c_login, c_signup = st.columns([5.4, 1, 1.15])
        with c_brand:
            st.markdown(
                f'<div class="fl-nav-brand">'
                f'<span class="fl-nav-icon">{logo}</span>'
                f'<span class="fl-nav-name">FoodLoop</span>'
                f'<span class="fl-loc-pill">'
                f'{icon("map-pin", 12)} Jalandhar – Phagwara'
                f'</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with c_login:
            if st.button("Log in", key="nav_login", use_container_width=True):
                _goto_auth("login")
        with c_signup:
            if st.button("Sign up", key="nav_signup", use_container_width=True, type="primary"):
                _goto_auth("signup")


def _render_hero():
    st.markdown(
        '<div class="fl-hero">'
        '<h1>Rescue <span class="accent">surplus</span> food,<br>nourish your community</h1>'
        '<p>'
        'FoodLoop connects commercial kitchens, university messes and hostels with verified NGOs '
        'using real-time expiry tracking and 4-digit PIN handshakes — before edible food goes to waste.'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="hero_cta"):
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Create free account", key="hero_signup",
                         use_container_width=True, type="primary"):
                _goto_auth("signup")
        with c2:
            if st.button("Log in", key="hero_login", use_container_width=True):
                _goto_auth("login")


def _render_features():
    cards = []
    for icon_name, title, desc in FEATURES:
        cards.append(
            f'<div class="fl-feature-item">'
            f'<div class="fl-feature-icon">{icon(icon_name, 20)}</div>'
            f'<div class="fl-feature-text">'
            f'<div class="fl-feature-title">{title}</div>'
            f'<div class="fl-feature-desc">{desc}</div>'
            f'</div>'
            f'</div>'
        )
    items_html = "".join(cards)

    features_html = (
        f'<div class="fl-features-section">'
        f'<div class="fl-features-eyebrow">How it works</div>'
        f'<div class="fl-features-heading">Six systems, one mission</div>'
        f'<div class="fl-features-sub">'
        f'Everything working together to move surplus food to those who need it '
        f'before the pickup window closes.'
        f'</div>'
        f'<div class="fl-features">{items_html}</div>'
        f'</div>'
    )
    st.markdown(features_html, unsafe_allow_html=True)


def _render_impact_strip():
    try:
        stats = database.get_platform_stats()
    except Exception:
        stats = {}
    meals = stats.get("total_meals_saved", 0)
    kg    = stats.get("total_kg_diverted", 0.0)
    users = len(database.get_all_users()) if hasattr(database, "get_all_users") else 0

    st.markdown(
        f'<div class="fl-landing-strip">'
        f'<div class="fl-strip-card">'
        f'<div class="fl-strip-val">{fmt_num(meals)}</div>'
        f'<div class="fl-strip-lbl">Meals saved</div>'
        f'</div>'
        f'<div class="fl-strip-card">'
        f'<div class="fl-strip-val">{fmt_kg(float(kg))}</div>'
        f'<div class="fl-strip-lbl">Food rescued</div>'
        f'</div>'
        f'<div class="fl-strip-card">'
        f'<div class="fl-strip-val">{fmt_num(users)}</div>'
        f'<div class="fl-strip-lbl">Organisations</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_footer():
    st.markdown(
        '<div class="fl-landing-footer">'
        'FoodLoop · Bridging surplus food with hungry communities · Built for SDG 2 &amp; SDG 12'
        '</div>',
        unsafe_allow_html=True,
    )


def render():
    _render_nav()
    _render_hero()
    _render_features()
    _render_impact_strip()
    _render_footer()
