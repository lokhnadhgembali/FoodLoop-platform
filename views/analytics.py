"""
views/analytics.py  -  FoodLoop Impact & Analytics
Accessible to every authenticated role.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import database
from utils import fmt_kg, fmt_num, format_countdown, is_urgent

BLUE = "#014BAA"
BLUE2 = "#0264E0"
EMERALD = "#10B981"
AMBER = "#F59E0B"
CORAL = "#D9381E"

STATUS_LABELS = {
    "pending": "Pending",
    "approved": "Approved",
    "completed": "Completed",
    "rejected": "Rejected",
}

CHART_FONT = dict(family="Plus Jakarta Sans, Inter, sans-serif", size=12, color="#475569")


def _sid(doc) -> str:
    return str(doc.get("_id", ""))


def _kpi_cards(stats):
    cards = [
        ("📦", fmt_num(stats.get("total_listings", 0)),                     "Total Listings"),
        ("✅", fmt_num(stats.get("completed_pickups", 0)),                  "Successful Pickups"),
        ("📬", fmt_num(stats.get("pending_requests", 0)),                   "Pending Requests"),
        ("⚖️", fmt_kg(float(stats.get("total_kg_diverted", 0) or 0)),       "Food Redistributed"),
    ]
    html = "".join(
        f'<div class="fl-kpi"><div class="fl-kpi-icon">{icon}</div>'
        f'<div class="fl-kpi-val">{val}</div>'
        f'<div class="fl-kpi-label">{label}</div></div>'
        for icon, val, label in cards
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
    st.markdown('<div class="fl-chart-title">📈 Weekly Collection Volume (kg)</div>',
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
    fig.update_traces(marker_line_width=0, opacity=0.92,
                      hovertemplate="%{x}<br><b>%{y:.1f} kg</b> collected<extra></extra>")
    fig.update_layout(xaxis=dict(showgrid=False, tickangle=-35),
                      yaxis=dict(gridcolor="rgba(1,75,170,0.07)", zeroline=False))
    _base_layout(fig, margin=dict(l=0, r=4, t=4, b=0))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _status_donut():
    st.markdown('<div class="fl-chart-title">🍩 Request Status Breakdown</div>',
                unsafe_allow_html=True)
    try:
        counts = database.get_request_status_counts() or {}
    except Exception as exc:
        st.info(f"Request data unavailable: {exc}")
        return

    df = pd.DataFrame(
        [{"Status": STATUS_LABELS.get(k, k.title()), "Count": v} for k, v in counts.items() if v]
    )
    if df.empty:
        st.info("No claims recorded yet.")
        return

    color_map = {"Pending": AMBER, "Approved": BLUE2, "Completed": EMERALD, "Rejected": CORAL}
    fig = px.pie(df, names="Status", values="Count", hole=0.55,
                 color="Status", color_discrete_map=color_map)
    fig.update_traces(textposition="outside", textinfo="percent",
                      marker=dict(line=dict(color="#FFFFFF", width=2)))
    _base_layout(fig, margin=dict(l=0, r=0, t=0, b=0))
    fig.update_layout(legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _category_chart():
    st.markdown('<div class="fl-chart-title">📦 Quantity Donated by Category (kg)</div>',
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
    fig.update_traces(marker_line_width=0, opacity=0.9,
                      hovertemplate="%{x}<br><b>%{y:.1f} kg</b><extra></extra>")
    fig.update_layout(xaxis=dict(showgrid=False),
                      yaxis=dict(gridcolor="rgba(1,75,170,0.07)", zeroline=False))
    _base_layout(fig, margin=dict(l=0, r=4, t=4, b=0))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _expiring_table():
    st.markdown('<div class="fl-chart-title">⏳ Soon-to-Expire Surplus</div>',
                unsafe_allow_html=True)
    try:
        listings = database.get_expiring_listings(hours=12) or []
    except Exception as exc:
        st.info(f"Expiry data unavailable: {exc}")
        return

    if not listings:
        st.success("✅ No listings expiring in the next 12 hours.")
        return

    rows = []
    for item in listings:
        rows.append({
            "Food":      item.get("food_name", "—"),
            "Category":  item.get("category", "—"),
            "Donor":     item.get("donor_name", "—"),
            "Qty (kg)":  round(float(item.get("remaining_qty_kg", 0) or 0), 1),
            "Time Left": format_countdown(item.get("pickup_deadline")),
            "Priority":  "🔴 URGENT" if is_urgent(item.get("pickup_deadline")) else "🟡 Soon",
        })
    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Qty (kg)": st.column_config.NumberColumn("Qty (kg)", format="%.1f"),
            "Priority": st.column_config.TextColumn("Priority", width="small"),
        },
    )


def render():
    try:
        stats = database.get_platform_stats() or {}
    except Exception:
        stats = {}

    st.markdown("""
    <div class="fl-page-head fl-wrap-wide">
      <h1 class="fl-page-title">📊 Impact &amp; Analytics</h1>
      <p class="fl-page-sub">
        Platform-wide food recovery, claim performance and SDG-12 impact — live from MongoDB.
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

        kg = float(stats.get("total_kg_diverted", 0) or 0)
        meals = int(stats.get("total_meals_saved", 0) or 0)
        co2 = round(kg * 2.5, 1)
        st.markdown(f"""
        <div class="fl-impact-banner">
          <div class="fl-impact-label">🌍 Cumulative Climate Impact</div>
          <div class="fl-impact-value">{co2:,.1f} kg CO₂e avoided</div>
          <div style="font-size:0.92rem;opacity:.85;max-width:560px;line-height:1.6;">
            Every kilogram rescued keeps edible food out of landfill and puts a warm meal
            in front of someone in the Jalandhar–Phagwara corridor.
          </div>
          <div class="fl-impact-stats">
            <div class="fl-impact-stat"><b>{fmt_kg(kg)}</b><span>Food Rescued</span></div>
            <div class="fl-impact-stat"><b>{fmt_num(meals)}</b><span>Meals Saved</span></div>
            <div class="fl-impact-stat"><b>{fmt_num(stats.get('completed_pickups', 0))}</b><span>Pickups</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
