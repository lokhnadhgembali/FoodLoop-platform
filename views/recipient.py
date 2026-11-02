"""
views/recipient.py  -  FoodLoop NGO Marketplace
Role: recipient (NGO)
"""
import streamlit as st
import database
from utils import fmt_kg, fmt_num, format_countdown, is_urgent, meals_saved

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

    cards = [
        ("🛒", fmt_kg(available_kg), "Available Food Nearby", False),
        ("🔥", fmt_num(urgent),      "Urgent Listings (< 2h)", urgent > 0),
        ("🎫", fmt_num(passes),      "Approved Pickup Passes", False),
        ("🍽️", fmt_num(meals_saved(claimed_kg)), "Meals Claimed", False),
    ]
    html = "".join(
        f'<div class="fl-kpi {"urgent" if urgent else ""}">'
        f'<div class="fl-kpi-icon">{icon}</div>'
        f'<div class="fl-kpi-val">{val}</div>'
        f'<div class="fl-kpi-label">{label}</div></div>'
        for icon, val, label, urgent in cards
    )
    st.markdown(f'<div class="fl-kpi-grid">{html}</div>', unsafe_allow_html=True)


# ── Marketplace ─────────────────────────────────────────────────────────────
def _marketplace(recipient_id, recipient_name):
    try:
        listings = database.get_available_listings() or []
    except Exception as exc:
        st.error(f"Could not load the marketplace: {exc}")
        return

    st.markdown("""
    <div class="fl-card-title">🛒 Live Surplus Marketplace</div>
    <div class="fl-card-sub">Claim full or partial quantities before the pickup window closes.</div>
    """, unsafe_allow_html=True)

    if not listings:
        st.markdown("""
        <div class="fl-empty">
          <div class="fl-empty-icon">🌟</div>
          <div class="fl-empty-title">No surplus available right now</div>
          <div class="fl-empty-sub">Donors post new listings daily — check back shortly.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    for listing in listings:
        lid = _sid(listing)
        category = listing.get("category", "Cooked Meals")
        urgent = is_urgent(listing.get("pickup_deadline"))
        qty = float(listing.get("remaining_qty_kg", listing.get("quantity_kg", 0)) or 0)
        tag_class = TAG_CLASS.get(category, "fl-tag-blue")

        st.markdown(f"""
        <div class="fl-food-card {'urgent' if urgent else ''}">
          <div class="fl-food-head">
            <span class="fl-food-name">{listing.get('food_name', 'Surplus food')}</span>
            <span class="fl-tag {tag_class}">{category}</span>
            {'<span class="fl-urgent-badge">🔥 URGENT EXPIRY (&lt; 2h)</span>' if urgent else ''}
          </div>
          <div class="fl-food-meta">
            <span>👤 <b>{listing.get('donor_name', 'Verified donor')}</b></span>
            <span>⚖️ <b>{fmt_kg(qty)}</b> available</span>
            <span>❄️ {listing.get('storage_condition', 'Room Temp')}</span>
            <span>📍 {listing.get('location') or 'Campus pickup'}</span>
          </div>
          <div class="fl-countdown {'urgent' if urgent else ''}">⏱️ {format_countdown(listing.get('pickup_deadline'))}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"🛒 Claim {listing.get('food_name', 'this listing')}"):
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

            if st.button("Submit Claim Request", key=f"claim_{lid}",
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
                        st.success(f"🎉 {msg} The donor reviews it now — your PIN appears under My Pickup Passes once approved.")
                        st.rerun()
                    else:
                        st.error(msg)


# ── Pickup passes ───────────────────────────────────────────────────────────
def _pickup_passes(requests):
    st.markdown("""
    <div class="fl-card-title">🎫 My Active Pickup Passes</div>
    <div class="fl-card-sub">Show the 4-digit PIN to the donor at handover. Never share it early.</div>
    """, unsafe_allow_html=True)

    if not requests:
        st.markdown("""
        <div class="fl-empty">
          <div class="fl-empty-icon">🎫</div>
          <div class="fl-empty-title">No claims yet</div>
          <div class="fl-empty-sub">Claim surplus from the marketplace to receive a pickup pass.</div>
        </div>
        """, unsafe_allow_html=True)
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
            st.markdown(f"""
            <div class="fl-ticket">
              <div class="fl-ticket-label">🎫 Pickup Pass · Approved</div>
              <div class="fl-ticket-pin">{pin}</div>
              <div class="fl-ticket-food">{food} · {fmt_kg(qty)}</div>
              <div class="fl-ticket-meta">👤 {donor} &nbsp;·&nbsp; 📍 {location}</div>
              <div class="fl-ticket-hint">
                Show this PIN to the donor at pickup to complete the handover.
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            note = {
                "pending":   "⏳ Waiting for donor approval — your PIN is issued on approval.",
                "rejected":  "This claim was declined by the donor.",
                "completed": "✅ Collected. Thank you for feeding your community.",
            }.get(status, "")
            st.markdown(f"""
            <div class="fl-req-card {status}">
              <div class="fl-req-title">{food}</div>
              <div class="fl-req-meta">
                ⚖️ {fmt_kg(qty)} &nbsp;·&nbsp; 👤 {donor} &nbsp;·&nbsp;
                📍 {location} &nbsp;·&nbsp;
                <span class="fl-status fl-status-{status}">{status}</span>
              </div>
              <div class="fl-req-meta">{note}</div>
            </div>
            """, unsafe_allow_html=True)


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

    st.markdown(f"""
    <div class="fl-page-head fl-wrap-wide">
      <h1 class="fl-page-title">🤝 NGO Marketplace</h1>
      <p class="fl-page-sub">
        {recipient_name}, claim verified surplus and collect it with a secure pickup PIN.
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(key="recipient_body"):
        _kpi_strip(listings, requests)

        tab_market, tab_passes = st.tabs(["🛒 Live Marketplace", "🎫 My Pickup Passes"])
        with tab_market:
            with st.container(key="recipient_market"):
                _marketplace(recipient_id, recipient_name)
        with tab_passes:
            with st.container(key="recipient_passes"):
                _pickup_passes(requests)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
