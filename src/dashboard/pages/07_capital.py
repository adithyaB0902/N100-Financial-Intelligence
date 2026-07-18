import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2]

if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.utils.db import (
    get_latest_financial_ratios,
    get_companies,
)

st.set_page_config(
    page_title="Capital Allocation",
    layout="wide",
)

st.title("💰 Capital Allocation Map")

st.markdown(
    """
Visualise all companies based on their
capital allocation strategy.
"""
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

ratios = get_latest_financial_ratios()
companies = get_companies()

if ratios.empty:

    st.error("Financial ratios not found.")

    st.stop()

df = ratios.merge(

    companies[
        [
            "id",
            "company_name",
        ]
    ],

    left_on="company_id",

    right_on="id",

    how="left",

)

if "id" in df.columns:

    df.drop(columns="id", inplace=True)

# --------------------------------------------------
# Clean Pattern
# --------------------------------------------------

df["capital_allocation_pattern"] = (

    df["capital_allocation_pattern"]

    .fillna("Unclassified")

)

patterns = sorted(

    df["capital_allocation_pattern"]

    .unique()

)
# --------------------------------------------------
# Treemap
# --------------------------------------------------

fig = px.treemap(

    df,

    path=[
        "capital_allocation_pattern",
        "company_name",
    ],

    values="revenue_cr",

    color="composite_quality_score",

    color_continuous_scale="RdYlGn",

    hover_data=[

        "return_on_equity_pct",

        "free_cash_flow_cr",

        "net_profit_cr",

    ],

)

fig.update_layout(

    margin=dict(

        t=40,

        l=10,

        r=10,

        b=10,

    )

)

st.plotly_chart(

    fig,

    use_container_width=True,

)

# --------------------------------------------------
# Pattern Selector
# --------------------------------------------------

st.markdown("---")

selected_pattern = st.selectbox(

    "Capital Allocation Pattern",

    patterns,

)

filtered = df[

    df["capital_allocation_pattern"]

    == selected_pattern

]

st.subheader(

    f"{len(filtered)} Companies"

)

display_columns = [

    "company_name",

    "revenue_cr",

    "net_profit_cr",

    "return_on_equity_pct",

    "free_cash_flow_cr",

    "composite_quality_score",

]

display_columns = [

    c

    for c in display_columns

    if c in filtered.columns

]

display_df = filtered[display_columns]

display_df = display_df.sort_values(

    "composite_quality_score",

    ascending=False,

)

st.dataframe(

    display_df,

    hide_index=True,

    use_container_width=True,

)

# --------------------------------------------------
# Download
# --------------------------------------------------

csv = display_df.to_csv(

    index=False

).encode("utf-8")

st.download_button(

    "📥 Download Pattern",

    csv,

    f"{selected_pattern}.csv",

    "text/csv",

)
