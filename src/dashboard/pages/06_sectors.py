import sys
from pathlib import Path
import time
# --------------------------------------------------------
# Add src folder to Python path
# --------------------------------------------------------

SRC_ROOT = Path(__file__).resolve().parents[2]

if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.utils.db import (
    get_sectors,
    get_companies,
    get_latest_financial_ratios,
)

# --------------------------------------------------------
# Page Config
# --------------------------------------------------------

st.set_page_config(
    page_title="Sector Analysis",
    layout="wide"
)
start_time = time.perf_counter()

st.title("🏭 Sector Analysis")

st.markdown(
    "Compare companies within each sector using "
    "Revenue, ROE and Market Capitalization."
)

# --------------------------------------------------------
# Load Data
# --------------------------------------------------------

ratios = get_latest_financial_ratios()
companies = get_companies()
sectors = get_sectors()

if ratios.empty:
    st.error("No financial ratio data found.")
    st.stop()

# --------------------------------------------------------
# Load Market Cap
# --------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

market_cap = pd.read_sql(
    """
    SELECT *
    FROM market_cap
    """,
    conn
)

conn.close()

# --------------------------------------------------------
# Keep latest market cap for each company
# --------------------------------------------------------

market_cap["year_num"] = (
    market_cap["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

market_cap = (
    market_cap
    .sort_values("year_num")
    .drop_duplicates(
        subset="company_id",
        keep="last"
    )
)

# --------------------------------------------------------
# Merge Everything
# --------------------------------------------------------

df = ratios.drop(columns=["id"], errors="ignore").merge(
    companies[
        [
            "id",
            "company_name"
        ]
    ],
    left_on="company_id",
    right_on="id",
    how="left"
)

df.drop(columns=["id"], inplace=True)

df = df.merge(
    sectors[
        [
            "company_id",
            "broad_sector",
            "sub_sector"
        ]
    ],
    on="company_id",
    how="left"
)

df = df.merge(
    market_cap[
        [
            "company_id",
            "market_cap_crore"
        ]
    ],
    on="company_id",
    how="left"
)

# --------------------------------------------------------
# Sector Selector
# --------------------------------------------------------

sector_list = sorted(
    df["broad_sector"]
    .dropna()
    .unique()
)

selected_sector = st.selectbox(
    "Select Sector",
    sector_list
)

sector_df = df[
    df["broad_sector"] == selected_sector
].copy()

if sector_df.empty:
    st.warning("No companies available.")
    st.stop()
# --------------------------------------------------------
# Bubble Chart
# --------------------------------------------------------

st.subheader("📊 Revenue vs ROE")

bubble_df = sector_df.copy()

bubble_df["market_cap_crore"] = (
    bubble_df["market_cap_crore"]
    .fillna(0)
)

fig = px.scatter(

    bubble_df,

    x="revenue_cr",

    y="return_on_equity_pct",

    size="market_cap_crore",

    color="sub_sector",

    hover_name="company_name",

    hover_data={

        "market_cap_crore": ":,.0f",

        "revenue_cr": ":,.0f",

        "return_on_equity_pct": ":.2f"

    },

    title=f"{selected_sector} Companies",

    size_max=50

)

fig.update_layout(

    xaxis_title="Revenue (Cr)",

    yaxis_title="ROE (%)",

    height=650,

    template="plotly_white"

)

st.plotly_chart(

    fig,

    width='stretch'

)

# --------------------------------------------------------
# Sector Median KPIs
# --------------------------------------------------------

st.markdown("---")

st.subheader("📈 Sector Median KPIs")

median_metrics = {

    "Revenue (Cr)": bubble_df["revenue_cr"].median(),

    "ROE (%)": bubble_df["return_on_equity_pct"].median(),

    "Net Profit (Cr)": bubble_df["net_profit_cr"].median(),

    "Debt/Equity": bubble_df["debt_to_equity"].median(),

    "FCF (Cr)": bubble_df["free_cash_flow_cr"].median(),

    "Composite Score": bubble_df["composite_quality_score"].median()

}

median_df = pd.DataFrame({

    "Metric": list(median_metrics.keys()),

    "Median": list(median_metrics.values())

})

bar = px.bar(

    median_df,

    x="Metric",

    y="Median",

    text="Median",

    title=f"{selected_sector} Median KPIs"

)

bar.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)

bar.update_layout(

    height=500,

    template="plotly_white"

)

st.plotly_chart(

    bar,

    width='stretch'

)

# --------------------------------------------------------
# Company Table
# --------------------------------------------------------

st.markdown("---")

st.subheader("🏢 Companies")

table_columns = [

    "company_name",

    "sub_sector",

    "revenue_cr",

    "return_on_equity_pct",

    "market_cap_crore",

    "net_profit_cr",

    "free_cash_flow_cr",

    "composite_quality_score"

]

table_columns = [

    c for c in table_columns

    if c in bubble_df.columns

]

display_df = bubble_df[table_columns]

display_df = display_df.sort_values(

    "market_cap_crore",

    ascending=False

)

st.dataframe(

    display_df,

    width='stretch',

    hide_index=True

)

# --------------------------------------------------------
# Download CSV
# --------------------------------------------------------

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(

    "📥 Download Sector Data",

    data=csv,

    file_name=f"{selected_sector}_sector_analysis.csv",

    mime="text/csv"

)
end_time = time.perf_counter()

st.caption(
    f"⚡ Page loaded in {end_time - start_time:.2f} seconds"
)
