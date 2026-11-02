"""
views/landing.py  –  FoodLoop Modern SaaS Landing Page
Page state: st.session_state.page == "landing"
"""
import streamlit as st
import database
from utils import get_logo_img, fmt_num, fmt_kg

def render():
    # ── Navbar ──────────────────────────────────────────────────────────────
    logo_b64 = get_logo_img(height=32, variant="blue", margin_right="0")
    st.markdown(f"""
    <div class="fl-pill-nav">
      <div class="fl-pill-nav-inner">
        <div class="fl-nav-brand-wrap">
          <div class="fl-nav-icon">{logo_b64}</div>
          <span class="fl-nav-brand-text">FoodLoop</span>
          <span class="fl-nav-loc-pill">📍 Jalandhar – Phagwara Hwy</span>
        </div>
        <div class="fl-nav-actions">
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Nav buttons — must be real Streamlit buttons (they change session_state)
    # Use columns hack inside the nav area
    nav_col1, nav_col2, nav_col3 = st.columns([8, 1, 1])
    with nav_col2:
        if st.button("Log In", key="nav_login", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.session_state.page = "auth"
            st.rerun()
    with nav_col3:
        if st.button("Sign Up", key="nav_signup", use_container_width=True):
            st.session_state.auth_mode = "signup"
            st.session_state.page = "auth"
            st.rerun()

    # ── Hero Section ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="fl-hero-wrap">
      <div class="fl-status-pill">
        <span class="fl-status-dot"></span>
        ⚡ Smart Surplus Routing &amp; SDG-12 Engine Active
      </div>
      <h1 class="fl-hero-headline">
        Rescue <span class="fl-hero-accent">Surplus</span> Food,<br>Nourish Your Community.
      </h1>
      <p class="fl-hero-sub">
        FoodLoop connects commercial kitchens, university messes, and hostels with verified NGOs
        using real-time expiry tracking and 4-digit PIN handshakes — before edible food goes to waste.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # CTA buttons — real Streamlit buttons centered
    c1, c2, c3 = st.columns([3, 1, 1])
    with c2:
        if st.button("🍲 Create Free Account", key="hero_signup", use_container_width=True):
            st.session_state.auth_mode = "signup"
            st.session_state.page = "auth"
            st.rerun()
    with c3:
        if st.button("Log In →", key="hero_login", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.session_state.page = "auth"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Live Platform Pulse ─────────────────────────────────────────────────
    stats = database.get_platform_stats()
    meals = stats.get("total_meals_saved", 0)
    kg = stats.get("total_kg_diverted", 0.0)
    co2 = round(kg * 2.5, 1)  # approx CO2e

    st.markdown("""<div style="text-align:center;margin:8px 0 4px">
      <span style="font-size:0.78rem;font-weight:700;color:#64748B;letter-spacing:1.5px;text-transform:uppercase;">
        Live Platform Pulse
      </span></div>""", unsafe_allow_html=True)

    kp1, kp2, kp3 = st.columns(3)
    for col, label, val, unit in [
        (kp1, "🍽️ Meals Saved", fmt_num(meals), "meals"),
        (kp2, "⚖️ Food Diverted", fmt_kg(kg), ""),
        (kp3, "🌿 CO₂e Avoided", f"{co2} kg", ""),
    ]:
        col.markdown(f"""
        <div style="background:white;border-radius:16px;border:1px solid rgba(1,75,170,0.08);
             box-shadow:0 8px 30px rgba(1,75,170,0.06);padding:24px;text-align:center;margin:4px;">
          <div style="font-size:1.8rem;font-weight:900;color:#014BAA;">{val} {unit}</div>
          <div style="font-size:0.85rem;font-weight:600;color:#475569;margin-top:4px;">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── How It Works ────────────────────────────────────────────────────────
    st.markdown("""<div style="text-align:center;margin:16px 0 8px">
      <h2 style="font-size:1.9rem;font-weight:800;color:#0F172A;">How FoodLoop Works</h2>
      <p style="color:#475569;font-size:0.95rem;">Three simple steps between surplus and a warm meal.</p>
    </div>""", unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    for col, step, icon, title, desc in [
        (s1, "01", "📦", "Donors Post Surplus",
         "Commercial kitchens & messes publish surplus food with a safe-pickup deadline."),
        (s2, "02", "🔔", "NGOs Claim & Get PIN",
         "Verified NGOs browse the live marketplace and claim listings — a secret 4-digit PIN is issued."),
        (s3, "03", "✅", "PIN-Verified Handover",
         "Donor verifies the NGO's PIN at pickup. Donation is logged and impact metrics updated instantly."),
    ]:
        col.markdown(f"""
        <div style="background:white;border-radius:16px;border:1px solid rgba(1,75,170,0.08);
             box-shadow:0 8px 30px rgba(1,75,170,0.06);padding:28px 20px;text-align:center;margin:4px;height:100%;">
          <div style="font-size:2.2rem;margin-bottom:10px;">{icon}</div>
          <div style="font-size:0.7rem;font-weight:800;color:#014BAA;letter-spacing:2px;margin-bottom:6px;">STEP {step}</div>
          <div style="font-size:1rem;font-weight:700;color:#0F172A;margin-bottom:8px;">{title}</div>
          <div style="font-size:0.85rem;color:#475569;line-height:1.5;">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── Features Grid ───────────────────────────────────────────────────────
    st.markdown("""<div style="text-align:center;margin:16px 0 24px">
      <h2 style="font-size:1.7rem;font-weight:800;color:#0F172A;">Platform Features</h2>
    </div>""", unsafe_allow_html=True)

    features = [
        ("🤖", "AI Shelf-Life Check", "Smart expiry estimation to flag food safety windows automatically."),
        ("🔐", "4-Digit PIN Handshake", "Cryptographically-simple but tamper-resistant pickup verification."),
        ("✅", "Verified Organizations", "Every NGO and donor is screened before going live on the platform."),
        ("⚡", "Urgent Expiry Alerts", "Real-time countdown badges highlight listings expiring within 2 hours."),
        ("📡", "Real-Time Matching", "Nearest-NGO routing based on location and food category preferences."),
        ("🌱", "SDG Impact Ledger", "Every pickup is logged against SDG 2 & SDG 12 for impact reporting."),
    ]
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        cols[i % 3].markdown(f"""
        <div style="background:white;border-radius:16px;border:1px solid rgba(1,75,170,0.08);
             box-shadow:0 8px 30px rgba(1,75,170,0.06);padding:24px 20px;margin:6px 4px;">
          <div style="font-size:1.8rem;margin-bottom:10px;">{icon}</div>
          <div style="font-size:0.95rem;font-weight:700;color:#0F172A;margin-bottom:6px;">{title}</div>
          <div style="font-size:0.82rem;color:#475569;line-height:1.5;">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── Footer ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:32px;border-top:1px solid rgba(1,75,170,0.08);margin-top:24px;">
      <span style="font-size:0.85rem;color:#94A3B8;">
        🍲 FoodLoop · Bridging Surplus Food with Hungry Communities · Built for SDG 2 &amp; SDG 12
      </span>
    </div>
    """, unsafe_allow_html=True)
