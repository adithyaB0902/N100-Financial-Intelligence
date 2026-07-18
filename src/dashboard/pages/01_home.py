import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from utils.db import get_latest_ratios, get_sectors
import streamlit as st
import plotly.express as px

st.title("🏠 Home Dashboard")

# Sidebar
year = st.sidebar.selectbox(
    "Financial Year",
    [2024, 2023, 2022, 2021, 2020, 2019],
)

# Load data
ratios = get_latest_ratios(year)
sectors = get_sectors()

if ratios.empty:
    st.warning("No financial data available.")
    st.stop()

# ======================
# KPI SECTION
# ======================

st.subheader(f"📊 Summary ({year})")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

col1.metric(
    "Average ROE",
    f"{ratios['return_on_equity_pct'].mean():.2f}%"
)

col2.metric(
    "Median D/E",
    f"{ratios['debt_to_equity'].median():.2f}"
)

col3.metric(
    "Average ROCE",
    f"{ratios['return_on_capital_employed'].mean():.2f}%"
)

col4.metric(
    "Total Companies",
    ratios["company_id"].nunique()
)

col5.metric(
    "Median Revenue CAGR",
    f"{ratios['revenue_cagr_5yr'].median():.2f}%"
)

col6.metric(
    "Debt-Free Companies",
    int((ratios["debt_to_equity"] == 0).sum())
)

# ======================
# SECTOR DONUT CHART
# ======================

st.divider()

st.subheader("🏭 Sector Distribution")

sector_counts = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_counts,
    names="broad_sector",
    values="Companies",
    hole=0.45,
    title="Sector Distribution",
)

st.plotly_chart(fig, use_container_width=True)

# ======================
# TOP 5 QUALITY COMPANIES
# ======================

st.divider()

st.subheader("🏆 Top 5 Companies by Composite Quality Score")

top5 = (
    ratios.sort_values(
        by="composite_quality_score",
        ascending=False,
    )[
        [
            "company_id",
            "return_on_equity_pct",
            "return_on_capital_employed",
            "revenue_cagr_5yr",
            "composite_quality_score",
        ]
    ]
    .head(5)
)

top5.columns = [
    "Company",
    "ROE %",
    "ROCE %",
    "Revenue CAGR %",
    "Quality Score",
]

st.dataframe(
    top5,
    use_container_width=True,
    hide_index=True,
)