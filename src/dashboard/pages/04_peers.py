import sys
from pathlib import Path
import time
SRC_ROOT = Path(__file__).resolve().parents[2]

if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from dashboard.utils.db import (
    get_peer_group_names,
    get_peer_group_companies,
    get_latest_company_ratios,
)
start_time = time.perf_counter()
st.title("👥 Peer Comparison")

# ---------------------------------
# Peer Group
# ---------------------------------

groups = get_peer_group_names()

group = st.selectbox(
    "Peer Group",
    groups["peer_group_name"].tolist()
)

# ---------------------------------
# Companies in selected group
# ---------------------------------

companies = get_peer_group_companies(group)

company = st.selectbox(
    "Company",
    companies["company_id"].tolist()
)

company_ids = companies["company_id"].tolist()

ratios = get_latest_company_ratios(company_ids)

if ratios.empty:
    st.warning("No financial ratio data found.")
    st.stop()

# ---------------------------------
# Radar Chart
# ---------------------------------

metrics = [
    "return_on_equity_pct",
    "return_on_capital_employed",
    "net_profit_margin_pct",
    "asset_turnover",
    "interest_coverage",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "composite_quality_score",
]

peer_avg = ratios[metrics].mean(numeric_only=True)

company_df = ratios[ratios["company_id"] == company]

if company_df.empty:
    st.warning("Selected company has no ratio data.")
    st.stop()

company_data = company_df.iloc[0]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=[company_data[m] for m in metrics],
        theta=metrics,
        fill="toself",
        name=company,
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=[peer_avg[m] for m in metrics],
        theta=metrics,
        fill="toself",
        name="Peer Average",
    )
)

fig.update_layout(
    title=f"{company} vs Peer Average",
    polar=dict(radialaxis=dict(visible=True)),
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# KPI Table
# ---------------------------------

table = ratios[
    ["company_id"] + metrics
].copy()

benchmark_company = companies.loc[
    companies["is_benchmark"] == 1,
    "company_id",
].iloc[0]

table.insert(
    1,
    "Benchmark",
    table["company_id"] == benchmark_company,
)

st.subheader("Peer Comparison Table")

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True,
)
end_time = time.perf_counter()

st.caption(
    f"⚡ Page loaded in {end_time - start_time:.2f} seconds"
)