"""
views/recipient.py  -  FoodLoop NGO Marketplace
Role: recipient (NGO)
"""
import streamlit as st
import database
from utils import fmt_kg, fmt_num, format_countdown, is_urgent, meals_saved, hours_until, icon

TAG_CLASS = {
    "Cooked Meals": "fl-tag-cooked",
    "Bakery":       "fl-tag-bakery",
    "Produce":      "fl-tag-produce",
    "Dairy":        "fl-tag-dairy",
    "Packaged":     "fl-tag-packaged",
    "Beverages":    "fl-tag-beverages",
}


def _sid(doc) -> str:
    return str(doc.get("_id", ""))


def _req_qty(req) -> float:
    return float(req.get("requested_qty_kg", req.get("quantity_kg", 0)) or 0)


def _kpi_strip(listings, requests):
    available_kg = sum(float(l.get("remaining_qty_kg", l.get("quantity_kg", 0)) or 0)
                       for l in listings)
    urgent = sum(1 for l in listings if is_urgent(l.get("pickup_deadline")))
    passes = sum(1 for r in requests if r.get("status") == "approved")
    claimed_kg = sum(_req_qty(r) for r in requests
                     if r.get("status") in ("approved", "completed"))

    # Pass 3+5: no emoji, no uppercase labels
    cards = [
        (fmt_kg(available_kg),          "Available nearby",    False),
        (fmt_num(urgent),               "Urgent (< 2h)",       urgent > 0),
        (fmt_num(passes),               "Approved passes",     False),
        (fmt_num(meals_saved(claimed_kg)), "Meals claimed",    False),
    ]
    html = "".join(
        f'<div class="fl-kpi {"urgent" if u else ""}">'
        f'<div class="fl-kpi-val">{val}</div>'
        f'<div class="fl-kpi-label">{label}</div></div>'
        for val, label, u in cards
    )
    st.markdown(f'<div class="fl-kpi-grid">{html}</div>', unsafe_allow_html=True)


def _countdown_bar(listing: dict) -> str:
    """Signature: a 3px drain bar showing time remaining vs safe window."""
    deadline = listing.get("pickup_deadline")
    safe_hours = float(listing.get("safe_hours", 0) or 0)
    if deadline is None or safe_hours <= 0:
        return ""
    h = hours_until(deadline)
    if h < 0:
        pct = 0.0
    else:
        pct = max(0.0, min(100.0, (h / safe_hours) * 100.0))

    # Colour: coral at < 2h, amber at < 6h, blue otherwise
    if h < 2:
        color = "#D9381E"
    elif h < 6:
        color = "#d97706"
    else:
        color = "#014BAA"

    return (
        f'<div class="fl-countdown-bar-wrap">'
        f'<div class="fl-countdown-bar" style="width:{pct:.1f}%;background:{color};"></div>'
        f'</div>'
    )


# ── Marketplace ─────────────────────────────────────────────────────────────
def _marketplace(recipient_id, recipient_name):
    try:
        listings = database.get_available_listings() or []
    except Exception as exc:
        st.error(f"Could not load the marketplace: {exc}")
        return

    st.markdown(
        '<div class="fl-card-title">Live marketplace</div>'
        '<div class="fl-card-sub">Claim full or partial quantities before the pickup window closes.</div>',
        unsafe_allow_html=True,
    )

    if not listings:
        st.markdown(
            f'<div class="fl-empty">'
            f'<div class="fl-empty-icon">{icon("package", 28)}</div>'
            f'<div class="fl-empty-title">No surplus available right now</div>'
            f'<div class="fl-empty-sub">Donors post new listings daily — check back shortly.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        return

    for listing in listings:
        lid = _sid(listing)
        category = listing.get("category", "Cooked Meals")
        urgent = is_urgent(listing.get("pickup_deadline"))
        qty = float(listing.get("remaining_qty_kg", listing.get("quantity_kg", 0)) or 0)
        tag_class = TAG_CLASS.get(category, "fl-tag-blue")
        countdown_text = format_countdown(listing.get("pickup_deadline"))
        bar_html = _countdown_bar(listing)

        urgent_badge = (
            '<span class="fl-urgent-badge">Under 2h left</span>'
            if urgent else ""
        )

        st.markdown(
            f'<div class="fl-food-card {"urgent" if urgent else ""}">'
            f'<div class="fl-food-head">'
            f'<span class="fl-food-name">{listing.get("food_name", "Surplus food")}</span>'
            f'<span class="fl-tag {tag_class}">{category}</span>'
            f'{urgent_badge}'
            f'</div>'
            f'<div class="fl-food-meta">'
            f'<span>{icon("user", 13)} <b>{listing.get("donor_name", "Verified donor")}</b></span>'
            f'<span>{icon("scale", 13)} <b>{fmt_kg(qty)}</b> available</span>'
            f'<span>{icon("snowflake", 13)} {listing.get("storage_condition", "Room temp")}</span>'
            f'<span>{icon("map-pin", 13)} {listing.get("location") or "Campus pickup"}</span>'
            f'</div>'
            f'<div class="fl-countdown {"urgent" if urgent else ""}">'
            f'{icon("clock", 13)} {countdown_text}'
            f'</div>'
            f'{bar_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

        with st.expander(f"Claim {listing.get('food_name', 'this listing')}"):
            full = st.checkbox("Claim the full remaining quantity", value=False,
                               key=f"full_{lid}")
            if full:
                claim_qty = qty
                st.markdown(
                    f'<div class="fl-card-sub" style="margin:0 0 8px;">'
                    f'Requesting all <b>{fmt_kg(qty)}</b>.</div>',
                    unsafe_allow_html=True)
            else:
                max_qty = max(round(qty, 1), 0.5)
                claim_qty = st.number_input(
                    "Quantity to claim (kg)",
                    min_value=0.5,
                    max_value=max_qty,
                    value=min(1.0, max_qty),
                    step=0.5,
                    key=f"qty_{lid}",
                )

            if st.button("Submit claim", key=f"claim_{lid}",
                         use_container_width=True, type="primary"):
                try:
                    ok, msg = database.create_request(
                        listing_id=lid,
                        recipient_id=recipient_id,
                        recipient_name=recipient_name,
                        qty_kg=float(claim_qty),
                    )
                except Exception as exc:
                    st.error(f"Could not submit claim: {exc}")
                else:
                    if ok:
                        st.success(f"{msg} The donor reviews it now — your PIN appears under Pickup passes once approved.")
                        st.rerun()
                    else:
                        st.error(msg)


# ── Pickup passes ───────────────────────────────────────────────────────────
def _pickup_passes(requests):
    st.markdown(
        '<div class="fl-card-title">Pickup passes</div>'
        '<div class="fl-card-sub">Show the 4-digit PIN to the donor at handover. Never share it early.</div>',
        unsafe_allow_html=True,
    )

    if not requests:
        st.markdown(
            f'<div class="fl-empty">'
            f'<div class="fl-empty-icon">{icon("ticket", 28)}</div>'
            f'<div class="fl-empty-title">No claims yet</div>'
            f'<div class="fl-empty-sub">Claim surplus from the marketplace to receive a pickup pass.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        return

    ordered = sorted(requests, key=lambda r: 0 if r.get("status") == "approved" else 1)
    for req in ordered:
        status = (req.get("status") or "pending").lower()
        pin = req.get("pickup_pin")
        food = req.get("food_name", "Surplus food")
        qty = _req_qty(req)
        donor = req.get("donor_name", "Donor")
        location = req.get("location") or "Pickup venue"

        if status == "approved" and pin:
            st.markdown(
                f'<div class="fl-ticket">'
                f'<div class="fl-ticket-label">'
                f'{icon("ticket", 12)} Pickup pass · approved'
                f'</div>'
                f'<div class="fl-ticket-pin">{pin}</div>'
                f'<div class="fl-ticket-food">{food} · {fmt_kg(qty)}</div>'
                f'<div class="fl-ticket-meta">'
                f'{icon("user", 13)} {donor}'
                f'&nbsp;·&nbsp;'
                f'{icon("map-pin", 13)} {location}'
                f'</div>'
                f'<div class="fl-ticket-hint">'
                f'Show this PIN to the donor at pickup to complete the handover.'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            note = {
                "pending":   "Waiting for donor approval — your PIN is issued on approval.",
                "rejected":  "This claim was declined by the donor.",
                "completed": "Collected. Thank you for feeding your community.",
            }.get(status, "")
            st.markdown(
                f'<div class="fl-req-card {status}">'
                f'<div class="fl-req-title">{food}</div>'
                f'<div class="fl-req-meta">'
                f'{icon("scale", 13)} {fmt_kg(qty)}'
                f'&nbsp;·&nbsp;'
                f'{icon("user", 13)} {donor}'
                f'&nbsp;·&nbsp;'
                f'{icon("map-pin", 13)} {location}'
                f'&nbsp;·&nbsp;'
                f'<span class="fl-status fl-status-{status}">{status}</span>'
                f'</div>'
                f'<div class="fl-req-meta" style="margin-top:4px;">{note}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ── Render ──────────────────────────────────────────────────────────────────
def render():
    recipient_id = str(st.session_state.get("user_id", ""))
    recipient_name = st.session_state.get("user_name", "NGO")

    try:
        listings = database.get_available_listings() or []
    except Exception:
        listings = []
    try:
        requests = database.get_requests_for_recipient(recipient_id) or []
    except Exception:
        requests = []

    # Pass 4: no emoji page title, no greeting copy
    st.markdown(
        '<div class="fl-page-head fl-wrap-wide">'
        '<h1 class="fl-page-title">Marketplace</h1>'
        '<p class="fl-page-sub">'
        'Claim surplus from verified donors and collect with a 4-digit PIN.'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="recipient_body"):
        _kpi_strip(listings, requests)

        # Pass 3: no emoji in tab labels
        tab_market, tab_passes = st.tabs(["Live marketplace", "Pickup passes"])
        with tab_market:
            with st.container(key="recipient_market"):
                _marketplace(recipient_id, recipient_name)
        with tab_passes:
            with st.container(key="recipient_passes"):
                _pickup_passes(requests)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
