"""
FoodLoop – Donor Dashboard
"""

import streamlit as st
import database
from utils import fmt_kg, fmt_num, format_countdown, is_urgent

# ── colour palette ──────────────────────────────────────────────────────────
BLUE   = "#014BAA"
CREAM  = "#F8F3F0"
CORAL  = "#D9381E"
WHITE  = "#FFFFFF"

# ── helpers ─────────────────────────────────────────────────────────────────

def _card(body: str, border_color: str = BLUE) -> None:
    st.markdown(
        f"""
        <div style="background:{WHITE};border-left:4px solid {border_color};
                    border-radius:8px;padding:16px 20px;margin-bottom:12px;
                    box-shadow:0 1px 4px rgba(0,0,0,.08);">
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _badge(label: str, color: str = BLUE) -> str:
    return (
        f'<span style="background:{color};color:#fff;border-radius:4px;'
        f'padding:2px 8px;font-size:0.75rem;font-weight:600;">{label}</span>'
    )


STATUS_COLORS = {
    "pending":   "#F59E0B",
    "approved":  "#10B981",
    "rejected":  CORAL,
    "completed": "#6B7280",
}


# ── KPI strip ───────────────────────────────────────────────────────────────

def _render_kpis(donor_name: str) -> None:
    stats = {}
    try:
        stats = database.get_platform_stats() or {}
    except Exception:
        pass

    listings = []
    try:
        listings = database.get_donor_listings(donor_name) or []
    except Exception:
        pass

    requests = []
    try:
        requests = database.get_requests_for_donor(donor_name) or []
    except Exception:
        pass

    active      = sum(1 for l in listings if l.get("status") == "available")
    pending_req = sum(1 for r in requests if r.get("status") == "pending")
    completed   = sum(1 for r in requests if r.get("status") == "completed")
    total_kg    = sum(l.get("quantity_kg", 0) for l in listings)

    cols = st.columns(4)
    kpis = [
        ("📦", "Active Listings",    fmt_num(active)),
        ("📬", "Pending Requests",   fmt_num(pending_req)),
        ("✅", "Completed Pickups",  fmt_num(completed)),
        ("⚖️", "Total kg Donated",   fmt_kg(total_kg)),
    ]
    for col, (icon, label, value) in zip(cols, kpis):
        with col:
            st.markdown(
                f"""
                <div style="background:{BLUE};color:#fff;border-radius:10px;
                            padding:16px;text-align:center;">
                    <div style="font-size:1.6rem;">{icon}</div>
                    <div style="font-size:1.4rem;font-weight:700;">{value}</div>
                    <div style="font-size:0.75rem;opacity:.85;">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ── Tab 1 – Publish Surplus ─────────────────────────────────────────────────

def _tab_publish() -> None:
    st.subheader("Publish New Surplus")
    with st.form("publish_form", clear_on_submit=True):
        food_name    = st.text_input("Food Name *", placeholder="e.g. Dal Makhani")
        category     = st.selectbox(
            "Category *",
            ["Cooked Meals", "Bakery", "Produce", "Packaged", "Beverages"],
        )
        col1, col2 = st.columns(2)
        with col1:
            quantity_kg  = st.number_input("Quantity (kg) *", min_value=0.5, step=0.5, value=1.0)
        with col2:
            servings     = st.number_input("Servings *", min_value=1, step=1, value=4)
        storage_note = st.text_input("Storage Note (optional)", placeholder="e.g. Keep refrigerated")
        safe_hours   = st.slider("Safe for (hours) *", min_value=1, max_value=48, value=6)
        location     = st.text_input("Location *", value="Punjab, India")

        submitted = st.form_submit_button("🚀 Publish Listing", use_container_width=True)

    if submitted:
        if not food_name.strip():
            st.error("Please enter a food name.")
            return
        if not location.strip():
            st.error("Please enter a location.")
            return
        try:
            database.add_listing(
                donor_name   = st.session_state.get("user_name", ""),
                food_name    = food_name.strip(),
                category     = category,
                quantity_kg  = quantity_kg,
                servings     = int(servings),
                storage_note = storage_note.strip(),
                safe_hours   = safe_hours,
                location     = location.strip(),
                donor_id     = st.session_state.get("user_id", ""),
            )
            st.success(f"✅ '{food_name}' listed successfully! NGOs can now claim it.")
        except Exception as exc:
            st.error(f"Failed to publish listing: {exc}")


# ── Tab 2 – Incoming Requests ────────────────────────────────────────────────

def _tab_requests(donor_name: str) -> None:
    st.subheader("Incoming Requests")

    requests = []
    try:
        requests = database.get_requests_for_donor(donor_name) or []
    except Exception as exc:
        st.error(f"Could not load requests: {exc}")
        return

    if not requests:
        st.info("No requests yet. Publish surplus to attract NGOs!")
        return

    for req in requests:
        req_id      = req.get("id") or req.get("request_id")
        food_name   = req.get("food_name", "Unknown Food")
        requester   = req.get("recipient_name", "Unknown NGO")
        qty         = req.get("quantity_kg", 0)
        status      = req.get("status", "pending").lower()
        pin         = req.get("pin") or req.get("pickup_pin")
        badge_color = STATUS_COLORS.get(status, BLUE)

        body = (
            f"<b>{food_name}</b> &nbsp; {_badge(status.upper(), badge_color)}<br>"
            f"<span style='color:#555;font-size:.9rem;'>Requester: <b>{requester}</b> &nbsp;|&nbsp; "
            f"Qty: <b>{fmt_kg(qty)}</b></span>"
        )

        if status == "approved" and pin:
            body += (
                f"<br><div style='margin-top:8px;background:{CREAM};border-radius:6px;"
                f"padding:8px 12px;display:inline-block;'>"
                f"🔑 Pickup PIN: <span style='font-family:monospace;font-size:1.2rem;"
                f"font-weight:700;color:{BLUE};'>{pin}</span></div>"
            )

        _card(body, border_color=badge_color)

        if status == "pending" and req_id is not None:
            col_a, col_b, _ = st.columns([1, 1, 4])
            with col_a:
                if st.button("✅ Approve", key=f"approve_{req_id}"):
                    try:
                        result = database.approve_request(req_id)
                        new_pin = (
                            result.get("pin") or result.get("pickup_pin")
                            if isinstance(result, dict) else None
                        )
                        msg = "Request approved!"
                        if new_pin:
                            msg += f" PIN: **{new_pin}**"
                        st.success(msg)
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Approval failed: {exc}")
            with col_b:
                if st.button("❌ Reject", key=f"reject_{req_id}"):
                    try:
                        database.reject_request(req_id)
                        st.warning("Request rejected.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Rejection failed: {exc}")


# ── Tab 3 – PIN Verify ───────────────────────────────────────────────────────

def _tab_pin_verify(donor_name: str) -> None:
    st.subheader("Verify Pickup PIN")
    st.caption("Confirm an NGO's pickup by validating their 4-digit PIN.")

    approved_requests = []
    try:
        all_reqs = database.get_requests_for_donor(donor_name) or []
        approved_requests = [r for r in all_reqs if r.get("status") == "approved"]
    except Exception as exc:
        st.error(f"Could not load approved requests: {exc}")
        return

    if not approved_requests:
        st.info("No approved requests awaiting pickup.")
        return

    options = {
        f"#{r.get('id') or r.get('request_id')} – {r.get('food_name','?')} → {r.get('recipient_name','?')}":
        r.get("id") or r.get("request_id")
        for r in approved_requests
    }

    selected_label = st.selectbox("Select Approved Request", list(options.keys()))
    request_id     = options[selected_label]

    pin_input = st.text_input(
        "Enter NGO's 4-digit PIN",
        max_chars=4,
        placeholder="e.g. 4782",
        type="password",
    )

    if st.button("🔓 Verify & Confirm Pickup", use_container_width=True):
        if len(pin_input) != 4 or not pin_input.isdigit():
            st.error("Please enter a valid 4-digit PIN.")
            return
        try:
            result = database.verify_pickup_pin(request_id, pin_input)
            if result:
                st.success("✅ PIN verified! Pickup confirmed. Thank you for reducing food waste 🌱")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Incorrect PIN. Please ask the NGO to check their pass.")
        except Exception as exc:
            st.error(f"Verification failed: {exc}")


# ── Main entry point ─────────────────────────────────────────────────────────

def render() -> None:
    donor_name = st.session_state.get("user_name", "Donor")

    st.markdown(
        f"<h2 style='color:{BLUE};margin-bottom:4px;'>👋 Welcome, {donor_name}</h2>"
        f"<p style='color:#555;margin-top:0;'>Manage your surplus food listings and pickups.</p>",
        unsafe_allow_html=True,
    )

    _render_kpis(donor_name)
    st.markdown("<hr style='margin:20px 0;'>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📦 Publish Surplus", "📋 Incoming Requests", "✅ PIN Verify"])

    with tab1:
        _tab_publish()

    with tab2:
        _tab_requests(donor_name)

    with tab3:
        _tab_pin_verify(donor_name)
