import sys
from pathlib import Path

# --------------------------------------------------------
# Add src folder to Python path
# --------------------------------------------------------

SRC_ROOT = Path(__file__).resolve().parents[2]

if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from dashboard.utils.db import (
    get_companies,
    get_ratios,
)

st.set_page_config(
    page_title="Trend Analysis",
    layout="wide"
)

st.title("📈 Trend Analysis")

st.markdown(
    "Compare up to **3 financial metrics** over the last 10 years."
)

# --------------------------------------------------------
# Load Companies
# --------------------------------------------------------

companies = get_companies()

if companies.empty:
    st.error("No companies found.")
    st.stop()

company_names = (
    companies["company_name"]
    .sort_values()
    .tolist()
)

selected_company = st.selectbox(
    "Select Company",
    company_names
)

company_id = companies.loc[
    companies["company_name"] == selected_company,
    "id"
].iloc[0]

# --------------------------------------------------------
# Load Historical Ratios
# --------------------------------------------------------

df = get_ratios(company_id)

if df.empty:
    st.warning("No historical financial ratios found.")
    st.stop()

# --------------------------------------------------------
# Convert Year
# --------------------------------------------------------

df["year_num"] = (
    df["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
    .astype(int)
)

df = (
    df
    .sort_values("year_num")
    .drop_duplicates(
        subset="year_num",
        keep="last"
    )
)

# --------------------------------------------------------
# Metrics
# --------------------------------------------------------

metric_map = {

    "Revenue (Cr)": "revenue_cr",

    "Net Profit (Cr)": "net_profit_cr",

    "ROE (%)": "return_on_equity_pct",

    "EPS": "earnings_per_share",

    "Book Value / Share": "book_value_per_share",

    "FCF (Cr)": "free_cash_flow_cr",

    "Operating Margin (%)":
        "operating_profit_margin_pct",

    "Debt / Equity":
        "debt_to_equity",

    "Interest Coverage":
        "interest_coverage",

    "Composite Score":
        "composite_quality_score",

}

selected_metrics = st.multiselect(

    "Select up to 3 metrics",

    list(metric_map.keys()),

    default=["Revenue (Cr)"],

    max_selections=3

)

if not selected_metrics:
    st.info("Please select at least one metric.")
    st.stop()

fig = go.Figure()
# --------------------------------------------------------
# Plot Selected Metrics
# --------------------------------------------------------

for metric_name in selected_metrics:

    column = metric_map[metric_name]

    if column not in df.columns:
        continue

    plot_df = df[
        ["year_num", column]
    ].copy()

    plot_df = plot_df.dropna()

    if plot_df.empty:
        continue

    plot_df = plot_df.sort_values(
        "year_num"
    )

    fig.add_trace(

        go.Scatter(

            x=plot_df["year_num"],

            y=plot_df[column],

            mode="lines+markers",

            name=metric_name,

            hovertemplate=(
                "<b>%{x}</b><br>"
                + metric_name
                + ": %{y:.2f}<extra></extra>"
            )

        )

    )

    # ----------------------------------------------------
    # YoY Annotation
    # ----------------------------------------------------

    values = plot_df[column].tolist()
    years = plot_df["year_num"].tolist()

    for i in range(1, len(values)):

        previous = values[i - 1]
        current = values[i]

        if (
            previous is None
            or previous == 0
            or pd.isna(previous)
            or pd.isna(current)
        ):
            continue

        yoy = (
            (current - previous)
            / previous
        ) * 100

        fig.add_annotation(

            x=years[i],

            y=current,

            text=f"{yoy:+.1f}%",

            showarrow=False,

            yshift=12,

            font=dict(
                size=10
            )

        )


# --------------------------------------------------------
# Chart Layout
# --------------------------------------------------------

fig.update_layout(

    title=f"{selected_company} — Financial Trends",

    xaxis_title="Year",

    yaxis_title="Value",

    template="plotly_white",

    hovermode="x unified",

    legend=dict(
        orientation="h",
        y=1.12
    ),

    height=650

)


st.plotly_chart(

    fig,

    use_container_width=True

)


# --------------------------------------------------------
# Historical Table
# --------------------------------------------------------

st.markdown("---")

st.subheader("Historical Data")


table_columns = [

    "year",

]

for metric in selected_metrics:

    col = metric_map[metric]

    if col in df.columns:

        table_columns.append(col)


table_df = df[
    table_columns
].copy()

table_df = table_df.sort_values(
    "year_num",
    ascending=False
)

st.dataframe(

    table_df,

    use_container_width=True,

    hide_index=True

)


# --------------------------------------------------------
# Download CSV
# --------------------------------------------------------

csv = (
    table_df
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(

    label="📥 Download Trend Data",

    data=csv,

    file_name=f"{company_id}_trend_analysis.csv",

    mime="text/csv"

)