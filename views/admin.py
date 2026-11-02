"""
views/admin.py  –  FoodLoop Admin Panel
Restricted to admin users only.
"""
import streamlit as st
import pandas as pd
import database
from utils import fmt_kg, fmt_num, export_history_csv

BLUE  = "#014BAA"
CORAL = "#D9381E"
CREAM = "#F8F3F0"
NAVY  = "#06152D"


def _kpi_card(col, icon: str, label: str, value: str, color: str = BLUE) -> None:
    col.markdown(f"""
    <div style="background:white;border-radius:16px;border:1px solid rgba(1,75,170,0.08);
         box-shadow:0 8px 30px rgba(1,75,170,0.06);padding:20px;text-align:center;margin:4px;">
      <div style="font-size:1.6rem;margin-bottom:6px;">{icon}</div>
      <div style="font-size:1.5rem;font-weight:900;color:{color};">{value}</div>
      <div style="font-size:0.78rem;font-weight:600;color:#64748B;margin-top:4px;">{label}</div>
    </div>""", unsafe_allow_html=True)


def render() -> None:
    # ── Page Header ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="padding:24px 32px 8px;">
      <h1 style="font-size:2rem;font-weight:900;color:{NAVY};margin:0;">🛡️ Admin Panel</h1>
      <p style="color:#64748B;margin-top:4px;">Manage users, monitor platform activity, and export data.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Admin KPI Strip ───────────────────────────────────────────────────────
    try:
        stats = database.get_platform_stats()
    except Exception as exc:
        st.error(f"Failed to load platform stats: {exc}")
        stats = {}

    kc1, kc2, kc3, kc4 = st.columns(4)
    _kpi_card(kc1, "👥", "Total Users",        fmt_num(stats.get("total_users", 0)),        BLUE)
    _kpi_card(kc2, "📦", "Active Listings",    str(stats.get("active_listings", 0)),         "#7C3AED")
    _kpi_card(kc3, "📋", "Total Requests",     str(stats.get("total_requests", 0)),          "#059669")
    _kpi_card(kc4, "✅", "Completed Pickups",  str(stats.get("completed_pickups", 0)),       "#D97706")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab_users, tab_monitor, tab_export = st.tabs([
        "👥 User Management",
        "📋 Platform Monitor",
        "📤 Export Data",
    ])

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 1 – User Management
    # ═════════════════════════════════════════════════════════════════════════
    with tab_users:
        st.markdown("### 👥 User Management")

        try:
            users = database.get_all_users()
        except Exception as exc:
            st.error(f"Could not load users: {exc}")
            users = []

        if not users:
            st.info("No users found.")
        else:
            # Role filter
            roles = ["All"] + sorted({u.get("role", "Unknown") for u in users})
            selected_role = st.selectbox("Filter by Role", roles, key="admin_role_filter")

            filtered = (
                users if selected_role == "All"
                else [u for u in users if u.get("role") == selected_role]
            )

            st.markdown(f"**{len(filtered)} user(s) shown**")

            for user in filtered:
                uid        = user.get("id") or user.get("user_id")
                name       = user.get("name", "N/A")
                email      = user.get("email", "N/A")
                role       = user.get("role", "N/A")
                verified   = bool(user.get("is_verified", False))
                badge_col  = "#059669" if verified else "#D97706"
                badge_text = "✅ Verified" if verified else "⏳ Unverified"

                with st.container():
                    col_info, col_btn = st.columns([5, 1])
                    with col_info:
                        st.markdown(f"""
                        <div style="background:white;border:1px solid #E2E8F0;border-radius:12px;
                             padding:14px 18px;margin-bottom:8px;">
                          <span style="font-weight:700;color:{NAVY};">{name}</span>
                          &nbsp;·&nbsp;
                          <span style="color:#64748B;font-size:0.85rem;">{email}</span>
                          &nbsp;·&nbsp;
                          <span style="background:{BLUE}22;color:{BLUE};border-radius:6px;
                               padding:2px 8px;font-size:0.8rem;font-weight:600;">{role}</span>
                          &nbsp;
                          <span style="background:{badge_col}22;color:{badge_col};border-radius:6px;
                               padding:2px 8px;font-size:0.8rem;font-weight:600;">{badge_text}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_btn:
                        btn_label = "Revoke" if verified else "Verify"
                        btn_color = CORAL if verified else "#059669"
                        if st.button(btn_label, key=f"toggle_{uid}",
                                     help=f"{'Revoke verification for' if verified else 'Verify'} {name}"):
                            try:
                                database.toggle_user_verification(uid, not verified)
                                st.success(f"{'Revoked' if verified else 'Verified'} {name}.")
                                st.rerun()
                            except Exception as exc:
                                st.error(f"Action failed: {exc}")

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 2 – Platform Monitor
    # ═════════════════════════════════════════════════════════════════════════
    with tab_monitor:
        st.markdown("### 📋 Platform Monitor")

        # ── Listings ─────────────────────────────────────────────────────────
        st.markdown("#### 📦 All Listings")
        try:
            listings = database.get_all_listings()
        except Exception as exc:
            st.error(f"Could not load listings: {exc}")
            listings = []

        if listings:
            df_listings = pd.DataFrame(listings)
            # Friendly column display
            col_cfg: dict = {}
            if "quantity_kg" in df_listings.columns:
                col_cfg["quantity_kg"] = st.column_config.NumberColumn("Qty (kg)", format="%.1f kg")
            if "is_active" in df_listings.columns:
                col_cfg["is_active"] = st.column_config.CheckboxColumn("Active")
            if "pickup_deadline" in df_listings.columns:
                col_cfg["pickup_deadline"] = st.column_config.TextColumn("Pickup Deadline")

            st.dataframe(df_listings, use_container_width=True, hide_index=True,
                         column_config=col_cfg)

            # Quick-action: cancel a listing
            with st.expander("⚠️ Cancel a Listing"):
                listing_ids = [str(row.get("id") or row.get("listing_id", "")) for row in listings]
                sel_id = st.selectbox("Select Listing ID to cancel", listing_ids,
                                      key="cancel_listing_sel")
                if st.button("Cancel Listing", key="cancel_listing_btn"):
                    try:
                        database.cancel_listing(int(sel_id))
                        st.success(f"Listing {sel_id} cancelled.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Cancel failed: {exc}")
        else:
            st.info("No listings found.")

        st.divider()

        # ── Requests ─────────────────────────────────────────────────────────
        st.markdown("#### 📋 All Requests")
        try:
            requests = database.get_all_requests()
        except Exception as exc:
            st.error(f"Could not load requests: {exc}")
            requests = []

        if requests:
            df_req = pd.DataFrame(requests)
            req_col_cfg: dict = {}
            if "status" in df_req.columns:
                req_col_cfg["status"] = st.column_config.TextColumn("Status")
            if "requested_at" in df_req.columns:
                req_col_cfg["requested_at"] = st.column_config.TextColumn("Requested At")

            st.dataframe(df_req, use_container_width=True, hide_index=True,
                         column_config=req_col_cfg)

            # Quick-actions: approve / reject
            with st.expander("✅ Approve / ❌ Reject a Request"):
                req_ids = [str(row.get("id") or row.get("request_id", "")) for row in requests]
                sel_req = st.selectbox("Select Request ID", req_ids, key="req_action_sel")
                col_approve, col_reject = st.columns(2)
                with col_approve:
                    if st.button("Approve", key="approve_req_btn"):
                        try:
                            database.approve_request(int(sel_req))
                            st.success(f"Request {sel_req} approved.")
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Approve failed: {exc}")
                with col_reject:
                    if st.button("Reject", key="reject_req_btn"):
                        try:
                            database.reject_request(int(sel_req))
                            st.warning(f"Request {sel_req} rejected.")
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Reject failed: {exc}")
        else:
            st.info("No requests found.")

        st.divider()

        # ── Summary Stats ────────────────────────────────────────────────────
        st.markdown("#### 📊 Quick Stats")
        active_count = sum(1 for r in listings if r.get("is_active", False)) if listings else 0
        completed    = stats.get("completed_pickups", 0)

        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.metric("Total Listings",    len(listings))
        sc2.metric("Active Listings",   active_count)
        sc3.metric("Total Requests",    len(requests))
        sc4.metric("Completed Pickups", completed)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 3 – Export Data
    # ═════════════════════════════════════════════════════════════════════════
    with tab_export:
        st.markdown("### 📤 Export Data")
        st.markdown(
            "Download the full donation history as a CSV file. "
            "This includes all completed and cancelled transactions."
        )

        try:
            history = database.get_all_history()
            csv_content = export_history_csv(history)

            st.download_button(
                label="⬇️ Download Donation History CSV",
                data=csv_content,
                file_name="foodloop_donation_history.csv",
                mime="text/csv",
                use_container_width=True,
            )

            if history:
                st.markdown(f"**{len(history)} record(s)** available for export.")
                with st.expander("👁️ Preview (first 20 rows)"):
                    df_hist = pd.DataFrame(history[:20])
                    st.dataframe(df_hist, use_container_width=True, hide_index=True)
            else:
                st.info("No history records found.")

        except Exception as exc:
            st.error(f"Export failed: {exc}")
