"""
views/analytics.py  -  FoodLoop Impact & Analytics
Accessible to every authenticated role.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import database
from utils import fmt_kg, fmt_num, format_countdown, is_urgent, icon

BLUE    = "#014BAA"
BLUE2   = "#2563EB"
EMERALD = "#10B981"
AMBER   = "#d97706"
CORAL   = "#D9381E"

STATUS_LABELS = {
    "pending":   "Pending",
    "approved":  "Approved",
    "completed": "Completed",
    "rejected":  "Rejected",
}

CHART_FONT = dict(family="Plus Jakarta Sans, Inter, sans-serif", size=12, color="#5e554a")

# Pass 2: neutral warm gridlines instead of blue-tinted
GRID_COLOR = "rgba(31, 27, 22, 0.06)"


def _sid(doc) -> str:
    return str(doc.get("_id", ""))


def _kpi_cards(stats):
    # Pass 3+5: no emoji, no uppercase labels
    cards = [
        (fmt_num(stats.get("total_listings", 0)),                    "Total listings"),
        (fmt_num(stats.get("completed_pickups", 0)),                 "Successful pickups"),
        (fmt_num(stats.get("pending_requests", 0)),                  "Pending requests"),
        (fmt_kg(float(stats.get("total_kg_diverted", 0) or 0)),     "Food redistributed"),
    ]
    html = "".join(
        f'<div class="fl-kpi">'
        f'<div class="fl-kpi-val">{val}</div>'
        f'<div class="fl-kpi-label">{label}</div></div>'
        for val, label in cards
    )
    st.markdown(f'<div class="fl-kpi-grid">{html}</div>', unsafe_allow_html=True)


def _base_layout(fig, margin=None):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=CHART_FONT,
        margin=margin or dict(l=6, r=6, t=6, b=6),
        showlegend=False,
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Plus Jakarta Sans"),
    )
    return fig


def _weekly_chart():
    # Pass 5: sentence case chart title, no emoji
    st.markdown('<div class="fl-chart-title">Weekly collection volume (kg)</div>',
                unsafe_allow_html=True)
    try:
        weekly = database.get_weekly_trend() or []
    except Exception as exc:
        st.info(f"Weekly data unavailable: {exc}")
        return

    if not weekly:
        st.info("No completed pickups yet — this chart fills in as donations are collected.")
        return

    df = pd.DataFrame(weekly)
    fig = px.bar(df, x="week_label", y="kg_donated",
                 labels={"week_label": "", "kg_donated": "kg collected"},
                 color_discrete_sequence=[BLUE])
    fig.update_traces(marker_line_width=0, opacity=0.88,
                      hovertemplate="%{x}<br><b>%{y:.1f} kg</b> collected<extra></extra>")
    fig.update_layout(
        xaxis=dict(showgrid=False, tickangle=-35),
        yaxis=dict(gridcolor=GRID_COLOR, zeroline=False),
    )
    _base_layout(fig, margin=dict(l=0, r=4, t=4, b=0))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _status_donut():
    # Pass 5: sentence case, no emoji
    st.markdown('<div class="fl-chart-title">Request status breakdown</div>',
                unsafe_allow_html=True)
    try:
        counts = database.get_request_status_counts() or {}
    except Exception as exc:
        st.info(f"Request data unavailable: {exc}")
        return

    df = pd.DataFrame(
        [{"Status": STATUS_LABELS.get(k, k.title()), "Count": v}
         for k, v in counts.items() if v]
    )
    if df.empty:
        st.info("No claims recorded yet.")
        return

    color_map = {"Pending": AMBER, "Approved": BLUE2, "Completed": EMERALD, "Rejected": CORAL}
    fig = px.pie(df, names="Status", values="Count", hole=0.55,
                 color="Status", color_discrete_map=color_map)
    fig.update_traces(textposition="outside", textinfo="percent",
                      marker=dict(line=dict(color="#fdfbf7", width=2)))
    _base_layout(fig, margin=dict(l=0, r=0, t=0, b=0))
    fig.update_layout(legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center",
                                  font=dict(size=11, color="#5e554a")))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _category_chart():
    # Pass 5: sentence case, no emoji
    st.markdown('<div class="fl-chart-title">Quantity by category (kg)</div>',
                unsafe_allow_html=True)
    try:
        categories = database.get_category_totals() or []
    except Exception as exc:
        st.info(f"Category data unavailable: {exc}")
        return

    if not categories:
        st.info("No completed donations by category yet.")
        return

    df = pd.DataFrame(categories)
    fig = px.bar(df, x="category", y="total_kg",
                 labels={"category": "", "total_kg": "kg redistributed"},
                 color_discrete_sequence=[BLUE2])
    fig.update_traces(marker_line_width=0, opacity=0.88,
                      hovertemplate="%{x}<br><b>%{y:.1f} kg</b><extra></extra>")
    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor=GRID_COLOR, zeroline=False),
    )
    _base_layout(fig, margin=dict(l=0, r=4, t=4, b=0))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _expiring_table():
    # Pass 5: sentence case, no emoji
    st.markdown('<div class="fl-chart-title">Expiring within 12 hours</div>',
                unsafe_allow_html=True)
    try:
        listings = database.get_expiring_listings(hours=12) or []
    except Exception as exc:
        st.info(f"Expiry data unavailable: {exc}")
        return

    if not listings:
        st.success("No listings expiring in the next 12 hours.")
        return

    rows = []
    for item in listings:
        rows.append({
            "Food":      item.get("food_name", "—"),
            "Category":  item.get("category", "—"),
            "Donor":     item.get("donor_name", "—"),
            "Qty (kg)":  round(float(item.get("remaining_qty_kg", 0) or 0), 1),
            "Time left": format_countdown(item.get("pickup_deadline")),
            # Pass 3+5: plain text priority labels, no emoji
            "Priority":  "Urgent" if is_urgent(item.get("pickup_deadline")) else "Soon",
        })
    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Qty (kg)":  st.column_config.NumberColumn("Qty (kg)", format="%.1f"),
            "Priority":  st.column_config.TextColumn("Priority", width="small"),
        },
    )


def render():
    try:
        stats = database.get_platform_stats() or {}
    except Exception:
        stats = {}

    # Pass 4: no emoji page title
    st.markdown("""
    <div class="fl-page-head fl-wrap-wide">
      <h1 class="fl-page-title">Impact &amp; analytics</h1>
      <p class="fl-page-sub">
        Platform-wide food recovery, claim performance and SDG-12 impact.
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(key="analytics_body"):
        _kpi_cards(stats)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1.45, 1])
        with c1:
            with st.container(key="chart_weekly"):
                _weekly_chart()
        with c2:
            with st.container(key="chart_status"):
                _status_donut()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        c3, c4 = st.columns([1.45, 1])
        with c3:
            with st.container(key="chart_category"):
                _category_chart()
        with c4:
            with st.container(key="chart_expiring"):
                _expiring_table()

        kg    = float(stats.get("total_kg_diverted", 0) or 0)
        meals = int(stats.get("total_meals_saved", 0) or 0)
        co2   = round(kg * 2.5, 1)

        # Pass 2+7: flat dark card, no gradient surface, sentence case label
        st.markdown(
            f'<div class="fl-impact-banner">'
            f'<div class="fl-impact-label">'
            f'{icon("leaf", 13)} Cumulative climate impact'
            f'</div>'
            f'<div class="fl-impact-value">{co2:,.1f} kg CO₂e avoided</div>'
            f'<div style="font-size:0.875rem;color:rgba(255,255,255,0.55);max-width:520px;line-height:1.6;">'
            f'Every kilogram rescued keeps edible food out of landfill and puts a warm meal '
            f'in front of someone in the Jalandhar–Phagwara corridor.'
            f'</div>'
            f'<div class="fl-impact-stats">'
            f'<div class="fl-impact-stat">'
            f'<b>{fmt_kg(kg)}</b><span>Food rescued</span>'
            f'</div>'
            f'<div class="fl-impact-stat">'
            f'<b>{fmt_num(meals)}</b><span>Meals saved</span>'
            f'</div>'
            f'<div class="fl-impact-stat">'
            f'<b>{fmt_num(stats.get("completed_pickups", 0))}</b><span>Pickups</span>'
            f'</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
