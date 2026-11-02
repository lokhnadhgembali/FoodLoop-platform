"""
styles.py  -  FoodLoop Global CSS (Modern SaaS UI)
Import get_css() in app.py and inject once via st.markdown.
"""


def get_css() -> str:
    return """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

/* ══════════════════════════════════════════
   RESET & ROOT VARIABLES
══════════════════════════════════════════ */
:root {
  --blue:       #014BAA;
  --blue2:      #0264E0;
  --blue-grad:  linear-gradient(135deg, #014BAA 0%, #0264E0 100%);
  --navy:       #06152D;
  --cream:      #F8F3F0;
  --white:      #FFFFFF;
  --coral:      #D9381E;
  --text:       #0F172A;
  --muted:      #475569;
  --slate:      #64748B;
  --border:     rgba(1, 75, 170, 0.08);
  --border-med: rgba(1, 75, 170, 0.15);
  --shadow-sm:  0 2px 8px rgba(1, 75, 170, 0.06);
  --shadow:     0 8px 30px rgba(1, 75, 170, 0.06);
  --shadow-lg:  0 20px 60px rgba(1, 75, 170, 0.12);
  --shadow-xl:  0 32px 80px rgba(1, 75, 170, 0.18);
  --radius-sm:  8px;
  --radius:     16px;
  --radius-lg:  24px;
  --radius-pill:999px;
}

/* ── Base reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  background: radial-gradient(circle at 50% 20%, #EFF6FF 0%, #F8F3F0 65%) !important;
  color: var(--text) !important;
  min-height: 100vh;
}

/* ── Kill default Streamlit chrome ── */
#MainMenu, footer, header { display: none !important; visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"]     { display: none !important; height: 0 !important; }
[data-testid="stSidebar"]    { display: none !important; }
.block-container {
  padding: 0 !important;
  max-width: 100% !important;
}

/* ══════════════════════════════════════════
   LANDING — FLOATING PILL NAVBAR
══════════════════════════════════════════ */
.fl-pill-nav {
  position: sticky;
  top: 16px;
  z-index: 1000;
  display: flex;
  justify-content: center;
  padding: 16px 24px 0;
  pointer-events: none;
}
.fl-pill-nav-inner {
  pointer-events: all;
  max-width: 1100px;
  width: 100%;
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: var(--radius-pill);
  border: 1px solid rgba(1,75,170,0.1);
  box-shadow: 0 4px 24px rgba(1,75,170,0.08), 0 1px 0 rgba(255,255,255,0.8) inset;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.fl-nav-brand-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}
.fl-nav-icon {
  width: 36px; height: 36px;
  background: var(--blue-grad);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
  box-shadow: 0 4px 12px rgba(1,75,170,0.3);
  flex-shrink: 0;
  overflow: hidden;
}
.fl-nav-icon img {
  width: 100%; height: 100%;
  object-fit: contain;
}
.fl-nav-brand-text {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--blue);
  letter-spacing: -0.3px;
}
.fl-nav-loc-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(1,75,170,0.05);
  border: 1px solid rgba(1,75,170,0.1);
  border-radius: var(--radius-pill);
  padding: 4px 12px;
  font-size: 0.73rem;
  font-weight: 600;
  color: var(--blue);
  white-space: nowrap;
}
.fl-nav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
.fl-btn-outline-pill {
  background: transparent;
  border: 1.5px solid rgba(1,75,170,0.3);
  border-radius: var(--radius-pill);
  color: var(--blue);
  font-size: 0.85rem;
  font-weight: 700;
  padding: 7px 22px;
  cursor: pointer;
  transition: all 0.18s ease;
  font-family: inherit;
}
.fl-btn-outline-pill:hover {
  background: rgba(1,75,170,0.05);
  border-color: var(--blue);
}
.fl-btn-solid-pill {
  background: var(--blue-grad);
  border: none;
  border-radius: var(--radius-pill);
  color: white;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 8px 22px;
  cursor: pointer;
  transition: all 0.18s ease;
  box-shadow: 0 4px 14px rgba(1,75,170,0.35);
  font-family: inherit;
}
.fl-btn-solid-pill:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(1,75,170,0.45);
}

/* ══════════════════════════════════════════
   LANDING — HERO SECTION
══════════════════════════════════════════ */
.fl-hero-wrap {
  max-width: 1100px;
  margin: 0 auto;
  padding: 72px 24px 48px;
  text-align: center;
}
.fl-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: white;
  border: 1px solid rgba(1,75,170,0.15);
  border-radius: var(--radius-pill);
  padding: 7px 18px;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--blue);
  margin-bottom: 28px;
  box-shadow: var(--shadow-sm);
  letter-spacing: 0.2px;
}
.fl-status-dot {
  width: 7px; height: 7px;
  background: #22c55e;
  border-radius: 50%;
  animation: blink 1.8s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1}50%{opacity:0.3} }

.fl-hero-headline {
  font-size: clamp(40px, 5.5vw, 64px);
  font-weight: 900;
  color: var(--text);
  line-height: 1.08;
  letter-spacing: -2px;
  margin-bottom: 20px;
}
.fl-hero-accent { color: var(--blue); }
.fl-hero-sub {
  font-size: clamp(15px, 1.3vw, 18px);
  color: var(--muted);
  max-width: 660px;
  margin: 0 auto 36px;
  line-height: 1.65;
  font-weight: 400;
}
.fl-hero-cta-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.fl-cta-primary {
  background: var(--blue-grad);
  color: white;
  border: none;
  border-radius: var(--radius-pill);
  padding: 14px 32px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 6px 24px rgba(1,75,170,0.4);
  transition: all 0.2s;
  font-family: inherit;
  display: inline-flex; align-items: center; gap: 8px;
}
.fl-cta-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 32px rgba(1,75,170,0.5); }
.fl-cta-secondary {
  background: white;
  color: var(--blue);
  border: 1.5px solid rgba(1,75,170,0.25);
  border-radius: var(--radius-pill);
  padding: 14px 32px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s;
  font-family: inherit;
}
.fl-cta-secondary:hover { background: rgba(1,75,170,0.03); border-color: var(--blue); }

/* ══════════════════════════════════════════
   LANDING — FEATURE CARDS & ORBITAL HUB
══════════════════════════════════════════ */
.fl-features-section {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px 80px;
}
.fl-features-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 24px;
  align-items: center;
}
.fl-feature-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 22px;
  box-shadow: var(--shadow);
  transition: all 0.25s ease;
}
.fl-feature-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: rgba(1,75,170,0.2);
}
.fl-feature-icon {
  width: 44px; height: 44px;
  background: linear-gradient(135deg, rgba(1,75,170,0.08) 0%, rgba(2,100,224,0.08) 100%);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px;
  margin-bottom: 12px;
  border: 1px solid rgba(1,75,170,0.1);
}
.fl-feature-title { font-size: 0.95rem; font-weight: 700; color: var(--text); margin-bottom: 5px; }
.fl-feature-desc  { font-size: 0.82rem; color: var(--muted); line-height: 1.5; }
.fl-feature-left  { display: flex; flex-direction: column; gap: 18px; }
.fl-feature-right { display: flex; flex-direction: column; gap: 18px; }

/* Orbital Hub */
.fl-orbital-hub {
  width: 220px;
  height: 220px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.fl-orbital-ring {
  position: absolute;
  border-radius: 50%;
  border: 1.5px solid rgba(1,75,170,0.12);
  top: 50%; left: 50%;
  transform: translate(-50%,-50%);
  animation: orbit-pulse 4s ease-in-out infinite;
}
.fl-orbital-ring:nth-child(1) { width: 70px;  height: 70px;  animation-delay: 0s; }
.fl-orbital-ring:nth-child(2) { width: 130px; height: 130px; animation-delay: 0.8s; }
.fl-orbital-ring:nth-child(3) { width: 190px; height: 190px; animation-delay: 1.6s; }
@keyframes orbit-pulse {
  0%,100%{ opacity:0.3; transform:translate(-50%,-50%) scale(1); }
  50%    { opacity:0.8; transform:translate(-50%,-50%) scale(1.04); }
}
.fl-orbital-center {
  position: relative;
  z-index: 2;
  width: 60px; height: 60px;
  background: var(--blue-grad);
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  font-size: 28px;
  box-shadow: 0 0 0 8px rgba(1,75,170,0.08), 0 0 40px rgba(1,75,170,0.3);
  overflow: hidden;
}
.fl-orbital-center img { width: 100%; height: 100%; object-fit: contain; }

/* ══════════════════════════════════════════
   AUTH — SPLIT SCREEN
══════════════════════════════════════════ */
.fl-auth-page {
  min-height: 100vh;
  display: flex;
}
.fl-auth-left {
  background: var(--navy);
  padding: 40px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  min-height: 100vh;
}
.fl-auth-left::before {
  content: '';
  position: absolute;
  top: -80px; left: -80px;
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(1,75,170,0.3) 0%, transparent 70%);
  border-radius: 50%;
}
.fl-auth-left::after {
  content: '';
  position: absolute;
  bottom: -60px; right: -60px;
  width: 250px; height: 250px;
  background: radial-gradient(circle, rgba(2,100,224,0.2) 0%, transparent 70%);
  border-radius: 50%;
}
.fl-auth-back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: var(--radius-pill);
  padding: 8px 16px;
  color: rgba(255,255,255,0.75);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 40px;
  transition: all 0.2s;
  font-family: inherit;
  position: relative; z-index: 1;
}
.fl-auth-back-btn:hover { background: rgba(255,255,255,0.12); color: white; }
.fl-auth-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 48px;
  position: relative; z-index: 1;
}
.fl-auth-brand-icon {
  width: 52px; height: 52px;
  background: var(--blue-grad);
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 26px;
  box-shadow: 0 8px 24px rgba(1,75,170,0.5);
  overflow: hidden;
  flex-shrink: 0;
}
.fl-auth-brand-icon img { width: 100%; height: 100%; object-fit: contain; }
.fl-auth-brand-name {
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
  letter-spacing: -0.3px;
}
.fl-auth-feature-pills {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: auto;
  position: relative; z-index: 1;
}
.fl-auth-pill {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: var(--radius-sm);
  padding: 14px 18px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(255,255,255,0.85);
  font-size: 0.85rem;
  font-weight: 500;
  backdrop-filter: blur(4px);
  transition: all 0.2s;
}
.fl-auth-pill:hover { background: rgba(255,255,255,0.09); border-color: rgba(255,255,255,0.18); }
.fl-auth-pill-icon { font-size: 18px; flex-shrink: 0; }
.fl-auth-social-proof {
  position: relative; z-index: 1;
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid rgba(255,255,255,0.08);
}
.fl-auth-proof-text {
  font-size: 0.82rem;
  color: rgba(255,255,255,0.5);
  line-height: 1.55;
  margin-bottom: 14px;
}
.fl-live-status {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: rgba(34,197,94,0.1);
  border: 1px solid rgba(34,197,94,0.25);
  border-radius: var(--radius-pill);
  padding: 6px 14px;
  font-size: 0.75rem;
  font-weight: 700;
  color: #4ade80;
}
.fl-live-dot {
  width: 6px; height: 6px;
  background: #22c55e;
  border-radius: 50%;
  animation: blink 1.5s infinite;
}
/* Auth Right Panel */
.fl-auth-right {
  background: white;
  padding: 48px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 100vh;
}
.fl-auth-heading {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text);
  margin-bottom: 6px;
  letter-spacing: -0.5px;
}
.fl-auth-subtext {
  font-size: 0.9rem;
  color: var(--muted);
  margin-bottom: 32px;
  line-height: 1.55;
}
.fl-form-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: 0.2px;
  display: block;
  margin-bottom: 6px;
}
.fl-role-pills {
  display: flex;
  gap: 10px;
  margin: 6px 0 20px;
  flex-wrap: wrap;
}
.fl-role-pill {
  flex: 1;
  min-width: 100px;
  padding: 10px 16px;
  border-radius: 12px;
  border: 1.5px solid var(--border-med);
  background: rgba(1,75,170,0.02);
  color: var(--muted);
  font-size: 0.83rem;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
  transition: all 0.18s;
  font-family: inherit;
}
.fl-role-pill:hover { border-color: var(--blue); color: var(--blue); background: rgba(1,75,170,0.04); }
.fl-role-pill.active {
  background: rgba(1,75,170,0.08);
  border-color: var(--blue);
  color: var(--blue);
  box-shadow: 0 0 0 3px rgba(1,75,170,0.08);
}
.fl-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 20px 0;
}
.fl-divider-line { flex: 1; height: 1px; background: rgba(0,0,0,0.08); }
.fl-divider-text { font-size: 0.72rem; font-weight: 700; color: var(--slate); letter-spacing: 1px; }
.fl-demo-btns {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.fl-demo-btn {
  flex: 1;
  min-width: 100px;
  padding: 10px 14px;
  border-radius: 10px;
  border: 1px solid var(--border-med);
  background: white;
  color: var(--text);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
  transition: all 0.18s;
  font-family: inherit;
}
.fl-demo-btn:hover {
  border-color: var(--blue);
  color: var(--blue);
  background: rgba(1,75,170,0.04);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}
.fl-auth-toggle {
  margin-top: 20px;
  text-align: center;
  font-size: 0.84rem;
  color: var(--muted);
}
.fl-auth-toggle a { color: var(--blue); font-weight: 700; cursor: pointer; }

/* ══════════════════════════════════════════
   DASHBOARD — TOP FLOATING NAVBAR
══════════════════════════════════════════ */
.fl-dash-nav {
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(1,75,170,0.08);
  padding: 12px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 500;
  box-shadow: 0 1px 20px rgba(1,75,170,0.06);
}
.fl-dash-brand {
  display: flex; align-items: center; gap: 10px;
  font-weight: 800; font-size: 1.15rem; color: var(--blue);
}
.fl-dash-brand-icon {
  width: 34px; height: 34px;
  background: var(--blue-grad);
  border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.fl-dash-brand-icon img { width: 100%; height: 100%; object-fit: contain; }
.fl-dash-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.fl-verified-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(34,197,94,0.1);
  border: 1px solid rgba(34,197,94,0.25);
  border-radius: var(--radius-pill);
  padding: 4px 12px;
  font-size: 0.73rem;
  font-weight: 700;
  color: #166534;
}
.fl-user-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(1,75,170,0.06);
  border: 1px solid rgba(1,75,170,0.12);
  border-radius: var(--radius-pill);
  padding: 6px 14px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--blue);
}
.fl-role-tag {
  display: inline-block;
  padding: 3px 10px;
  border-radius: var(--radius-pill);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.3px;
}
.fl-role-donor     { background: #eff6ff; color: #1d4ed8; }
.fl-role-recipient { background: #f0fdf4; color: #15803d; }
.fl-role-admin     { background: #fef2f2; color: #b91c1c; }

/* ══════════════════════════════════════════
   DASHBOARD — KPI STRIP
══════════════════════════════════════════ */
.fl-kpi-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  padding: 24px 32px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}
.fl-kpi-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
  transition: all 0.2s;
}
.fl-kpi-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--blue-grad);
  border-radius: var(--radius) var(--radius) 0 0;
}
.fl-kpi-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.fl-kpi-icon { font-size: 1.6rem; margin-bottom: 10px; }
.fl-kpi-val {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--blue);
  line-height: 1;
  margin-bottom: 4px;
}
.fl-kpi-label { font-size: 0.78rem; font-weight: 600; color: var(--muted); }
.fl-kpi-sub   { font-size: 0.7rem; color: #94a3b8; margin-top: 2px; }

/* ══════════════════════════════════════════
   DASHBOARD — CONTENT AREA
══════════════════════════════════════════ */
.fl-dash-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px 64px;
  width: 100%;
}
.fl-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-top: 8px;
}
.fl-section-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--text);
  letter-spacing: -0.3px;
}
.fl-section-sub { font-size: 0.83rem; color: var(--muted); margin-top: 2px; }

/* ── Food Listing Cards ── */
.fl-food-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow);
  margin-bottom: 14px;
  transition: all 0.2s;
}
.fl-food-card:hover { box-shadow: var(--shadow-lg); border-color: var(--border-med); }
.fl-food-card.urgent { border-color: rgba(217,56,30,0.3); border-width: 1.5px; }
.fl-cat-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 10px;
  border-radius: var(--radius-pill);
  font-size: 0.71rem;
  font-weight: 700;
  margin-bottom: 8px;
}
.fl-cat-Cooked   { background: #fff0eb; color: #c2410c; }
.fl-cat-Bakery   { background: #fefce8; color: #854d0e; }
.fl-cat-Produce  { background: #f0fdf4; color: #15803d; }
.fl-cat-Dairy    { background: #e0f2fe; color: #0369a1; }
.fl-cat-Packaged { background: #f5f3ff; color: #6d28d9; }
.fl-food-title { font-size: 1.05rem; font-weight: 700; color: var(--text); margin-bottom: 6px; }
.fl-food-meta  { font-size: 0.82rem; color: var(--muted); line-height: 1.8; }
.fl-urgent-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(217,56,30,0.1);
  border: 1px solid rgba(217,56,30,0.25);
  border-radius: var(--radius-pill);
  padding: 3px 10px;
  font-size: 0.71rem;
  font-weight: 800;
  color: var(--coral);
  float: right;
  animation: urgent-pulse 1.8s ease-in-out infinite;
}
@keyframes urgent-pulse { 0%,100%{opacity:1} 50%{opacity:0.55} }

/* ── PIN Pickup Ticket ── */
.fl-pin-ticket {
  background: linear-gradient(135deg, #011f4b 0%, #014BAA 50%, #0264E0 100%);
  border-radius: var(--radius-lg);
  padding: 32px;
  text-align: center;
  box-shadow: 0 12px 40px rgba(1,75,170,0.4);
  color: white;
  position: relative;
  overflow: hidden;
}
.fl-pin-ticket::before {
  content: '';
  position: absolute;
  top: -40px; right: -40px;
  width: 150px; height: 150px;
  background: rgba(255,255,255,0.05);
  border-radius: 50%;
}
.fl-pin-ticket-label {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  opacity: 0.7;
  margin-bottom: 12px;
  position: relative;
}
.fl-pin-ticket-number {
  font-size: 3.5rem;
  font-weight: 900;
  letter-spacing: 14px;
  font-family: 'Courier New', monospace;
  text-shadow: 0 4px 16px rgba(0,0,0,0.3);
  position: relative;
}
.fl-pin-ticket-hint {
  font-size: 0.75rem;
  opacity: 0.65;
  margin-top: 12px;
  position: relative;
}

/* ── Request Cards ── */
.fl-req-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px 18px;
  margin-bottom: 10px;
  box-shadow: var(--shadow);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.fl-req-info { flex: 1; }
.fl-req-name { font-size: 0.92rem; font-weight: 700; color: var(--text); }
.fl-req-meta { font-size: 0.78rem; color: var(--muted); margin-top: 3px; }
.fl-status-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: var(--radius-pill);
  font-size: 0.72rem;
  font-weight: 800;
  white-space: nowrap;
}
.fl-status-pending   { background: #fef9c3; color: #854d0e; }
.fl-status-approved  { background: #eff6ff; color: #1d4ed8; }
.fl-status-completed { background: #f0fdf4; color: #15803d; }
.fl-status-rejected  { background: #fef2f2; color: #b91c1c; }

/* ══════════════════════════════════════════
   ANALYTICS
══════════════════════════════════════════ */
.fl-analytics-wrap {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px 32px 64px;
}
.fl-analytics-kpi {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}
@media (max-width: 900px) { .fl-analytics-kpi { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 500px) { .fl-analytics-kpi { grid-template-columns: 1fr; } }
.fl-impact-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  border-radius: var(--radius-pill);
  font-size: 0.83rem;
  font-weight: 700;
}
.fl-chip-blue  { background: #eff6ff; color: #1d4ed8; }
.fl-chip-green { background: #f0fdf4; color: #15803d; }
.fl-chip-amber { background: #fefce8; color: #854d0e; }

/* ══════════════════════════════════════════
   COMMON — FORMS & INPUTS
══════════════════════════════════════════ */
.stTextInput > div > div > input,
.stTextArea > div > textarea,
.stNumberInput > div > div > input,
.stSelectbox > div > div[data-baseweb="select"] > div {
  border-radius: 12px !important;
  border: 1.5px solid rgba(1,75,170,0.15) !important;
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  font-size: 0.9rem !important;
  color: var(--text) !important;
  background: white !important;
  transition: border-color 0.18s !important;
  padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > textarea:focus {
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 3px rgba(1,75,170,0.08) !important;
  outline: none !important;
}
.stTextInput > label, .stSelectbox > label,
.stTextArea > label, .stNumberInput > label,
.stSlider > label {
  font-size: 0.82rem !important;
  font-weight: 700 !important;
  color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  letter-spacing: 0.2px !important;
}

/* ── Streamlit Buttons → styled as our design ── */
.stButton > button {
  background: var(--blue-grad) !important;
  color: white !important;
  border: none !important;
  border-radius: 12px !important;
  font-weight: 700 !important;
  font-size: 0.88rem !important;
  padding: 10px 22px !important;
  transition: all 0.18s !important;
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  box-shadow: 0 4px 14px rgba(1,75,170,0.3) !important;
}
.stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 22px rgba(1,75,170,0.42) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tab"] {
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.88rem !important;
  color: var(--muted) !important;
  padding: 10px 20px !important;
  border-radius: 10px 10px 0 0 !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--blue) !important;
  border-bottom: 2.5px solid var(--blue) !important;
}

/* ══════════════════════════════════════════
   COMMON — ALERTS
══════════════════════════════════════════ */
.fl-alert-success {
  background: #f0fdf4;
  border: 1px solid rgba(34,197,94,0.3);
  border-left: 4px solid #22c55e;
  border-radius: 0 12px 12px 0;
  padding: 14px 18px;
  color: #14532d;
  font-size: 0.87rem;
  font-weight: 500;
  margin: 10px 0;
}
.fl-alert-error {
  background: #fef2f2;
  border: 1px solid rgba(217,56,30,0.2);
  border-left: 4px solid var(--coral);
  border-radius: 0 12px 12px 0;
  padding: 14px 18px;
  color: #7f1d1d;
  font-size: 0.87rem;
  font-weight: 500;
  margin: 10px 0;
}
.fl-alert-info {
  background: #eff6ff;
  border: 1px solid rgba(1,75,170,0.15);
  border-left: 4px solid var(--blue);
  border-radius: 0 12px 12px 0;
  padding: 14px 18px;
  color: #1e3a8a;
  font-size: 0.87rem;
  font-weight: 500;
  margin: 10px 0;
}

/* ══════════════════════════════════════════
   ADMIN — USER CARDS
══════════════════════════════════════════ */
.fl-admin-user-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px 20px;
  box-shadow: var(--shadow);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.fl-admin-user-info { flex: 1; }
.fl-admin-user-name { font-size: 0.95rem; font-weight: 700; color: var(--text); }
.fl-admin-user-meta { font-size: 0.78rem; color: var(--muted); margin-top: 4px; }

/* ══════════════════════════════════════════
   SCROLLBAR
══════════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(1,75,170,0.2); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(1,75,170,0.35); }

/* ── Plotly chart containers ── */
.stPlotlyChart { border-radius: var(--radius) !important; overflow: hidden; }
[data-testid="stDataFrame"] { border-radius: var(--radius) !important; overflow: hidden; }
</style>
"""

