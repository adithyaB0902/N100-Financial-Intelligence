import streamlit as st
import plotly.express as px
from utils.db import get_latest_ratios, get_sectors

st.title("🏠 Home Dashboard")

year = st.sidebar.selectbox(
    "Financial Year",
    [2024, 2023, 2022, 2021, 2020, 2019],
)

ratios = get_latest_ratios(year)
sectors = get_sectors()

st.subheader(f"Summary ({year})")

if ratios.empty:
    st.warning("No financial ratio data available.")
    st.stop()

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

col1.metric("Average ROE", f"{ratios['return_on_equity_pct'].mean():.2f}%")
col2.metric("Median P/E", f"{ratios['price_to_earnings'].median():.2f}")
col3.metric("Median D/E", f"{ratios['debt_to_equity'].median():.2f}")

col4.metric("Companies", len(ratios))
col5.metric("Median Revenue CAGR", f"{ratios['revenue_cagr_5yr'].median():.2f}%")
col6.metric("Debt-Free", (ratios["debt_to_equity"] == 0).sum())

st.divider()

sector_counts = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_counts,
    names="broad_sector",
    values="Companies",
    hole=0.5,
    title="Sector Distribution",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Top 5 Quality Companies")

top5 = ratios.sort_values(
    "composite_quality_score",
    ascending=False,
).head(5)

st.dataframe(top5, use_container_width=True)