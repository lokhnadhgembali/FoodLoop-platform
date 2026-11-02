"""
FoodLoop – NGO / Recipient Dashboard
"""

import streamlit as st
import database
from utils import fmt_kg, fmt_num, format_countdown, is_urgent

# ── colour palette ──────────────────────────────────────────────────────────
BLUE   = "#014BAA"
CREAM  = "#F8F3F0"
CORAL  = "#D9381E"
GREEN  = "#10B981"
WHITE  = "#FFFFFF"

# ── helpers ─────────────────────────────────────────────────────────────────

def _card(body: str, bg: str = WHITE, border_color: str = BLUE) -> None:
    st.markdown(
        f"""
        <div style="background:{bg};border-left:4px solid {border_color};
                    border-radius:8px;padding:16px 20px;margin-bottom:12px;
                    box-shadow:0 1px 4px rgba(0,0,0,.08);">
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _badge(label: str, color: str = BLUE, text_color: str = "#fff") -> str:
    return (
        f'<span style="background:{color};color:{text_color};border-radius:4px;'
        f'padding:2px 8px;font-size:0.75rem;font-weight:600;">{label}</span>'
    )


STATUS_COLORS = {
    "pending":   "#F59E0B",
    "approved":  GREEN,
    "rejected":  CORAL,
    "completed": "#6B7280",
}

STATUS_BG = {
    "pending":   "#FFFBEB",
    "approved":  "#ECFDF5",
    "rejected":  "#FEF2F2",
    "completed": "#F9FAFB",
}


# ── KPI strip ───────────────────────────────────────────────────────────────

def _render_kpis(recipient_id: str) -> None:
    listings = []
    try:
        listings = database.get_available_listings() or []
    except Exception:
        pass

    my_requests = []
    try:
        my_requests = database.get_requests_for_recipient(recipient_id) or []
    except Exception:
        pass

    available_count = len(listings)
    urgent_count    = sum(1 for l in listings if is_urgent(l))
    approved_passes = sum(1 for r in my_requests if r.get("status") == "approved")
    total_kg        = sum(
        r.get("quantity_kg", 0) for r in my_requests if r.get("status") in ("approved", "completed")
    )

    cols = st.columns(4)
    kpis = [
        ("🛒", "Available Listings", fmt_num(available_count)),
        ("⚡", "Urgent (<2 h)",      fmt_num(urgent_count)),
        ("🎫", "Approved Passes",    fmt_num(approved_passes)),
        ("⚖️", "Total kg Claimed",   fmt_kg(total_kg)),
    ]
    for col, (icon, label, value) in zip(cols, kpis):
        with col:
            bg = CORAL if label == "Urgent (<2 h)" and urgent_count > 0 else BLUE
            st.markdown(
                f"""
                <div style="background:{bg};color:#fff;border-radius:10px;
                            padding:16px;text-align:center;">
                    <div style="font-size:1.6rem;">{icon}</div>
                    <div style="font-size:1.4rem;font-weight:700;">{value}</div>
                    <div style="font-size:0.75rem;opacity:.85;">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ── Tab 1 – Live Marketplace ─────────────────────────────────────────────────

def _tab_marketplace(recipient_name: str, recipient_id: str) -> None:
    st.subheader("Live Food Listings")

    listings = []
    try:
        listings = database.get_available_listings() or []
    except Exception as exc:
        st.error(f"Could not load listings: {exc}")
        return

    if not listings:
        st.info("🌟 No food listings available right now. Check back soon!")
        return

    for listing in listings:
        listing_id   = listing.get("id") or listing.get("listing_id")
        food_name    = listing.get("food_name", "Unknown Food")
        category     = listing.get("category", "")
        quantity_kg  = listing.get("quantity_kg", 0)
        location     = listing.get("location", "Unknown Location")
        storage_note = listing.get("storage_note", "")
        donor_name   = listing.get("donor_name", "Anonymous Donor")
        urgent       = is_urgent(listing)

        countdown_html = format_countdown(listing)

        urgent_badge = (
            f'&nbsp;{_badge("⚡ URGENT", CORAL)}' if urgent else ""
        )

        body = (
            f"<div style='display:flex;align-items:center;gap:8px;flex-wrap:wrap;'>"
            f"<b style='font-size:1.05rem;'>{food_name}</b>"
            f"&nbsp;{_badge(category, BLUE)}{urgent_badge}"
            f"</div>"
            f"<div style='margin-top:6px;color:#555;font-size:.9rem;'>"
            f"📍 {location} &nbsp;|&nbsp; ⚖️ {fmt_kg(quantity_kg)} available"
            f"&nbsp;|&nbsp; 👤 {donor_name}"
            f"</div>"
            f"<div style='margin-top:4px;font-size:.85rem;color:#777;'>⏰ {countdown_html}</div>"
        )
        if storage_note:
            body += f"<div style='margin-top:4px;font-size:.82rem;color:#888;'>📝 {storage_note}</div>"

        border = CORAL if urgent else BLUE
        _card(body, border_color=border)

        with st.expander("🛒 Claim This Food", expanded=False):
            max_qty = max(float(quantity_kg), 0.5)
            claim_qty = st.slider(
                "Quantity to claim (kg)",
                min_value=0.5,
                max_value=float(max_qty),
                step=0.5,
                value=min(1.0, float(max_qty)),
                key=f"slider_{listing_id}",
            )
            if st.button("✅ Submit Claim", key=f"claim_{listing_id}", use_container_width=True):
                try:
                    database.create_request(
                        listing_id     = listing_id,
                        recipient_name = recipient_name,
                        recipient_id   = recipient_id,
                        quantity_kg    = claim_qty,
                        unit           = "kg",
                    )
                    st.success(
                        f"🎉 Claim submitted for {fmt_kg(claim_qty)} of '{food_name}'! "
                        "Check **My Passes** for your status."
                    )
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not submit claim: {exc}")


# ── Tab 2 – My Passes ───────────────────────────────────────────────────────

def _tab_my_passes(recipient_id: str) -> None:
    st.subheader("My Passes & Requests")

    requests = []
    try:
        requests = database.get_requests_for_recipient(recipient_id) or []
    except Exception as exc:
        st.error(f"Could not load your passes: {exc}")
        return

    if not requests:
        st.info("You haven't claimed any food yet. Head to the Marketplace to get started!")
        return

    for req in requests:
        req_id      = req.get("id") or req.get("request_id")
        food_name   = req.get("food_name", "Unknown Food")
        donor_loc   = req.get("location", "Unknown Location")
        donor_name  = req.get("donor_name", "Unknown Donor")
        qty         = req.get("quantity_kg", 0)
        status      = req.get("status", "pending").lower()
        pin         = req.get("pin") or req.get("pickup_pin")
        badge_color = STATUS_COLORS.get(status, BLUE)
        card_bg     = STATUS_BG.get(status, WHITE)

        if status == "approved" and pin:
            # PIN Ticket card
            body = (
                f"<div style='text-align:center;padding:4px 0;'>"
                f"<div style='font-size:.8rem;color:#555;text-transform:uppercase;"
                f"letter-spacing:.08em;'>🎫 Pickup Pass — {_badge('APPROVED', GREEN)}</div>"
                f"<div style='font-size:2.4rem;font-weight:800;font-family:monospace;"
                f"color:{BLUE};letter-spacing:.3em;margin:10px 0;'>{pin}</div>"
                f"<div style='font-size:.85rem;color:#555;'>"
                f"<b>{food_name}</b> &nbsp;|&nbsp; {fmt_kg(qty)}</div>"
                f"<div style='font-size:.82rem;color:#777;margin-top:4px;'>"
                f"📍 {donor_loc} &nbsp;|&nbsp; 👤 {donor_name}</div>"
                f"<div style='margin-top:10px;background:{CREAM};border-radius:6px;"
                f"padding:8px 12px;font-size:.82rem;color:#444;'>"
                f"📲 Show this PIN to the donor at pickup to confirm collection.</div>"
                f"</div>"
            )
            _card(body, bg=card_bg, border_color=GREEN)

        else:
            # Standard status card
            body = (
                f"<b>{food_name}</b> &nbsp; {_badge(status.upper(), badge_color)}<br>"
                f"<span style='color:#555;font-size:.9rem;'>"
                f"⚖️ {fmt_kg(qty)} &nbsp;|&nbsp; 📍 {donor_loc} &nbsp;|&nbsp; 👤 {donor_name}"
                f"</span>"
            )
            if status == "rejected":
                body += "<br><span style='color:#777;font-size:.8rem;'>This request was not approved by the donor.</span>"
            elif status == "completed":
                body += "<br><span style='color:#6B7280;font-size:.8rem;'>✅ Pickup completed. Thank you!</span>"
            elif status == "pending":
                body += "<br><span style='color:#777;font-size:.8rem;'>⏳ Awaiting donor approval.</span>"

            _card(body, bg=card_bg, border_color=badge_color)


# ── Main entry point ─────────────────────────────────────────────────────────

def render() -> None:
    recipient_name = st.session_state.get("user_name", "NGO")
    recipient_id   = st.session_state.get("user_id", "")

    st.markdown(
        f"<h2 style='color:{BLUE};margin-bottom:4px;'>👋 Welcome, {recipient_name}</h2>"
        f"<p style='color:#555;margin-top:0;'>Discover and claim surplus food in your area.</p>",
        unsafe_allow_html=True,
    )

    _render_kpis(recipient_id)
    st.markdown("<hr style='margin:20px 0;'>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🛒 Live Marketplace", "🎫 My Passes"])

    with tab1:
        _tab_marketplace(recipient_name, recipient_id)

    with tab2:
        _tab_my_passes(recipient_id)
