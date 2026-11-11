"""
styles.py  -  FoodLoop Global CSS
Inject once from app.py via st.markdown(get_css(), unsafe_allow_html=True)
"""


def get_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');

/* ══════════════════════════════════════════
   PASS 1 + 2: TOKENS — warm neutral ramp, solid accent
══════════════════════════════════════════ */
:root {
  /* Warm neutral ramp (light) */
  --bg:          #f7f4ee;
  --surface:     #fdfbf7;
  --raised:      #ede8df;
  --hairline:    rgba(31, 27, 22, 0.08);
  --hairline-2:  rgba(31, 27, 22, 0.16);

  /* Text — three roles only */
  --text:        #1f1b16;
  --text-2:      #5e554a;
  --muted:       #7b7266;

  /* Accent — real brand blue, solid */
  --blue:        #014BAA;
  --blue-dark:   #013A85;

  /* Semantic */
  --green:       #16a34a;
  --amber:       #d97706;
  --red:         #dc2626;
  --coral:       #D9381E;
  --emerald:     #10B981;

  /* Radius — nested system */
  --r-xs:        4px;
  --r-sm:        6px;
  --r-md:        10px;
  --r-card:      12px;
  --r-panel:     16px;

  /* Shadow — neutral, soft */
  --shadow-sm:   0 1px 2px rgba(0,0,0,0.05);
  --shadow-md:   0 4px 16px rgba(0,0,0,0.06);
  --shadow-lg:   0 8px 24px rgba(0,0,0,0.08);

  /* Pass 9: Motion — one curve, named durations */
  --ease:        cubic-bezier(0.22, 1, 0.36, 1);
  --dur-fast:    150ms;
  --dur-mid:     200ms;
}

/* ── Pass 5: Base — font, weight, colour ── */
html, body, .stApp, [data-testid="stAppViewContainer"] {
  font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
  font-weight: 400 !important;
  color: var(--text) !important;
}
[data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
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
/* Pass 1: Spacing — Streamlit's default gaps → 4px grid */
[data-testid="stVerticalBlock"]   { gap: 8px; }
[data-testid="stHorizontalBlock"] { gap: 16px; }

/* ══════════════════════════════════════════
   LAYOUT HELPERS
══════════════════════════════════════════ */
.fl-wrap      { max-width: 1100px; margin: 0 auto; padding: 0 24px; }
.fl-wrap-wide { max-width: 1400px; margin: 0 auto; padding: 0 28px; }
.fl-section   { margin: 0 auto; }
.fl-muted     { color: var(--muted); }

/* ══════════════════════════════════════════
   PASS 7: BUTTONS
══════════════════════════════════════════ */
[data-testid^="stBaseButton"] {
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  font-weight: 500 !important;
  border-radius: var(--r-md) !important;
  font-size: 0.875rem !important;
  padding: 9px 20px !important;
  transition: background-color var(--dur-fast) var(--ease),
              border-color var(--dur-fast) var(--ease),
              color var(--dur-fast) var(--ease) !important;
  box-shadow: none !important;
}
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-primaryFormSubmit"] {
  background: var(--blue) !important;
  color: #FFFFFF !important;
  border: 1px solid var(--blue) !important;
}
[data-testid="stBaseButton-primary"]:hover,
[data-testid="stBaseButton-primaryFormSubmit"]:hover {
  background: var(--blue-dark) !important;
  border-color: var(--blue-dark) !important;
  color: #FFFFFF !important;
}
[data-testid="stBaseButton-primary"]:active,
[data-testid="stBaseButton-primaryFormSubmit"]:active {
  transform: scale(0.98) !important;
}
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-secondaryFormSubmit"] {
  background: var(--surface) !important;
  color: var(--text) !important;
  border: 1px solid var(--hairline-2) !important;
}
[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stBaseButton-secondaryFormSubmit"]:hover {
  background: var(--raised) !important;
  border-color: var(--hairline-2) !important;
  color: var(--text) !important;
}
[data-testid="stBaseButton-secondary"]:active,
[data-testid="stBaseButton-secondaryFormSubmit"]:active {
  transform: scale(0.98) !important;
}

/* ══════════════════════════════════════════
   LANDING — NAVBAR (Pass 6: flat sticky bar, not a pill)
══════════════════════════════════════════ */
.st-key-landing_nav {
  position: sticky;
  top: 0;
  z-index: 999;
  width: 100%;
  background: rgba(247, 244, 238, 0.95);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--hairline);
  padding: 0 24px;
  box-sizing: border-box;
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
  min-height: 56px;
}
.st-key-landing_nav [data-testid="stColumn"] { display: flex; align-items: center; }
.st-key-landing_nav [data-testid="stElementContainer"],
.st-key-landing_nav [data-testid="stMarkdownContainer"] {
  margin: 0 !important;
  padding: 0 !important;
}
.st-key-landing_nav [data-testid^="stBaseButton"] {
  padding: 7px 16px !important;
  font-size: 0.8125rem !important;
  white-space: nowrap;
}
.st-key-landing_nav [data-testid="stMarkdownContainer"] p {
  margin: 0 !important;
  line-height: 1 !important;
}

/* Nav brand */
.fl-nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  line-height: 1;
}
.fl-nav-icon {
  width: 32px; height: 32px;
  background: var(--blue);
  border-radius: var(--r-sm);
  display: inline-flex; align-items: center; justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
}
.fl-nav-icon img {
  width: 22px; height: 22px;
  object-fit: contain;
  display: block;
}
/* Pass 5: logo wordmark — weight 600, no negative tracking at small size */
.fl-nav-name {
  font-size: 1rem; font-weight: 600; color: var(--text);
  white-space: nowrap;
  margin: 0;
  line-height: 1;
}
/* Location pill — quiet, no emoji */
.fl-loc-pill {
  display: inline-flex; align-items: center; gap: 5px;
  background: transparent;
  border: 1px solid var(--hairline-2);
  border-radius: var(--r-sm);
  padding: 4px 10px;
  font-size: 0.75rem; font-weight: 400; color: var(--text-2);
  white-space: nowrap;
}

/* ══════════════════════════════════════════
   LANDING — HERO (Pass 4+5: clean copy, weight 500)
══════════════════════════════════════════ */
.fl-hero { text-align: center; padding: 72px 24px 40px; }
/* Pass 2: remove status pill above headline — keep class as no-op */
.fl-status-pill { display: none; }

/* Pass 9: live status dot — only genuinely live element keeps a pulse */
.fl-status-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--emerald);
  animation: fl-live-pulse 2.4s ease-in-out infinite;
}
@keyframes fl-live-pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.4; }
}

/* Pass 5: hero headline — weight 500, tracking -0.02em at display size only */
.fl-hero h1 {
  font-size: clamp(36px, 5vw, 60px);
  font-weight: 500;
  line-height: 1.08;
  letter-spacing: -0.02em;
  color: var(--text);
  margin: 0 auto 20px;
  max-width: 820px;
}
.fl-hero h1 .accent { color: var(--blue); }
.fl-hero p {
  font-size: clamp(15px, 1.2vw, 17px);
  color: var(--text-2);
  max-width: 620px;
  margin: 0 auto;
  line-height: 1.65;
  font-weight: 400;
}

/* Hero CTA row */
.st-key-hero_cta { max-width: 480px; margin: 32px auto 0; }
.st-key-hero_cta [data-testid="stHorizontalBlock"] { justify-content: center; }
.st-key-hero_cta [data-testid^="stBaseButton"] {
  padding: 11px 28px !important;
  font-size: 0.9375rem !important;
  width: 100%;
}

/* ══════════════════════════════════════════
   LANDING — FEATURE GRID (Pass 8: replaces orbit hub)
══════════════════════════════════════════ */
.fl-features-section {
  max-width: 1100px;
  margin: 0 auto;
  padding: 56px 24px 0;
}
.fl-features-eyebrow {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--muted);
  letter-spacing: 0.04em;
  margin-bottom: 8px;
  text-align: center;
}
.fl-features-heading {
  font-size: 1.625rem;
  font-weight: 500;
  color: var(--text);
  letter-spacing: -0.01em;
  margin: 0 0 6px;
  text-align: center;
}
.fl-features-sub {
  color: var(--text-2);
  font-size: 0.9375rem;
  margin: 0 auto 36px;
  text-align: center;
  max-width: 540px;
  line-height: 1.6;
}
.fl-features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
.fl-feature-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 20px;
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: var(--r-card);
  box-shadow: var(--shadow-sm);
  transition: border-color var(--dur-fast) var(--ease);
}
.fl-feature-item:hover {
  border-color: var(--hairline-2);
}
.fl-feature-icon {
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  color: var(--blue);
  flex-shrink: 0;
  margin-top: 1px;
}
.fl-feature-text { display: flex; flex-direction: column; min-width: 0; }
.fl-feature-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text);
  margin: 0 0 3px;
  line-height: 1.3;
}
.fl-feature-desc {
  font-size: 0.8125rem;
  color: var(--text-2);
  margin: 0;
  line-height: 1.5;
}

/* ══════════════════════════════════════════
   LANDING — IMPACT STRIP + FOOTER
══════════════════════════════════════════ */
.fl-landing-strip {
  max-width: 1100px;
  margin: 48px auto 0;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding: 0 24px;
}
/* Pass 7: stat cards — number + label only, no accent stripe, no icon */
.fl-strip-card {
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: var(--r-card);
  padding: 20px 24px;
  box-shadow: var(--shadow-sm);
}
/* Pass 5: values — weight 500, tabular nums, tracking -0.01em */
.fl-strip-val {
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--text);
  letter-spacing: -0.01em;
  font-variant-numeric: tabular-nums;
  line-height: 1.1;
}
/* Pass 5: labels — sentence case, no uppercase tracking */
.fl-strip-lbl {
  font-size: 0.8125rem;
  font-weight: 400;
  color: var(--text-2);
  margin-top: 4px;
}
.fl-landing-footer {
  text-align: center;
  padding: 48px 24px 32px;
  color: var(--muted);
  font-size: 0.8125rem;
}

/* ══════════════════════════════════════════
   AUTH — SPLIT SCREEN
══════════════════════════════════════════ */
.st-key-auth_page { padding: 24px; }
.st-key-auth_page [data-testid="stHorizontalBlock"] { gap: 20px; align-items: stretch; }

/* Pass 2: dark panel — no color wash blobs (removed via ::before/::after removal) */
.st-key-auth_left {
  background: #1f1b16;
  border-radius: var(--r-panel);
  padding: 32px 36px;
  min-height: 740px;
  height: 100%;
  position: relative;
  overflow: hidden;
}
.st-key-auth_left [data-testid="stMarkdownContainer"] { position: relative; z-index: 1; }
.st-key-auth_left [data-testid^="stBaseButton"] {
  background: rgba(255, 255, 255, 0.07) !important;
  color: rgba(255, 255, 255, 0.75) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: var(--r-md) !important;
  font-size: 0.8125rem !important;
  padding: 7px 16px !important;
  width: auto !important;
}
.st-key-auth_left [data-testid^="stBaseButton"]:hover {
  background: rgba(255, 255, 255, 0.12) !important;
  color: #FFFFFF !important;
}

/* Auth brand row */
.fl-auth-brand-badge {
  display: inline-flex; align-items: center; gap: 10px;
  margin: 0 0 28px;
}
.fl-auth-brand-badge .icon {
  width: 32px; height: 32px;
  border-radius: var(--r-sm);
  background: var(--blue);
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.fl-auth-brand-badge .icon img { width: 22px; height: 22px; object-fit: contain; }
.fl-auth-brand-badge .name {
  font-size: 1rem; font-weight: 600; color: #FFFFFF;
}

/* Pass 5: auth headline — weight 500, specific to FoodLoop */
.fl-auth-headline {
  font-size: 1.75rem;
  font-weight: 500;
  color: #FFFFFF;
  line-height: 1.18;
  letter-spacing: -0.01em;
  margin-bottom: 8px;
}
.fl-auth-headline .accent { color: #93C5FD; }
.fl-auth-lead {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.6;
  margin-bottom: 24px;
}

/* Pass 3: auth feature list — SVG icons, no emoji */
.fl-auth-features {
  list-style: none;
  margin: 0 0 24px;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.fl-auth-feature {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.875rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.72);
}
.fl-auth-feature-icon {
  color: rgba(255, 255, 255, 0.4);
  flex-shrink: 0;
  display: flex;
}

.fl-auth-proof {
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.4);
  line-height: 1.6;
}
/* Pass 9: live pill — legitimate live indicator, keep subtle pulse */
.fl-live-pill {
  display: inline-flex; align-items: center; gap: 7px;
  margin-top: 16px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.25);
  border-radius: var(--r-sm);
  padding: 5px 12px;
  font-size: 0.75rem; font-weight: 500; color: #34D399;
}
.fl-live-pill .dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: #10B981;
  animation: fl-live-pulse 2s ease-in-out infinite;
}

/* Auth right form */
.st-key-auth_right {
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: var(--r-panel);
  padding: 40px 44px;
  min-height: 740px;
  box-shadow: var(--shadow-md);
  display: flex;
  flex-direction: column;
  justify-content: center;
}
/* Pass 5: form heading — weight 500, appropriate size */
.fl-form-heading {
  font-size: 1.5rem; font-weight: 500; color: var(--text);
  letter-spacing: -0.01em; margin: 0 0 6px;
}
.fl-form-sub { font-size: 0.875rem; color: var(--text-2); line-height: 1.55; margin: 0 0 20px; }
.fl-field-label {
  display: block;
  font-size: 0.8125rem; font-weight: 500; color: var(--text);
  margin: 0 0 4px;
}
.fl-link-row {
  text-align: center;
  font-size: 0.8125rem;
  color: var(--text-2);
  line-height: 1.5;
  margin: 0;
  padding: 14px 0 10px;
}
.fl-link-row b { color: var(--blue); font-weight: 500; }
.st-key-to_signup [data-testid="stButton"],
.st-key-to_login  [data-testid="stButton"] {
  margin-top: 16px;
}

/* Pass 7: role toggle pills → smaller radius, not full pills */
:is(.st-key-role_pills, .st-key-login_role_pills) [data-testid="stHorizontalBlock"] { gap: 8px; }
:is(.st-key-role_pills, .st-key-login_role_pills) [data-testid^="stBaseButton"] {
  width: 100%;
  font-size: 0.8125rem !important;
  padding: 8px 8px !important;
  border-radius: var(--r-sm) !important;
}

/* Pass 5: demo divider — sentence case, lighter */
.fl-demo-divider {
  display: flex; align-items: center; gap: 10px;
  margin: 20px 0 10px;
  font-size: 0.75rem; font-weight: 400; color: var(--muted);
}
.fl-demo-divider::before, .fl-demo-divider::after {
  content: ''; flex: 1; height: 1px; background: var(--hairline);
}
.st-key-demo_row [data-testid="stHorizontalBlock"] { gap: 8px; }
.st-key-demo_row [data-testid^="stBaseButton"] {
  width: 100%;
  font-size: 0.8125rem !important;
  padding: 7px 6px !important;
  border-radius: var(--r-sm) !important;
  white-space: nowrap;
}

/* ══════════════════════════════════════════
   DASHBOARD — NAVBAR (flat sticky bar)
══════════════════════════════════════════ */
.st-key-dash_nav {
  position: sticky;
  top: 0;
  z-index: 998;
  width: 100%;
  background: rgba(247, 244, 238, 0.95);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--hairline);
  padding: 0 28px;
  box-sizing: border-box;
}
.st-key-dash_nav [data-testid="stHorizontalBlock"] {
  align-items: center;
  gap: 8px;
  flex-wrap: nowrap;
  min-height: 56px;
}
.st-key-dash_nav [data-testid^="stBaseButton"] {
  padding: 6px 14px !important;
  font-size: 0.8125rem !important;
  white-space: nowrap;
}
.st-key-dash_nav [data-testid="stMarkdownContainer"] p { margin: 0 !important; }
.st-key-dash_nav [data-testid="stColumn"] { display: flex; align-items: center; }
.st-key-dash_nav [data-testid="stElementContainer"],
.st-key-dash_nav [data-testid="stMarkdownContainer"] {
  margin: 0 !important;
  padding: 0 !important;
}
/* Pass 5: dash user info — weight 500, no uppercase role tags */
.fl-dash-user {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin: 0;
  line-height: 1;
  min-height: 32px;
}
.fl-dash-name { font-size: 0.875rem; font-weight: 500; color: var(--text); }
.fl-verified {
  display: inline-flex; align-items: center; gap: 4px;
  background: rgba(22, 163, 74, 0.1); color: var(--green);
  border-radius: var(--r-sm); padding: 2px 8px;
  font-size: 0.6875rem; font-weight: 500;
}
/* Pass 5: role tag — sentence case, no uppercase tracking */
.fl-role-tag {
  display: inline-flex; align-items: center; gap: 4px;
  border-radius: var(--r-sm); padding: 2px 8px;
  font-size: 0.6875rem; font-weight: 500;
}
.fl-role-donor     { background: rgba(1, 75, 170, 0.08); color: var(--blue); }
.fl-role-recipient { background: rgba(16, 185, 129, 0.1); color: #047857; }
.fl-role-admin     { background: rgba(109, 40, 217, 0.08); color: #6D28D9; }

/* ══════════════════════════════════════════
   DASHBOARD — CONTENT
══════════════════════════════════════════ */
.fl-page-head { padding: 24px 4px 8px; }
/* Pass 5: page title — weight 500, appropriate scale */
.fl-page-title {
  font-size: 1.5rem; font-weight: 500; color: var(--text);
  letter-spacing: -0.01em; margin: 0;
}
.fl-page-sub { font-size: 0.875rem; color: var(--text-2); margin: 4px 0 0; line-height: 1.5; }

/* Pass 7: KPI strip — number + label only, no icon, no accent stripe */
.fl-kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(148px, 1fr));
  gap: 12px;
  margin: 12px 0 8px;
}
.fl-kpi {
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: var(--r-card);
  padding: 16px 20px;
  box-shadow: var(--shadow-sm);
}
/* Pass 2: remove gradient stripe — no ::before pseudo-element */
.fl-kpi-icon { display: none; }
/* Pass 5: KPI value — weight 500, tabular nums */
.fl-kpi-val {
  font-size: 1.5rem; font-weight: 500; color: var(--text);
  letter-spacing: -0.01em; line-height: 1.1;
  font-variant-numeric: tabular-nums;
}
.fl-kpi.urgent .fl-kpi-val { color: var(--coral); }
/* Pass 5: KPI label — sentence case, muted, no uppercase */
.fl-kpi-label {
  font-size: 0.75rem; font-weight: 400; color: var(--text-2);
  margin-top: 4px;
  line-height: 1.3;
}

/* Generic white card for HTML blocks */
.fl-card {
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: var(--r-card);
  padding: 20px 24px;
  box-shadow: var(--shadow-sm);
  margin: 8px 0;
}
/* Pass 5: card title — weight 500, sentence case */
.fl-card-title {
  font-size: 0.9375rem; font-weight: 500; color: var(--text);
  margin: 0 0 4px;
}
.fl-card-sub { font-size: 0.8125rem; color: var(--text-2); line-height: 1.55; margin: 0 0 14px; }

/* ══════════════════════════════════════════
   FOOD LISTING CARDS
══════════════════════════════════════════ */
.fl-food-card {
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-left: 3px solid var(--blue);
  border-radius: var(--r-card);
  padding: 16px 20px;
  box-shadow: var(--shadow-sm);
  margin: 8px 0;
  position: relative;
  overflow: hidden;
  /* Pass 9: hover = colour/border change, no translateY */
  transition: border-color var(--dur-fast) var(--ease),
              box-shadow var(--dur-fast) var(--ease);
}
.fl-food-card:hover {
  border-color: var(--hairline-2);
  box-shadow: var(--shadow-md);
}
.fl-food-card.urgent {
  border-left-color: var(--coral);
}
.fl-food-head {
  display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 6px;
}
.fl-food-name { font-size: 0.9375rem; font-weight: 500; color: var(--text); }
.fl-tag {
  display: inline-flex; align-items: center;
  border-radius: var(--r-sm); padding: 2px 8px;
  font-size: 0.6875rem; font-weight: 500;
}
.fl-tag-blue     { background: rgba(1, 75, 170, 0.08); color: var(--blue); }
.fl-tag-cooked   { background: rgba(194, 65, 12, 0.08); color: #C2410C; }
.fl-tag-bakery   { background: rgba(133, 77, 14, 0.08); color: #854D0E; }
.fl-tag-produce  { background: rgba(21, 128, 61, 0.08); color: #15803D; }
.fl-tag-dairy    { background: rgba(3, 105, 161, 0.08); color: #0369A1; }
.fl-tag-packaged { background: rgba(109, 40, 217, 0.08); color: #6D28D9; }
.fl-tag-beverages{ background: rgba(190, 24, 93, 0.08); color: #BE185D; }

/* Pass 3+5: urgent badge — no emoji, no uppercase, sentence case */
.fl-urgent-badge {
  display: inline-flex; align-items: center; gap: 4px;
  background: rgba(217, 56, 30, 0.07);
  border: 1px solid rgba(217, 56, 30, 0.2);
  color: var(--coral);
  border-radius: var(--r-sm);
  padding: 2px 8px;
  font-size: 0.6875rem; font-weight: 500;
}
/* Pass 9: remove pulsing animation on urgent badge text */
.fl-food-meta {
  font-size: 0.8125rem; color: var(--text-2);
  display: flex; gap: 12px; flex-wrap: wrap; margin-top: 4px;
  align-items: center;
}
.fl-food-meta b { color: var(--text); font-weight: 500; }
.fl-food-meta svg { opacity: 0.5; }

/* Pass 7: countdown text — no emoji */
.fl-countdown {
  font-size: 0.8125rem; font-weight: 400; color: var(--text-2); margin-top: 8px;
  display: flex; align-items: center; gap: 5px;
}
.fl-countdown.urgent { color: var(--coral); }

/* Signature: countdown bar — 3px drain bar at card bottom */
.fl-countdown-bar-wrap {
  height: 3px;
  background: var(--raised);
  margin: 10px -20px -16px;
  overflow: hidden;
  border-radius: 0 0 var(--r-card) var(--r-card);
}
.fl-countdown-bar {
  height: 100%;
  border-radius: 0 0 var(--r-card) var(--r-card);
}

/* ══════════════════════════════════════════
   REQUEST CARDS
══════════════════════════════════════════ */
.fl-req-card {
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-left: 3px solid var(--amber);
  border-radius: var(--r-card);
  padding: 14px 18px;
  box-shadow: var(--shadow-sm);
  margin: 6px 0;
}
.fl-req-card.approved  { border-left-color: var(--emerald); }
.fl-req-card.rejected  { border-left-color: var(--coral); }
.fl-req-card.completed { border-left-color: var(--muted); }
.fl-req-title { font-size: 0.9375rem; font-weight: 500; color: var(--text); }
.fl-req-meta { font-size: 0.8125rem; color: var(--text-2); margin-top: 4px; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.fl-req-meta svg { opacity: 0.5; }

/* Pass 5+7: status badges — sentence case, no uppercase tracking */
.fl-status {
  display: inline-flex; border-radius: var(--r-xs);
  padding: 2px 8px; font-size: 0.6875rem; font-weight: 500;
}
.fl-status-pending   { background: rgba(217, 119, 6, 0.1); color: #92400E; }
.fl-status-approved  { background: rgba(22, 163, 74, 0.1); color: #166534; }
.fl-status-completed { background: var(--raised); color: var(--text-2); }
.fl-status-rejected  { background: rgba(220, 38, 38, 0.08); color: #B91C1C; }

/* ══════════════════════════════════════════
   PIN TICKET (Pass 2+7: flat dark card, no gradient)
══════════════════════════════════════════ */
.fl-ticket {
  background: #1f1b16;
  border-radius: var(--r-panel);
  padding: 24px 24px 20px;
  margin: 10px 0;
  color: #FFFFFF;
  position: relative;
  box-shadow: var(--shadow-lg);
}
/* Pass 5: ticket label — sentence case, no uppercase */
.fl-ticket-label {
  font-size: 0.6875rem; font-weight: 500;
  color: rgba(255, 255, 255, 0.45);
  letter-spacing: 0.03em;
  display: flex; align-items: center; gap: 6px;
}
/* Pass 5: PIN digits — large mono, the visual centrepiece */
.fl-ticket-pin {
  font-family: 'Courier New', Courier, monospace;
  font-size: 2.75rem; font-weight: 700;
  letter-spacing: 0.28em;
  margin: 10px 0 6px;
  color: #FFFFFF;
  font-variant-numeric: tabular-nums;
}
.fl-ticket-food { font-size: 0.9375rem; font-weight: 500; color: rgba(255, 255, 255, 0.9); }
.fl-ticket-meta {
  font-size: 0.8125rem; color: rgba(255, 255, 255, 0.5);
  margin-top: 4px;
  display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
}
.fl-ticket-meta svg { opacity: 0.4; }
.fl-ticket-hint {
  margin-top: 14px;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--r-sm);
  padding: 8px 12px;
  font-size: 0.8125rem; font-weight: 400;
  color: rgba(255, 255, 255, 0.55);
}

/* ══════════════════════════════════════════
   EMPTY STATES
══════════════════════════════════════════ */
.fl-empty {
  background: var(--surface);
  border: 1px dashed var(--hairline-2);
  border-radius: var(--r-card);
  padding: 40px 24px;
  text-align: center;
  margin: 10px 0;
}
/* Pass 3: empty state icon → SVG, muted colour */
.fl-empty-icon {
  font-size: 1.25rem;
  color: var(--muted);
  margin-bottom: 8px;
  display: flex; justify-content: center;
}
.fl-empty-title { font-size: 0.9375rem; font-weight: 500; color: var(--text); margin-bottom: 4px; }
.fl-empty-sub { font-size: 0.8125rem; color: var(--text-2); }

/* ══════════════════════════════════════════
   ADMIN
══════════════════════════════════════════ */
.fl-user-row {
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: var(--r-card);
  padding: 12px 16px;
  margin: 6px 0;
  display: flex; align-items: center; justify-content: space-between;
  gap: 12px; flex-wrap: wrap;
  box-shadow: var(--shadow-sm);
}
.fl-user-name { font-size: 0.9rem; font-weight: 500; color: var(--text); }
.fl-user-meta { font-size: 0.75rem; color: var(--text-2); margin-top: 3px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.fl-user-meta svg { opacity: 0.4; }
/* Pass 7: verification badges — sentence case */
.fl-badge-ok   { background: rgba(22, 163, 74, 0.1); color: #166534; border-radius: var(--r-xs); padding: 2px 7px; font-size: 0.6875rem; font-weight: 500; }
.fl-badge-warn { background: rgba(217, 119, 6, 0.1); color: #92400E; border-radius: var(--r-xs); padding: 2px 7px; font-size: 0.6875rem; font-weight: 500; }

/* ══════════════════════════════════════════
   ANALYTICS
══════════════════════════════════════════ */
.fl-chart-card {
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: var(--r-card);
  padding: 16px 18px 10px;
  box-shadow: var(--shadow-sm);
  margin: 8px 0;
}
/* Pass 5: chart title — weight 500, sentence case */
.fl-chart-title {
  font-size: 0.875rem; font-weight: 500; color: var(--text); margin-bottom: 10px;
}

/* Pass 2+7: impact banner — flat dark card, no gradient */
.fl-impact-banner {
  background: #1f1b16;
  border-radius: var(--r-panel);
  padding: 28px 32px;
  color: #FFFFFF;
  margin: 12px 0;
  box-shadow: var(--shadow-lg);
}
/* Pass 5: impact labels — sentence case, no uppercase */
.fl-impact-label {
  font-size: 0.6875rem; font-weight: 500; color: rgba(255,255,255,0.45);
  letter-spacing: 0.03em; margin-bottom: 4px;
  display: flex; align-items: center; gap: 6px;
}
.fl-impact-value {
  font-size: 2.25rem; font-weight: 500; letter-spacing: -0.02em;
  margin: 4px 0 8px;
  font-variant-numeric: tabular-nums;
}
.fl-impact-stats { display: flex; gap: 28px; flex-wrap: wrap; margin-top: 12px; }
.fl-impact-stat b { display: block; font-size: 1.125rem; font-weight: 500; font-variant-numeric: tabular-nums; }
.fl-impact-stat span { font-size: 0.6875rem; color: rgba(255,255,255,0.45); }

/* ══════════════════════════════════════════
   PASS 2: STREAMLIT WIDGETS — hairline borders at rest
══════════════════════════════════════════ */
.stTextInput input, .stNumberInput input, .stTextArea textarea {
  border-radius: var(--r-md) !important;
  border: 1px solid var(--hairline-2) !important;
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  font-size: 0.875rem !important;
  color: var(--text) !important;
  background: var(--surface) !important;
  padding: 10px 13px !important;
  box-shadow: none !important;
  transition: border-color var(--dur-fast) var(--ease) !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 3px rgba(1, 75, 170, 0.1) !important;
  outline: none !important;
}
[data-baseweb="select"] > div,
[data-testid="stSelectbox"] .react-aria-ComboBox > div {
  border-radius: var(--r-md) !important;
  border: 1px solid var(--hairline-2) !important;
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  font-size: 0.875rem !important;
  background: var(--surface) !important;
  transition: border-color var(--dur-fast) var(--ease) !important;
}
[data-testid="stSelectbox"] .react-aria-ComboBox > div:focus-within {
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 3px rgba(1, 75, 170, 0.1) !important;
}
/* Pass 5: widget labels — weight 500, correct size */
.stTextInput label, .stNumberInput label, .stTextArea label,
.stSelectbox label, .stSlider label, .stFileUploader label {
  font-size: 0.8125rem !important;
  font-weight: 500 !important;
  color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
}
[data-testid="stWidgetLabel"] p { font-weight: 500 !important; font-size: 0.8125rem !important; }

/* ══════════════════════════════════════════
   TABS — Pass 7: underline indicator only
══════════════════════════════════════════ */
[data-testid="stTabs"] [data-baseweb="tab-list"],
[data-testid="stTabs"] [role="tablist"] {
  gap: 4px;
  border-bottom: 1px solid var(--hairline);
  background: transparent;
}
[data-testid="stTabs"] [data-testid="stTab"] {
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  font-weight: 400 !important;
  font-size: 0.875rem !important;
  color: var(--text-2) !important;
  padding: 9px 14px !important;
  border-bottom: 2px solid transparent !important;
  transition: color var(--dur-fast) var(--ease) !important;
}
[data-testid="stTabs"] [data-testid="stTab"] p,
[data-testid="stTabs"] [data-testid="stTab"] span,
[data-testid="stTabs"] [data-testid="stTab"] [data-testid="stMarkdownContainer"] {
  color: inherit !important;
  margin-bottom: 0 !important;
}
[data-testid="stTabs"] [data-testid="stTab"]:hover p,
[data-testid="stTabs"] [data-testid="stTab"]:hover span {
  color: var(--text) !important;
}
[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] {
  color: var(--text) !important;
  font-weight: 500 !important;
  border-bottom-color: var(--blue) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background: var(--blue) !important; }

/* Force headings to dark colour in all dashboard bodies */
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
.st-key-recipient_body h1, .st-key-recipient_body h2, .st-key-recipient_body h3,
.st-key-admin_body h1, .st-key-admin_body h2, .st-key-admin_body h3,
.st-key-analytics_body h1, .st-key-analytics_body h2, .st-key-analytics_body h3,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
  color: var(--text) !important;
}

[data-testid="stExpander"] {
  background: var(--surface) !important;
  border: 1px solid var(--hairline) !important;
  border-radius: var(--r-card) !important;
  box-shadow: var(--shadow-sm) !important;
  margin-bottom: 6px;
}
[data-testid="stExpander"] summary {
  font-weight: 500 !important;
  font-size: 0.875rem !important;
  color: var(--text) !important;
}

[data-testid="stForm"] {
  background: var(--surface);
  border: 1px solid var(--hairline) !important;
  border-radius: var(--r-card) !important;
  padding: 20px 22px !important;
  box-shadow: var(--shadow-sm);
}
[data-testid="stDataFrame"] {
  border-radius: var(--r-card) !important;
  overflow: hidden;
  border: 1px solid var(--hairline);
}
.stPlotlyChart { border-radius: var(--r-card) !important; overflow: hidden; }

[data-testid="stAlert"] { border-radius: var(--r-card) !important; font-size: 0.875rem !important; }

/* Scrollbar — warm tint */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--hairline-2); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(31, 27, 22, 0.24); }

/* Dashboard shells */
.st-key-donor_body,
.st-key-recipient_body,
.st-key-admin_body,
.st-key-analytics_body {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 28px 32px;
}
/* Chart containers */
.st-key-chart_weekly,
.st-key-chart_status,
.st-key-chart_category,
.st-key-chart_expiring {
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: var(--r-card);
  padding: 16px 18px 8px;
  box-shadow: var(--shadow-sm);
  margin: 4px 0;
  height: 100%;
}

/* Responsive */
@media (max-width: 980px) {
  .fl-features { grid-template-columns: 1fr; }
  .fl-landing-strip { grid-template-columns: 1fr; }
  .st-key-auth_left, .st-key-auth_right { min-height: auto; padding: 24px; }
}
@media (max-width: 640px) {
  .fl-hero h1 { letter-spacing: -0.01em; }
}
</style>
"""
