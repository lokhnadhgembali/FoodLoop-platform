"""
views/donor.py  -  FoodLoop Donor Hub
Role: donor
"""
import streamlit as st
import database
from utils import fmt_kg, fmt_num, format_countdown, is_urgent, icon

CATEGORIES = ["Cooked Meals", "Bakery", "Produce", "Dairy", "Packaged"]
STORAGE_OPTIONS = ["Room Temp", "Refrigerated", "Frozen"]

TAG_CLASS = {
    "Cooked Meals": "fl-tag-cooked",
    "Bakery":       "fl-tag-bakery",
    "Produce":      "fl-tag-produce",
    "Dairy":        "fl-tag-dairy",
    "Packaged":     "fl-tag-packaged",
}


def _sid(doc) -> str:
    return str(doc.get("_id", ""))


def _req_qty(req) -> float:
    return float(req.get("requested_qty_kg", req.get("quantity_kg", 0)) or 0)


def _kpi_strip(listings, requests):
    active    = sum(1 for l in listings if l.get("status") == "available")
    pending   = sum(1 for r in requests if r.get("status") == "pending")
    completed = sum(1 for r in requests if r.get("status") == "completed")
    total_kg  = sum(float(r.get("requested_qty_kg", 0) or 0)
                    for r in requests if r.get("status") == "completed")
    if total_kg == 0:
        total_kg = sum(float(l.get("quantity_kg", 0) or 0)
                       for l in listings if l.get("status") == "collected")
    points = int(st.session_state.get("reward_points", 0) or 0)

    # Pass 3+5: no emoji icons, no uppercase labels
    cards = [
        (fmt_num(active),    "Active listings"),
        (fmt_num(pending),   "Pending claims"),
        (fmt_num(completed), "Completed pickups"),
        (fmt_kg(total_kg),   "Total donated"),
        (fmt_num(points),    "Reward points"),
    ]
    html = "".join(
        f'<div class="fl-kpi">'
        f'<div class="fl-kpi-val">{val}</div>'
        f'<div class="fl-kpi-label">{label}</div></div>'
        for val, label in cards
    )
    st.markdown(f'<div class="fl-kpi-grid">{html}</div>', unsafe_allow_html=True)


# ── Publish ─────────────────────────────────────────────────────────────────
def _publish_form():
    st.markdown(
        '<div class="fl-card-title">Publish surplus food</div>'
        '<div class="fl-card-sub">'
        'Add a listing with a safe pickup window. Verified NGOs can claim part or all of it '
        'before the deadline.'
        '</div>',
        unsafe_allow_html=True,
    )

    with st.form("publish_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            food_name = st.text_input("Food name", placeholder="e.g. Dal Makhani & Rice")
        with c2:
            category = st.selectbox("Category", CATEGORIES)

        c3, c4 = st.columns(2)
        with c3:
            quantity_kg = st.number_input("Quantity (kg)", min_value=0.5, max_value=500.0,
                                          value=5.0, step=0.5)
        with c4:
            meals = st.number_input("Estimated meals", min_value=1, max_value=2000,
                                    value=int(quantity_kg * 2), step=1)

        c5, c6 = st.columns(2)
        with c5:
            storage = st.selectbox("Storage", STORAGE_OPTIONS)
        with c6:
            safe_hours = st.slider("Safe pickup window (hours)", 1, 48, 6)

        location = st.text_input("Pickup location", value="LPU Campus, Phagwara")
        note = st.text_input("Storage note (optional)", placeholder="Keep refrigerated until pickup")

        submitted = st.form_submit_button("Publish listing", use_container_width=True,
                                          type="primary")

    if submitted:
        if not food_name.strip():
            st.error("Please enter the food name.")
        elif not location.strip():
            st.error("Please enter a pickup location.")
        else:
            try:
                database.add_listing(
                    donor_id=st.session_state.get("user_id", ""),
                    donor_name=st.session_state.get("user_name", ""),
                    food_name=food_name.strip(),
                    category=category,
                    quantity_kg=float(quantity_kg),
                    servings=int(meals),
                    storage=storage,
                    safe_hours=int(safe_hours),
                    location=location.strip(),
                    description=note.strip(),
                )
            except Exception as exc:
                st.error(f"Could not publish listing: {exc}")
            else:
                st.success(f"'{food_name.strip()}' is live — NGOs can claim it now.")
                st.rerun()


# ── Incoming requests ───────────────────────────────────────────────────────
def _requests_queue(requests):
    st.markdown(
        '<div class="fl-card-title">Incoming claims</div>'
        '<div class="fl-card-sub">'
        'Approving a claim issues a secret 4-digit pickup PIN to the NGO. The PIN is never '
        'shown here — the NGO presents it at handover.'
        '</div>',
        unsafe_allow_html=True,
    )

    if not requests:
        st.markdown(
            f'<div class="fl-empty">'
            f'<div class="fl-empty-icon">{icon("inbox", 28)}</div>'
            f'<div class="fl-empty-title">No claims yet</div>'
            f'<div class="fl-empty-sub">NGOs will appear here as soon as they claim your listings.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        return

    for req in requests:
        rid = _sid(req)
        status = (req.get("status") or "pending").lower()
        st.markdown(
            f'<div class="fl-req-card {status}">'
            f'<div class="fl-req-title">{req.get("food_name", "Surplus food")}</div>'
            f'<div class="fl-req-meta">'
            f'{icon("user", 14)} <b>{req.get("recipient_name", "NGO")}</b>'
            f'&nbsp;·&nbsp;'
            f'{icon("scale", 14)} {fmt_kg(_req_qty(req))}'
            f'&nbsp;·&nbsp;'
            f'{icon("map-pin", 14)} {req.get("location") or "Campus pickup"}'
            f'</div>'
            f'<div style="margin-top:8px;">'
            f'<span class="fl-status fl-status-{status}">{status}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if status == "pending":
            ca, cb, _ = st.columns([1, 1, 4])
            with ca:
                if st.button("Approve", key=f"approve_{rid}", use_container_width=True,
                             type="primary"):
                    try:
                        ok, msg = database.approve_request(rid)
                    except Exception as exc:
                        st.error(f"Approval failed: {exc}")
                    else:
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
            with cb:
                if st.button("Reject", key=f"reject_{rid}", use_container_width=True):
                    try:
                        database.reject_request(rid)
                    except Exception as exc:
                        st.error(f"Rejection failed: {exc}")
                    else:
                        st.warning("Claim rejected.")
                        st.rerun()


# ── PIN handshake ───────────────────────────────────────────────────────────
def _pin_handshake(requests):
    st.markdown(
        '<div class="fl-card-title">PIN handshake</div>'
        '<div class="fl-card-sub">'
        'At the pickup venue the NGO shows their pickup pass. Enter those 4 digits to confirm '
        'the handover — this completes the request, closes the listing and logs the impact.'
        '</div>',
        unsafe_allow_html=True,
    )

    approved = [r for r in requests if r.get("status") == "approved"]
    if not approved:
        st.markdown(
            f'<div class="fl-empty">'
            f'<div class="fl-empty-icon">{icon("key", 28)}</div>'
            f'<div class="fl-empty-title">No approved pickups waiting</div>'
            f'<div class="fl-empty-sub">Approve a pending claim first, then verify its PIN here.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        return

    options = {}
    for r in approved:
        label = f"{r.get('food_name', 'Food')} → {r.get('recipient_name', 'NGO')} · {fmt_kg(_req_qty(r))}"
        options[label] = _sid(r)

    selected_label = st.selectbox("Approved request", list(options.keys()), key="pin_request")
    pin_input = st.text_input("NGO's 4-digit PIN", max_chars=4, type="password",
                              placeholder="••••", key="pin_input",
                              help="The NGO reads this from their pickup pass at handover.")

    if st.button("Verify & complete pickup", key="pin_verify",
                 use_container_width=True, type="primary"):
        pin = pin_input.strip()
        if len(pin) != 4 or not pin.isdigit():
            st.error("Enter the 4-digit numeric PIN shown by the NGO.")
        else:
            try:
                ok, msg = database.verify_pickup_pin(options[selected_label], pin)
            except Exception as exc:
                st.error(f"Verification failed: {exc}")
            else:
                if ok:
                    st.success(msg)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(msg)


# ── Render ──────────────────────────────────────────────────────────────────
def render():
    donor_id = str(st.session_state.get("user_id", ""))
    donor_name = st.session_state.get("user_name", "Donor")

    try:
        listings = database.get_donor_listings(donor_id) or []
    except Exception:
        listings = []
    try:
        requests = database.get_requests_for_donor(donor_id) or []
    except Exception:
        requests = []

    # Pass 4: no greeting emoji, no "Welcome back" copy
    st.markdown(
        f'<div class="fl-page-head fl-wrap-wide">'
        f'<h1 class="fl-page-title">Donor hub</h1>'
        f'<p class="fl-page-sub">'
        f'Publish surplus food, approve claims and verify pickups, {donor_name}.'
        f'</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="donor_body"):
        _kpi_strip(listings, requests)

        # Pass 3: no emoji in tab labels
        tab_publish, tab_requests, tab_pin = st.tabs(
            ["Publish surplus", "Incoming claims", "PIN handshake"]
        )
        with tab_publish:
            with st.container(key="donor_publish"):
                _publish_form()
        with tab_requests:
            with st.container(key="donor_requests"):
                _requests_queue(requests)
        with tab_pin:
            with st.container(key="donor_pin"):
                _pin_handshake(requests)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
