"""
views/admin.py  -  FoodLoop Admin Control Center
Role: admin
"""
import streamlit as st
import pandas as pd
import database
from utils import fmt_kg, fmt_num, format_countdown, export_history_csv

ROLE_LABELS = {"donor": "Donor", "recipient": "NGO", "admin": "Admin"}


def _sid(doc) -> str:
    return str(doc.get("_id", ""))


def _kpi_strip(users, listings, requests, stats):
    verified = sum(1 for u in users if u.get("is_verified"))
    active = sum(1 for l in listings if l.get("status") == "available")
    pending = sum(1 for r in requests if r.get("status") == "pending")

    cards = [
        ("🏫", fmt_num(len(users)),                        "Organizations"),
        ("🛡️", fmt_num(verified),                           "Verified Accounts"),
        ("📦", fmt_num(active),                             "Active Listings"),
        ("📬", fmt_num(pending),                            "Pending Claims"),
        ("✅", fmt_num(stats.get("completed_pickups", 0)),  "Completed Pickups"),
    ]
    html = "".join(
        f'<div class="fl-kpi"><div class="fl-kpi-icon">{icon}</div>'
        f'<div class="fl-kpi-val">{val}</div>'
        f'<div class="fl-kpi-label">{label}</div></div>'
        for icon, val, label in cards
    )
    st.markdown(f'<div class="fl-kpi-grid">{html}</div>', unsafe_allow_html=True)


# ── Verification ────────────────────────────────────────────────────────────
def _verification_tab(users):
    st.markdown("""
    <div class="fl-card-title">🛡️ Organization Verification</div>
    <div class="fl-card-sub">
      Only verified donors and NGOs should transact. Verify new organizations after checking
      their details, or revoke access if something looks wrong.
    </div>
    """, unsafe_allow_html=True)

    role_filter = st.selectbox(
        "Filter by account type",
        ["All", "donor", "recipient", "admin"],
        format_func=lambda r: "All accounts" if r == "All" else ROLE_LABELS.get(r, r),
        key="admin_role_filter",
    )
    filtered = users if role_filter == "All" else [u for u in users if u.get("role") == role_filter]

    if not filtered:
        st.info("No accounts match this filter.")
        return

    for user in filtered:
        uid = _sid(user)
        verified = bool(user.get("is_verified"))
        role = user.get("role", "donor")
        badge = (
            '<span class="fl-badge-ok">VERIFIED</span>' if verified
            else '<span class="fl-badge-warn">PENDING</span>'
        )
        st.markdown(f"""
        <div class="fl-user-row">
          <div>
            <div class="fl-user-name">{user.get('name', 'Unknown')} &nbsp;{badge}
              <span class="fl-role-tag fl-role-{'recipient' if role == 'recipient' else role}">
                {ROLE_LABELS.get(role, role)}
              </span>
            </div>
            <div class="fl-user-meta">
              {user.get('email', '')} &nbsp;·&nbsp; 📍 {user.get('address') or '—'}
              &nbsp;·&nbsp; 🏅 {fmt_num(user.get('reward_points', 0) or 0)} pts
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        ca, _, _ = st.columns([1.3, 1, 4])
        with ca:
            label = "Revoke verification" if verified else "Verify organization"
            if st.button(label, key=f"verify_{uid}", use_container_width=True,
                         type="secondary" if verified else "primary"):
                try:
                    database.toggle_user_verification(uid, not verified)
                except Exception as exc:
                    st.error(f"Could not update verification: {exc}")
                else:
                    st.rerun()


# ── Health monitor ──────────────────────────────────────────────────────────
def _health_tab(listings, requests):
    st.markdown("""
    <div class="fl-card-title">❤️ Platform Health &amp; Expiry Monitor</div>
    <div class="fl-card-sub">
      Run the expiry sweep to close listings past their safe pickup window, then audit live
      listings and every claim on the platform.
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 2])
    with c1:
        if st.button("⏱️ Trigger auto-expiry sweep", key="expiry_sweep",
                     use_container_width=True, type="primary"):
            try:
                expired = database.expire_old_listings()
            except Exception as exc:
                st.error(f"Expiry sweep failed: {exc}")
            else:
                st.success(f"Sweep complete — {expired} listing(s) marked expired.")
    with c2:
        try:
            expiring = database.get_expiring_listings(hours=6)
        except Exception:
            expiring = []
        st.markdown(
            f'<div class="fl-card-sub" style="margin:8px 0 0;">'
            f'<b>{len(expiring)}</b> available listing(s) expire within 6 hours.</div>',
            unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.markdown('<div class="fl-card-title" style="font-size:0.9rem;">📦 Live &amp; Recent Listings</div>',
                unsafe_allow_html=True)
    if listings:
        df_listings = pd.DataFrame([{
            "Food":       l.get("food_name", ""),
            "Category":   l.get("category", ""),
            "Donor":      l.get("donor_name", ""),
            "Remaining":  round(float(l.get("remaining_qty_kg", 0) or 0), 1),
            "Status":     l.get("status", ""),
            "Location":   l.get("location", ""),
            "Time Left":  format_countdown(l.get("pickup_deadline")),
        } for l in listings])
        st.dataframe(df_listings, use_container_width=True, hide_index=True)
    else:
        st.info("No listings on the platform yet.")

    st.markdown('<div class="fl-card-title" style="font-size:0.9rem;">📬 Transaction Audit</div>',
                unsafe_allow_html=True)
    if requests:
        df_reqs = pd.DataFrame([{
            "Food":       r.get("food_name", ""),
            "NGO":        r.get("recipient_name", ""),
            "Donor":      r.get("donor_name", ""),
            "Qty (kg)":   round(float(r.get("requested_qty_kg", 0) or 0), 1),
            "Status":     r.get("status", ""),
            "PIN Issued": bool(r.get("pickup_pin")),
        } for r in requests])
        st.dataframe(df_reqs, use_container_width=True, hide_index=True)
    else:
        st.info("No claims recorded yet.")


# ── Export ──────────────────────────────────────────────────────────────────
def _export_tab():
    st.markdown("""
    <div class="fl-card-title">📤 Export Donation History</div>
    <div class="fl-card-sub">
      Download the full audit trail of completed donations for SDG-12 reporting and compliance.
    </div>
    """, unsafe_allow_html=True)

    try:
        history = database.get_all_history() or []
    except Exception as exc:
        st.error(f"Could not load donation history: {exc}")
        return

    if not history:
        st.info("No completed donations recorded yet.")
        return

    csv_data = export_history_csv(history)
    total_kg = sum(float(h.get("quantity_kg", 0) or 0) for h in history)
    st.markdown(
        f'<div class="fl-card-sub" style="margin-bottom:14px;">'
        f'<b>{len(history)}</b> completed donations · <b>{fmt_kg(total_kg)}</b> redistributed.</div>',
        unsafe_allow_html=True)

    st.download_button(
        "⬇️ Download donation_history.csv",
        data=csv_data,
        file_name="foodloop_donation_history.csv",
        mime="text/csv",
        use_container_width=True,
        type="primary",
    )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown("**Latest 20 records**")
    df = pd.DataFrame(history[:20])
    df = df.drop(columns=[c for c in ("_id",) if c in df.columns])
    st.dataframe(df, use_container_width=True, hide_index=True)


# ── Render ──────────────────────────────────────────────────────────────────
def render():
    try:
        users = database.get_all_users() or []
        listings = database.get_all_listings() or []
        requests = database.get_all_requests() or []
        stats = database.get_platform_stats() or {}
    except Exception as exc:
        st.error(f"Could not load admin data: {exc}")
        users, listings, requests, stats = [], [], [], {}

    st.markdown(f"""
    <div class="fl-page-head fl-wrap-wide">
      <h1 class="fl-page-title">🛡️ Admin Control Center</h1>
      <p class="fl-page-sub">
        {st.session_state.get('user_name', 'Administrator')}, verify organizations,
        monitor expiries and audit every transaction.
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(key="admin_body"):
        _kpi_strip(users, listings, requests, stats)

        tab_verify, tab_health, tab_export = st.tabs(
            ["🛡️ Verification", "❤️ Platform Health", "📤 Audit & Export"]
        )
        with tab_verify:
            with st.container(key="admin_verify"):
                _verification_tab(users)
        with tab_health:
            with st.container(key="admin_health"):
                _health_tab(listings, requests)
        with tab_export:
            with st.container(key="admin_export"):
                _export_tab()

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
