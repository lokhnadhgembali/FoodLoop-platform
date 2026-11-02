"""
styles.py  -  FoodLoop Global CSS (Modern SaaS UI)
Inject once from app.py via st.markdown(get_css(), unsafe_allow_html=True)
"""


def get_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ══════════════════════════════════════════
   TOKENS
══════════════════════════════════════════ */
:root {
  --blue:        #014BAA;
  --blue-2:      #0264E0;
  --blue-grad:   linear-gradient(135deg, #014BAA 0%, #0264E0 100%);
  --navy:        #06152D;
  --cream:       #F8F3F0;
  --white:       #FFFFFF;
  --coral:       #D9381E;
  --emerald:     #10B981;
  --text:        #0F172A;
  --muted:       #475569;
  --slate:       #64748B;
  --line:        rgba(1, 75, 170, 0.08);
  --line-2:      rgba(1, 75, 170, 0.16);
  --card-shadow: 0 8px 30px rgba(1, 75, 170, 0.06);
  --shadow-lg:   0 20px 60px rgba(1, 75, 170, 0.13);
  --radius:      16px;
  --radius-lg:   24px;
  --pill:        999px;
}

/* ── Base ── */
html, body, .stApp, [data-testid="stAppViewContainer"] {
  font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
  color: var(--text) !important;
}
[data-testid="stAppViewContainer"] {
  background: radial-gradient(circle at 50% 20%, #EFF6FF 0%, #F8F3F0 65%) !important;
  background-attachment: fixed !important;
}

/* ── Remove Streamlit chrome ── */
#MainMenu, header, footer,
[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"],
[data-testid="stSidebar"], [data-testid="collapsedControl"] {
  display: none !important;
  visibility: hidden !important;
  height: 0 !important;
}
[data-testid="stMainBlockContainer"], .block-container {
  padding: 0 !important;
  max-width: 100% !important;
}
[data-testid="stVerticalBlock"] { gap: 0.55rem; }
[data-testid="stHorizontalBlock"] { gap: 0.9rem; }

/* ══════════════════════════════════════════
   LAYOUT HELPERS
══════════════════════════════════════════ */
.fl-wrap   { max-width: 1100px; margin: 0 auto; padding: 0 24px; }
.fl-wrap-wide { max-width: 1400px; margin: 0 auto; padding: 0 28px; }
.fl-section { margin: 0 auto; }
.fl-muted  { color: var(--muted); }

/* ══════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════ */
[data-testid^="stBaseButton"] {
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  font-weight: 700 !important;
  border-radius: var(--pill) !important;
  font-size: 0.86rem !important;
  padding: 9px 22px !important;
  transition: transform 0.16s ease, box-shadow 0.16s ease, background 0.16s ease !important;
  box-shadow: none !important;
}
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-primaryFormSubmit"] {
  background: var(--blue-grad) !important;
  color: #FFFFFF !important;
  border: none !important;
  box-shadow: 0 6px 18px rgba(1, 75, 170, 0.28) !important;
}
[data-testid="stBaseButton-primary"]:hover,
[data-testid="stBaseButton-primaryFormSubmit"]:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 10px 26px rgba(1, 75, 170, 0.38) !important;
  color: #FFFFFF !important;
}
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-secondaryFormSubmit"] {
  background: #FFFFFF !important;
  color: var(--blue) !important;
  border: 1.4px solid var(--line-2) !important;
}
[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stBaseButton-secondaryFormSubmit"]:hover {
  background: rgba(1, 75, 170, 0.04) !important;
  border-color: var(--blue) !important;
  color: var(--blue) !important;
  transform: translateY(-1px) !important;
}

/* ══════════════════════════════════════════
   LANDING — FLOATING PILL NAVBAR
══════════════════════════════════════════ */
.st-key-landing_nav {
  position: sticky;
  top: 14px;
  z-index: 999;
  width: min(1100px, calc(100% - 40px));
  margin: 16px auto 0;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(22px);
  -webkit-backdrop-filter: blur(22px);
  border: 1px solid rgba(1, 75, 170, 0.1);
  border-radius: 999px;
  padding: 10px 24px;
  box-shadow: 0 10px 34px rgba(1, 75, 170, 0.1);
  display: flex;
  align-items: center;
  gap: 0 !important;
}
.st-key-landing_nav [data-testid="stVerticalBlock"] { gap: 0 !important; }
.st-key-landing_nav [data-testid="stHorizontalBlock"] {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: nowrap;
  margin: 0;
  width: 100%;
}
.st-key-landing_nav [data-testid="stColumn"] { display: flex; align-items: center; }
.st-key-landing_nav [data-testid="stElementContainer"],
.st-key-landing_nav [data-testid="stMarkdownContainer"] {
  margin: 0 !important;
  padding: 0 !important;
}
.st-key-landing_nav [data-testid^="stBaseButton"] {
  padding: 7px 18px !important;
  font-size: 0.81rem !important;
  white-space: nowrap;
}
.st-key-landing_nav [data-testid="stMarkdownContainer"] p {
  margin: 0 !important;
  line-height: 1 !important;
}

.fl-nav-brand {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  margin: 0;
  line-height: 1;
  height: 36px;
}
.fl-nav-icon {
  width: 36px; height: 36px;
  background: var(--blue-grad);
  border-radius: 11px;
  display: inline-flex; align-items: center; justify-content: center;
  box-shadow: 0 5px 14px rgba(1, 75, 170, 0.3);
  overflow: hidden;
  flex-shrink: 0;
  margin: 0;
  line-height: 1;
}
.fl-nav-icon img {
  width: 26px; height: 26px;
  object-fit: contain;
  display: block;
  margin: 0;
  vertical-align: middle;
}
.fl-nav-name {
  font-size: 1.08rem; font-weight: 800; color: var(--blue); letter-spacing: -0.3px;
  white-space: nowrap;
  margin: 0;
  line-height: 1;
  display: inline-flex;
  align-items: center;
}
.fl-loc-pill {
  display: inline-flex; align-items: center; gap: 5px;
  background: rgba(1, 75, 170, 0.05);
  border: 1px solid rgba(1, 75, 170, 0.1);
  border-radius: 999px;
  padding: 5px 12px;
  font-size: 0.71rem; font-weight: 600; color: var(--blue);
  margin: 0;
  line-height: 1;
  white-space: nowrap;
  white-space: nowrap;
}

/* ══════════════════════════════════════════
   LANDING — HERO
══════════════════════════════════════════ */
.fl-hero { text-align: center; padding: 74px 24px 34px; }
.fl-status-pill {
  display: inline-flex; align-items: center; gap: 8px;
  background: #FFFFFF;
  border: 1px solid var(--line-2);
  border-radius: 999px;
  padding: 7px 18px;
  font-size: 0.78rem; font-weight: 700; color: var(--blue);
  box-shadow: 0 2px 10px rgba(1, 75, 170, 0.06);
  letter-spacing: 0.2px;
}
.fl-status-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--emerald);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
  animation: fl-blink 1.9s ease-in-out infinite;
}
@keyframes fl-blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }

.fl-hero h1 {
  font-size: clamp(38px, 5.4vw, 64px);
  font-weight: 800;
  line-height: 1.06;
  letter-spacing: -2px;
  color: #0F172A;
  margin: 26px auto 20px;
  max-width: 900px;
}
.fl-hero h1 .accent { color: var(--blue); }
.fl-hero p {
  font-size: clamp(15px, 1.3vw, 18px);
  color: var(--muted);
  max-width: 680px;
  margin: 0 auto;
  line-height: 1.68;
}

/* Hero CTA row (Streamlit buttons inside keyed container) */
.st-key-hero_cta { max-width: 520px; margin: 30px auto 0; }
.st-key-hero_cta [data-testid="stHorizontalBlock"] { justify-content: center; }
.st-key-hero_cta [data-testid^="stBaseButton"] {
  padding: 12px 30px !important;
  font-size: 0.95rem !important;
  width: 100%;
}

/* ══════════════════════════════════════════
   LANDING — ORBITAL FEATURES
══════════════════════════════════════════ */
.st-key-orbit_stage {
  max-width: 1100px;
  margin: 0 auto;
  padding: 18px 24px 0;
}
.st-key-orbit_stage [data-testid="stHorizontalBlock"] {
  align-items: center;
  gap: 22px;
}
/* Compact horizontal engine cards — three per column, aligned toward the radar */
.engine-stack {
  display: flex;
  flex-direction: column;
  gap: 22px;
  width: 100%;
}
.engine-stack-left  { align-items: flex-end; }
.engine-stack-right { align-items: flex-start; }

.engine-card {
  display: flex;
  align-items: center;
  gap: 14px;
  width: 100%;
  max-width: 340px;
  box-sizing: border-box;
  padding: 16px 20px;
  background: #FFFFFF;
  border: 1.5px solid rgba(1, 75, 170, 0.10);
  border-radius: 14px;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  text-align: left;
}
.engine-card:hover {
  border-color: #014BAA !important;
  box-shadow: 0 10px 26px rgba(1, 75, 170, 0.16), 0 0 0 1px #014BAA;
  transform: translateY(-3px);
}
.engine-icon {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: #EFF6FF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 19px;
  flex-shrink: 0;
}
.engine-text { display: flex; flex-direction: column; min-width: 0; }
.engine-title {
  font-size: 15px;
  font-weight: 700;
  color: #0F172A;
  margin: 0 0 3px 0;
  line-height: 1.3;
}
.engine-desc {
  font-size: 13px;
  color: #64748B;
  margin: 0;
  line-height: 1.35;
}
/* staggered middle card, pushing outward away from the hub */
.engine-stack-left  .engine-card.stagger { margin-right: 16px; }
.engine-stack-right .engine-card.stagger { margin-left: 16px; }

.fl-orbit-hub {
  position: relative;
  width: 300px; height: 300px;
  display: flex; align-items: center; justify-content: center;
  justify-self: center;
}
.fl-radar-ring {
  position: absolute;
  top: 50%; left: 50%;
  border-radius: 50%;
  border: 1.4px solid rgba(1, 75, 170, 0.14);
  transform: translate(-50%, -50%);
  animation: fl-radar 4.6s ease-in-out infinite;
}
.fl-radar-ring.r1 { width: 96px;  height: 96px;  animation-delay: 0s; }
.fl-radar-ring.r2 { width: 172px; height: 172px; animation-delay: 0.9s; }
.fl-radar-ring.r3 { width: 252px; height: 252px; animation-delay: 1.8s; }
@keyframes fl-radar {
  0%, 100% { opacity: 0.35; transform: translate(-50%, -50%) scale(1); }
  50%      { opacity: 0.85; transform: translate(-50%, -50%) scale(1.035); }
}
.fl-hub-glow {
  position: absolute;
  width: 190px; height: 190px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(2, 100, 224, 0.22) 0%, rgba(2, 100, 224, 0) 70%);
  filter: blur(2px);
}
.fl-hub-core {
  position: relative; z-index: 2;
  width: 78px; height: 78px;
  border-radius: 22px;
  background: var(--blue-grad);
  display: flex; align-items: center; justify-content: center;
  font-size: 30px;
  transform: rotate(45deg);
  box-shadow: 0 0 0 9px rgba(1, 75, 170, 0.08), 0 0 46px rgba(1, 75, 170, 0.35);
}
.fl-hub-core > span { transform: rotate(-45deg); display: inline-flex; }
.fl-hub-core img { width: 40px; height: 40px; object-fit: contain; transform: rotate(-45deg); }
.fl-orbit-dot {
  position: absolute;
  width: 9px; height: 9px;
  border-radius: 50%;
  background: var(--blue-2);
  box-shadow: 0 0 12px rgba(2, 100, 224, 0.7);
  animation: fl-blink 2.6s ease-in-out infinite;
}
.fl-orbit-dot.d1 { top: 12%;  left: 20%; }
.fl-orbit-dot.d2 { top: 22%;  right: 12%; animation-delay: 0.5s; background: var(--emerald); box-shadow: 0 0 12px rgba(16,185,129,.7); }
.fl-orbit-dot.d3 { bottom: 16%; left: 10%;  animation-delay: 1s; }
.fl-orbit-dot.d4 { bottom: 10%; right: 24%; animation-delay: 1.5s; background: var(--emerald); box-shadow: 0 0 12px rgba(16,185,129,.7); }
.fl-orbit-caption {
  text-align: center;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1.6px;
  text-transform: uppercase;
  color: var(--slate);
  margin-top: 4px;
}

/* Landing lower strip / footer */
.fl-landing-strip {
  max-width: 1100px;
  margin: 34px auto 0;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 0 24px;
}
.fl-strip-card {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--card-shadow);
  text-align: center;
}
.fl-strip-val { font-size: 1.45rem; font-weight: 800; color: var(--blue); letter-spacing: -0.5px; }
.fl-strip-lbl {
  font-size: 0.73rem; font-weight: 700; color: var(--slate);
  text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;
}
.fl-landing-footer {
  text-align: center;
  padding: 46px 24px 34px;
  color: #94A3B8;
  font-size: 0.82rem;
}

/* ══════════════════════════════════════════
   AUTH — SPLIT SCREEN
══════════════════════════════════════════ */
.st-key-auth_page { padding: 26px 26px 34px; }
.st-key-auth_page [data-testid="stHorizontalBlock"] { gap: 20px; align-items: stretch; }

.st-key-auth_left {
  background: var(--navy);
  border-radius: var(--radius-lg);
  padding: 34px 36px;
  min-height: 780px;
  height: 100%;
  position: relative;
  overflow: hidden;
  box-shadow: 0 24px 70px rgba(6, 21, 45, 0.35);
}
.st-key-auth_left::before {
  content: '';
  position: absolute;
  top: -140px; right: -100px;
  width: 340px; height: 340px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(2, 100, 224, 0.35) 0%, transparent 70%);
}
.st-key-auth_left::after {
  content: '';
  position: absolute;
  bottom: -120px; left: -110px;
  width: 320px; height: 320px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%);
}
.st-key-auth_left [data-testid="stMarkdownContainer"] { position: relative; z-index: 1; }
.st-key-auth_left [data-testid^="stBaseButton"] {
  background: rgba(255, 255, 255, 0.07) !important;
  color: rgba(255, 255, 255, 0.82) !important;
  border: 1px solid rgba(255, 255, 255, 0.14) !important;
  border-radius: 999px !important;
  font-size: 0.8rem !important;
  padding: 7px 16px !important;
  width: auto !important;
}
.st-key-auth_left [data-testid^="stBaseButton"]:hover {
  background: rgba(255, 255, 255, 0.13) !important;
  color: #FFFFFF !important;
}

.fl-auth-brand-badge {
  display: inline-flex; align-items: center; gap: 10px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 999px;
  padding: 8px 18px 8px 10px;
  margin: 26px 0 30px;
}
.fl-auth-brand-badge .icon {
  width: 34px; height: 34px;
  border-radius: 10px;
  background: var(--blue-grad);
  display: flex; align-items: center; justify-content: center;
  overflow: hidden; font-size: 17px;
}
.fl-auth-brand-badge .icon img { width: 24px; height: 24px; object-fit: contain; }
.fl-auth-brand-badge .name { font-size: 1.06rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.2px; }

.fl-auth-headline {
  font-size: 1.95rem;
  font-weight: 800;
  color: #FFFFFF;
  line-height: 1.16;
  letter-spacing: -0.8px;
  margin-bottom: 8px;
}
.fl-auth-headline .accent { color: #60A5FA; }
.fl-auth-lead {
  font-size: 0.86rem;
  color: rgba(255, 255, 255, 0.55);
  line-height: 1.6;
  margin-bottom: 28px;
}

.fl-glass-pill {
  display: flex; align-items: center; gap: 11px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 13px 16px;
  margin-bottom: 10px;
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.82rem;
  font-weight: 500;
  backdrop-filter: blur(4px);
}
.fl-glass-pill .icon { font-size: 15px; }

.fl-auth-proof {
  margin-top: 30px;
  padding-top: 22px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.55);
  line-height: 1.6;
}
.fl-live-pill {
  display: inline-flex; align-items: center; gap: 7px;
  margin-top: 18px;
  background: rgba(16, 185, 129, 0.14);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 999px;
  padding: 6px 14px;
  font-size: 0.73rem; font-weight: 700; color: #4ADE80;
}
.fl-live-pill .dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: #22C55E;
  animation: fl-blink 1.6s ease-in-out infinite;
}

/* Auth right form card */
.st-key-auth_right {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  padding: 40px 44px;
  min-height: 780px;
  box-shadow: var(--card-shadow);
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.fl-form-heading { font-size: 1.72rem; font-weight: 800; color: var(--text); letter-spacing: -0.6px; margin: 0 0 6px; }
.fl-form-sub { font-size: 0.88rem; color: var(--slate); line-height: 1.55; margin: 0 0 24px; }
.fl-field-label {
  display: block;
  font-size: 0.78rem; font-weight: 700; color: var(--text);
  letter-spacing: 0.2px; margin: 0 0 2px;
}
.fl-link-row {
  text-align: center;
  font-size: 0.83rem;
  color: var(--slate);
  line-height: 1.5;
  /* padding (not margin) so Streamlit's markdown container grows and the
     button below is not pulled up over the text */
  margin: 0;
  padding: 16px 0 12px;
}
.fl-link-row b { color: var(--blue); }
/* the caption above these buttons must not be overlapped by them */
.st-key-to_signup [data-testid="stButton"],
.st-key-to_login [data-testid="stButton"] {
  margin-top: 18px;
}

:is(.st-key-role_pills, .st-key-login_role_pills) [data-testid="stHorizontalBlock"] { gap: 8px; }
:is(.st-key-role_pills, .st-key-login_role_pills) [data-testid^="stBaseButton"] {
  width: 100%;
  font-size: 0.79rem !important;
  padding: 8px 8px !important;
  border-radius: 11px !important;
}
:is(.st-key-role_pills, .st-key-login_role_pills) [data-testid="stBaseButton-secondary"] {
  background: rgba(1, 75, 170, 0.02) !important;
  color: var(--slate) !important;
}
:is(.st-key-role_pills, .st-key-login_role_pills) [data-testid="stBaseButton-primary"] {
  box-shadow: 0 0 0 3px rgba(1, 75, 170, 0.1) !important;
}

.fl-demo-divider {
  display: flex; align-items: center; gap: 12px;
  margin: 20px 0 12px;
  font-size: 0.68rem; font-weight: 800; color: #94A3B8;
  letter-spacing: 1.4px; text-transform: uppercase;
}
.fl-demo-divider::before, .fl-demo-divider::after {
  content: ''; flex: 1; height: 1px; background: rgba(15, 23, 42, 0.08);
}
.st-key-demo_row [data-testid="stHorizontalBlock"] { gap: 8px; }
.st-key-demo_row [data-testid^="stBaseButton"] {
  width: 100%;
  font-size: 0.75rem !important;
  padding: 8px 6px !important;
  border-radius: 11px !important;
  white-space: nowrap;
}

/* ══════════════════════════════════════════
   DASHBOARD — FLOATING NAV
══════════════════════════════════════════ */
.st-key-dash_nav {
  position: sticky;
  top: 12px;
  z-index: 998;
  width: min(1400px, calc(100% - 36px));
  margin: 14px auto 4px;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(22px);
  -webkit-backdrop-filter: blur(22px);
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 9px 18px;
  box-shadow: 0 10px 30px rgba(1, 75, 170, 0.08);
}
.st-key-dash_nav [data-testid="stHorizontalBlock"] { align-items: center; gap: 0.5rem; flex-wrap: nowrap; }
.st-key-dash_nav [data-testid^="stBaseButton"] {
  padding: 7px 16px !important;
  font-size: 0.79rem !important;
  white-space: nowrap;
}
.st-key-dash_nav [data-testid="stMarkdownContainer"] p { margin: 0 !important; }

.st-key-dash_nav [data-testid="stColumn"] { display: flex; align-items: center; }
.st-key-dash_nav [data-testid="stElementContainer"],
.st-key-dash_nav [data-testid="stMarkdownContainer"] {
  margin: 0 !important;
  padding: 0 !important;
}
.fl-dash-user {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin: 0;
  line-height: 1;
  min-height: 34px;
}
.fl-dash-name { font-size: 0.88rem; font-weight: 800; color: var(--text); }
.fl-verified {
  display: inline-flex; align-items: center; gap: 4px;
  background: #DCFCE7; color: #166534;
  border-radius: 999px; padding: 2px 9px;
  font-size: 0.66rem; font-weight: 800;
}
.fl-role-tag {
  display: inline-flex; align-items: center; gap: 4px;
  border-radius: 999px; padding: 2px 10px;
  font-size: 0.65rem; font-weight: 800; letter-spacing: 0.5px;
  text-transform: uppercase;
}
.fl-role-donor     { background: #EFF6FF; color: #014BAA; }
.fl-role-recipient { background: #ECFDF5; color: #047857; }
.fl-role-admin     { background: #F5F3FF; color: #6D28D9; }

/* ══════════════════════════════════════════
   DASHBOARD — CONTENT
══════════════════════════════════════════ */
.fl-page-head { padding: 26px 4px 6px; }
.fl-page-title {
  font-size: 1.6rem; font-weight: 800; color: var(--text);
  letter-spacing: -0.6px; margin: 0;
}
.fl-page-sub { font-size: 0.88rem; color: var(--slate); margin: 4px 0 0; }

.fl-kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(168px, 1fr));
  gap: 14px;
  margin: 14px 0 6px;
}
.fl-kpi {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 18px;
  box-shadow: var(--card-shadow);
  position: relative;
  overflow: hidden;
}
.fl-kpi::before {
  content: '';
  position: absolute; inset: 0 0 auto 0;
  height: 3px;
  background: var(--blue-grad);
}
.fl-kpi.urgent::before { background: linear-gradient(135deg, #D9381E, #F97316); }
.fl-kpi-icon { font-size: 1.15rem; margin-bottom: 8px; }
.fl-kpi-val {
  font-size: 1.6rem; font-weight: 800; color: var(--blue);
  letter-spacing: -0.8px; line-height: 1.1;
}
.fl-kpi.urgent .fl-kpi-val { color: var(--coral); }
.fl-kpi-label {
  font-size: 0.7rem; font-weight: 700; color: var(--slate);
  text-transform: uppercase; letter-spacing: 0.9px; margin-top: 4px;
}

/* Generic white card for HTML blocks */
.fl-card {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 22px 24px;
  box-shadow: var(--card-shadow);
  margin: 10px 0;
}
.fl-card-title {
  font-size: 0.98rem; font-weight: 800; color: var(--text);
  letter-spacing: -0.2px; margin: 0 0 6px;
}
.fl-card-sub { font-size: 0.82rem; color: var(--slate); line-height: 1.55; margin: 0 0 16px; }

/* Food listing / marketplace cards */
.fl-food-card {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-left: 4px solid var(--blue);
  border-radius: var(--radius);
  padding: 18px 20px;
  box-shadow: var(--card-shadow);
  margin: 10px 0;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.fl-food-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-2px); }
.fl-food-card.urgent { border-left-color: var(--coral); border-color: rgba(217, 56, 30, 0.18); }
.fl-food-head { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }
.fl-food-name { font-size: 1.02rem; font-weight: 800; color: var(--text); }
.fl-tag {
  display: inline-flex; align-items: center;
  border-radius: 7px; padding: 2px 9px;
  font-size: 0.69rem; font-weight: 800;
}
.fl-tag-blue    { background: #EFF6FF; color: #014BAA; }
.fl-tag-cooked  { background: #FFF1EB; color: #C2410C; }
.fl-tag-bakery  { background: #FEFCE8; color: #854D0E; }
.fl-tag-produce { background: #F0FDF4; color: #15803D; }
.fl-tag-dairy   { background: #E0F2FE; color: #0369A1; }
.fl-tag-packaged{ background: #F5F3FF; color: #6D28D9; }
.fl-tag-beverages{ background: #FDF2F8; color: #BE185D; }
.fl-urgent-badge {
  display: inline-flex; align-items: center; gap: 4px;
  background: rgba(217, 56, 30, 0.08);
  border: 1px solid rgba(217, 56, 30, 0.25);
  color: var(--coral);
  border-radius: 999px;
  padding: 2px 10px;
  font-size: 0.68rem; font-weight: 800;
  animation: fl-urgent 1.9s ease-in-out infinite;
}
@keyframes fl-urgent { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
.fl-food-meta { font-size: 0.81rem; color: var(--muted); display: flex; gap: 14px; flex-wrap: wrap; margin-top: 4px; }
.fl-food-meta b { color: var(--text); }
.fl-countdown { font-size: 0.79rem; font-weight: 700; color: var(--slate); margin-top: 7px; }
.fl-countdown.urgent { color: var(--coral); }

/* Requests queue */
.fl-req-card {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-left: 4px solid #F59E0B;
  border-radius: 14px;
  padding: 15px 18px;
  box-shadow: var(--card-shadow);
  margin: 8px 0;
}
.fl-req-card.approved  { border-left-color: var(--emerald); }
.fl-req-card.rejected  { border-left-color: var(--coral); }
.fl-req-card.completed { border-left-color: #64748B; }
.fl-req-title { font-size: 0.94rem; font-weight: 800; color: var(--text); }
.fl-req-meta { font-size: 0.79rem; color: var(--muted); margin-top: 4px; }
.fl-status {
  display: inline-flex; border-radius: 999px;
  padding: 2px 10px; font-size: 0.67rem; font-weight: 800;
  text-transform: uppercase; letter-spacing: 0.4px;
}
.fl-status-pending   { background: #FEF9C3; color: #854D0E; }
.fl-status-approved  { background: #DCFCE7; color: #166534; }
.fl-status-completed { background: #F1F5F9; color: #475569; }
.fl-status-rejected  { background: #FEE2E2; color: #B91C1C; }

/* PIN ticket */
.fl-ticket {
  background: linear-gradient(135deg, #01295C 0%, #014BAA 52%, #0264E0 100%);
  border-radius: var(--radius-lg);
  padding: 26px 24px;
  margin: 12px 0;
  color: #FFFFFF;
  position: relative;
  overflow: hidden;
  box-shadow: 0 14px 44px rgba(1, 75, 170, 0.38);
}
.fl-ticket::before {
  content: '';
  position: absolute;
  top: -60px; right: -50px;
  width: 180px; height: 180px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.06);
}
.fl-ticket::after {
  content: '';
  position: absolute;
  bottom: -70px; left: -40px;
  width: 170px; height: 170px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.04);
}
.fl-ticket-label {
  font-size: 0.68rem; font-weight: 800; letter-spacing: 2.2px;
  text-transform: uppercase; opacity: 0.72; position: relative; z-index: 1;
}
.fl-ticket-pin {
  font-family: 'Courier New', monospace;
  font-size: 2.9rem; font-weight: 700;
  letter-spacing: 0.34em;
  margin: 10px 0 4px;
  position: relative; z-index: 1;
  text-shadow: 0 4px 18px rgba(0, 0, 0, 0.28);
}
.fl-ticket-food { font-size: 0.92rem; font-weight: 800; position: relative; z-index: 1; }
.fl-ticket-meta { font-size: 0.78rem; opacity: 0.78; margin-top: 4px; position: relative; z-index: 1; }
.fl-ticket-hint {
  margin-top: 14px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 10px;
  padding: 9px 13px;
  font-size: 0.75rem; font-weight: 600;
  position: relative; z-index: 1;
}

/* Empty states */
.fl-empty {
  background: #FFFFFF;
  border: 1px dashed rgba(1, 75, 170, 0.18);
  border-radius: var(--radius);
  padding: 42px 24px;
  text-align: center;
  margin: 12px 0;
}
.fl-empty-icon { font-size: 2.2rem; margin-bottom: 8px; }
.fl-empty-title { font-size: 0.95rem; font-weight: 800; color: var(--text); margin-bottom: 4px; }
.fl-empty-sub { font-size: 0.82rem; color: var(--slate); }

/* Admin user rows */
.fl-user-row {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 12px 16px;
  margin: 7px 0;
  display: flex; align-items: center; justify-content: space-between;
  gap: 12px; flex-wrap: wrap;
  box-shadow: 0 2px 10px rgba(1, 75, 170, 0.04);
}
.fl-user-name { font-size: 0.9rem; font-weight: 800; color: var(--text); }
.fl-user-meta { font-size: 0.76rem; color: var(--slate); margin-top: 3px; }
.fl-badge-ok   { background: #DCFCE7; color: #166534; border-radius: 6px; padding: 2px 8px; font-size: 0.66rem; font-weight: 800; }
.fl-badge-warn { background: #FEF3C7; color: #92400E; border-radius: 6px; padding: 2px 8px; font-size: 0.66rem; font-weight: 800; }

/* ══════════════════════════════════════════
   ANALYTICS
══════════════════════════════════════════ */
.fl-chart-card {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 18px 18px 10px;
  box-shadow: var(--card-shadow);
  margin: 10px 0;
}
.fl-chart-title { font-size: 0.92rem; font-weight: 800; color: var(--text); margin-bottom: 10px; }
.fl-impact-banner {
  background: var(--blue-grad);
  border-radius: var(--radius-lg);
  padding: 32px 36px;
  color: #FFFFFF;
  margin: 16px 0;
  box-shadow: 0 18px 50px rgba(1, 75, 170, 0.3);
}
.fl-impact-label { font-size: 0.72rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; opacity: 0.75; }
.fl-impact-value { font-size: 2.5rem; font-weight: 800; letter-spacing: -1.2px; margin: 6px 0 10px; }
.fl-impact-stats { display: flex; gap: 34px; flex-wrap: wrap; margin-top: 14px; }
.fl-impact-stat b { display: block; font-size: 1.2rem; font-weight: 800; }
.fl-impact-stat span { font-size: 0.7rem; letter-spacing: 1px; text-transform: uppercase; opacity: 0.75; }

/* ══════════════════════════════════════════
   STREAMLIT WIDGETS
══════════════════════════════════════════ */
.stTextInput input, .stNumberInput input, .stTextArea textarea {
  border-radius: 11px !important;
  border: 1.5px solid var(--blue) !important;
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  font-size: 0.88rem !important;
  color: var(--text) !important;
  background: #FFFFFF !important;
  padding: 10px 13px !important;
  box-shadow: none !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
  border-color: var(--blue-dark, #013A85) !important;
  box-shadow: 0 0 0 3px rgba(1, 75, 170, 0.14) !important;
}
[data-baseweb="select"] > div,
[data-testid="stSelectbox"] .react-aria-ComboBox > div {
  border-radius: 11px !important;
  border: 1.5px solid var(--blue) !important;
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  font-size: 0.88rem !important;
  background: #FFFFFF !important;
}
[data-testid="stSelectbox"] .react-aria-ComboBox > div:focus-within {
  box-shadow: 0 0 0 3px rgba(1, 75, 170, 0.14) !important;
}
.stTextInput label, .stNumberInput label, .stTextArea label,
.stSelectbox label, .stSlider label, .stFileUploader label {
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  letter-spacing: 0.2px !important;
}
[data-testid="stWidgetLabel"] p { font-weight: 700 !important; font-size: 0.78rem !important; }

[data-testid="stTabs"] [data-baseweb="tab-list"],
[data-testid="stTabs"] [role="tablist"] {
  gap: 4px;
  border-bottom: 1px solid var(--line);
  background: transparent;
}
/* Streamlit 1.6x renders each tab as div[data-testid="stTab"], not a button */
[data-testid="stTabs"] [data-testid="stTab"] {
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.84rem !important;
  color: #0F172A !important;
  padding: 9px 16px !important;
  border-bottom: 2px solid transparent !important;
}
[data-testid="stTabs"] [data-testid="stTab"] p,
[data-testid="stTabs"] [data-testid="stTab"] span,
[data-testid="stTabs"] [data-testid="stTab"] [data-testid="stMarkdownContainer"] {
  color: #0F172A !important;
  margin-bottom: 0 !important;
}
[data-testid="stTabs"] [data-testid="stTab"]:hover p,
[data-testid="stTabs"] [data-testid="stTab"]:hover span {
  color: var(--blue) !important;
}
[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] {
  border-bottom-color: var(--blue) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background: var(--blue) !important; }

/* Headings must always be dark, even if Streamlit's dark theme is active */
.fl-page-title,
.fl-card-title,
.fl-req-title,
.fl-food-name,
.fl-user-name,
.fl-empty-title,
.fl-chart-title,
[data-testid="stHeading"],
[data-testid="stHeading"] *,
.st-key-donor_body h1, .st-key-donor_body h2, .st-key-donor_body h3,
.st-key-donor_body h4, .st-key-donor_body h5, .st-key-donor_body h6,
.st-key-recipient_body h1, .st-key-recipient_body h2, .st-key-recipient_body h3,
.st-key-recipient_body h4, .st-key-recipient_body h5, .st-key-recipient_body h6,
.st-key-admin_body h1, .st-key-admin_body h2, .st-key-admin_body h3,
.st-key-admin_body h4, .st-key-admin_body h5, .st-key-admin_body h6,
.st-key-analytics_body h1, .st-key-analytics_body h2, .st-key-analytics_body h3,
.st-key-analytics_body h4, .st-key-analytics_body h5, .st-key-analytics_body h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6 {
  color: #0F172A !important;
}

[data-testid="stExpander"] {
  background: #FFFFFF !important;
  border: 1px solid var(--line) !important;
  border-radius: 12px !important;
  box-shadow: 0 2px 10px rgba(1, 75, 170, 0.04) !important;
  margin-bottom: 6px;
}
[data-testid="stExpander"] summary { font-weight: 700 !important; font-size: 0.84rem !important; color: var(--blue) !important; }

[data-testid="stForm"] {
  background: #FFFFFF;
  border: 1px solid var(--line) !important;
  border-radius: var(--radius) !important;
  padding: 20px 22px !important;
  box-shadow: var(--card-shadow);
}
[data-testid="stDataFrame"] {
  border-radius: 12px !important;
  overflow: hidden;
  border: 1px solid var(--line);
}
.stPlotlyChart { border-radius: 12px !important; overflow: hidden; }

/* Alerts */
[data-testid="stAlert"] { border-radius: 12px !important; font-size: 0.85rem !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 7px; height: 7px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(1, 75, 170, 0.18); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(1, 75, 170, 0.32); }

/* Keyed dashboard shells */
.st-key-donor_body,
.st-key-recipient_body,
.st-key-admin_body,
.st-key-analytics_body {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 28px 34px;
}
.st-key-chart_weekly,
.st-key-chart_status,
.st-key-chart_category,
.st-key-chart_expiring {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 16px 18px 8px;
  box-shadow: var(--card-shadow);
  margin: 6px 0;
  height: 100%;
}

/* Responsive */
@media (max-width: 980px) {
  .fl-orbit-stage { grid-template-columns: 1fr; }
  .fl-orbit-hub { margin: 8px auto; }
  .fl-landing-strip { grid-template-columns: 1fr; }
  .st-key-auth_left, .st-key-auth_right { min-height: auto; padding: 26px; }
  .st-key-dash_nav, .st-key-landing_nav { border-radius: 24px; }
}
</style>
"""
