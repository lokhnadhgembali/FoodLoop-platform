"""
views/analytics.py  –  FoodLoop Platform Analytics
Available to all authenticated users.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import database
from utils import fmt_kg, fmt_num, format_countdown, is_urgent

BLUE = "#014BAA"
BLUE2 = "#0264E0"
CORAL = "#D9381E"
CREAM = "#F8F3F0"

def render():
    st.markdown("""
    <div style="padding:24px 32px 8px;">
      <h1 style="font-size:2rem;font-weight:900;color:#0F172A;margin:0;">📊 Impact Analytics</h1>
      <p style="color:#64748B;margin-top:4px;">Real-time platform performance metrics and SDG impact tracking.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Strip ─────────────────────────────────────────────────────────────
    stats = database.get_platform_stats()
    kpis = [
        ("🍽️", "Total Meals Saved",     fmt_num(stats.get("total_meals_saved", 0)),   "#014BAA"),
        ("⚖️", "Food Diverted",         fmt_kg(stats.get("total_kg_diverted", 0.0)),  "#059669"),
        ("📦", "Active Listings",        str(stats.get("active_listings", 0)),          "#7C3AED"),
        ("✅", "Completed Pickups",      str(stats.get("completed_pickups", 0)),        "#D97706"),
    ]
    cols = st.columns(4)
    for col, (icon, label, val, color) in zip(cols, kpis):
        col.markdown(f"""
        <div style="background:white;border-radius:16px;border:1px solid rgba(1,75,170,0.08);
             box-shadow:0 8px 30px rgba(1,75,170,0.06);padding:20px;text-align:center;margin:4px;">
          <div style="font-size:1.6rem;margin-bottom:6px;">{icon}</div>
          <div style="font-size:1.5rem;font-weight:900;color:{color};">{val}</div>
          <div style="font-size:0.78rem;font-weight:600;color:#64748B;margin-top:4px;">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts Row 1 ─────────────────────────────────────────────────────────
    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown("#### 📈 Weekly Donation Trend")
        weekly = database.get_weekly_trend()
        if weekly:
            df_w = pd.DataFrame(weekly)
            # expected keys: week_label (str), kg_donated (float), pickups (int)
            if "week_label" in df_w.columns and "kg_donated" in df_w.columns:
                fig = px.bar(df_w, x="week_label", y="kg_donated",
                             color_discrete_sequence=[BLUE],
                             labels={"week_label": "Week", "kg_donated": "Kg Donated"})
                fig.update_layout(
                    plot_bgcolor="white", paper_bgcolor="white",
                    margin=dict(l=10, r=10, t=10, b=10),
                    font=dict(family="Plus Jakarta Sans, Inter, sans-serif"),
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Weekly trend data format mismatch.")
        else:
            st.info("No weekly trend data available yet.")

    with ch2:
        st.markdown("#### 🍩 Request Status Breakdown")
        status_counts = database.get_request_status_counts()
        if status_counts:
            df_s = pd.DataFrame(list(status_counts.items()), columns=["Status", "Count"])
            fig2 = px.pie(df_s, names="Status", values="Count", hole=0.55,
                          color_discrete_sequence=[BLUE, "#60A5FA", "#059669", CORAL])
            fig2.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                margin=dict(l=10, r=10, t=10, b=10),
                font=dict(family="Plus Jakarta Sans, Inter, sans-serif"),
                legend=dict(orientation="h", y=-0.1),
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No request data yet.")

    # ── Charts Row 2 ─────────────────────────────────────────────────────────
    ch3, ch4 = st.columns(2)

    with ch3:
        st.markdown("#### 📦 Food Category Breakdown")
        cat_data = database.get_category_totals()
        if cat_data:
            df_c = pd.DataFrame(cat_data)
            # expected keys: category (str), total_kg (float)
            if "category" in df_c.columns and "total_kg" in df_c.columns:
                fig3 = px.bar(df_c.sort_values("total_kg"), x="total_kg", y="category",
                              orientation="h", color_discrete_sequence=[BLUE2],
                              labels={"total_kg": "Total kg", "category": "Category"})
                fig3.update_layout(
                    plot_bgcolor="white", paper_bgcolor="white",
                    margin=dict(l=10, r=10, t=10, b=10),
                    font=dict(family="Plus Jakarta Sans, Inter, sans-serif"),
                    showlegend=False,
                )
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("Category data format mismatch.")
        else:
            st.info("No category data yet.")

    with ch4:
        st.markdown("#### ⏰ Expiring Soon (Next 3 Hours)")
        expiring = database.get_expiring_listings()
        if expiring:
            rows = []
            for item in expiring:
                urgent = is_urgent(item.get("pickup_deadline"))
                rows.append({
                    "Food": item.get("food_name", "Unknown"),
                    "Category": item.get("category", ""),
                    "Qty (kg)": item.get("quantity_kg", 0),
                    "Deadline": format_countdown(item.get("pickup_deadline")),
                    "⚠️": "🔴 URGENT" if urgent else "🟡 Soon",
                })
            df_e = pd.DataFrame(rows)
            st.dataframe(df_e, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No listings expiring in the next 3 hours.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CO2e Impact Banner ────────────────────────────────────────────────────
    kg_total = stats.get("total_kg_diverted", 0.0)
    co2_saved = round(kg_total * 2.5, 1)
    meals = stats.get("total_meals_saved", 0)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#014BAA 0%,#0264E0 100%);border-radius:20px;
         padding:32px 40px;text-align:center;margin:16px 4px;color:white;">
      <div style="font-size:1.1rem;font-weight:700;opacity:0.9;margin-bottom:8px;">
        🌍 Cumulative Climate Impact
      </div>
      <div style="font-size:3rem;font-weight:900;letter-spacing:-1px;">{co2_saved} kg CO₂e</div>
      <div style="font-size:1rem;opacity:0.8;margin-top:6px;">
        Avoided by redistributing {fmt_kg(kg_total)} of food — equivalent to {fmt_num(meals)} meals saved.
      </div>
    </div>
    """, unsafe_allow_html=True)
