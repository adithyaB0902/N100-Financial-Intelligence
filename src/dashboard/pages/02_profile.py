import sys
from pathlib import Path
import time
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.db import (
    search_companies,
    get_company,
    get_company_ratios,
    get_pl,
    get_sectors,
    get_pros_cons,
)
start_time = time.perf_counter()
st.title("🏢 Company Profile")

companies = search_companies()

company_id_key = "company_id" if "company_id" in companies.columns else "id"
company_options = {
    f"{row[company_id_key]} - {row['company_name']}": row[company_id_key]
    for _, row in companies.iterrows()
}

selected = st.selectbox("Search Company", list(company_options.keys()))
company_id = company_options[selected]

company = get_company(company_id)
ratios = get_company_ratios(company_id)
pl = get_pl(company_id)
sector = get_sectors()

if company.empty:
    st.error("Company not found — please try another.")
    st.stop()

if ratios.empty:
    st.warning("No financial ratio data is available for this company yet.")
    st.stop()

company = company.iloc[0]

sector_info = sector[sector["company_id"] == company_id]

col1, col2 = st.columns([1, 3])

with col1:
    st.image(company["company_logo"], width=120)

with col2:
    st.subheader(company["company_name"])

    if not sector_info.empty:
        st.write(
            f"**Sector:** {sector_info.iloc[0]['broad_sector']}"
        )
        st.write(
            f"**Sub Sector:** {sector_info.iloc[0]['sub_sector']}"
        )

    st.write(company["about_company"])

    st.markdown(f"[🌐 Website]({company['website']})")


def fmt(value, suffix=""):
    if value is None:
        return "N/A"
    try:
        if str(value) == "nan":
            return "N/A"
    except Exception:
        pass
    return f"{value:.2f}{suffix}"


def parse_years(df):
    df = df[df["year"].str.contains(r"\d{4}", na=False)].copy()
    df["year_num"] = (
        df["year"].str.extract(r"(\d{4})").astype(int)
    )
    return df.sort_values("year_num")

pl = parse_years(pl)
ratios = parse_years(ratios)

if len(pl) < 10:
    st.info(f"Only {len(pl)} years of financial data are available.")

latest = ratios.iloc[-1]

c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

metric_values = {
    "ROE": latest.get("return_on_equity_pct"),
    "ROCE": latest.get("return_on_capital_employed"),
    "Net Profit Margin": latest.get("net_profit_margin_pct"),
    "Debt / Equity": latest.get("debt_to_equity"),
    "Revenue CAGR": latest.get("revenue_cagr_5yr"),
    "Free Cash Flow": latest.get("free_cash_flow_cr"),
}

c1.metric("ROE", fmt(metric_values["ROE"], "%"))
c2.metric("ROCE", fmt(metric_values["ROCE"], "%"))
c3.metric("Net Profit Margin", fmt(metric_values["Net Profit Margin"], "%"))
c4.metric("Debt / Equity", fmt(metric_values["Debt / Equity"]))
c5.metric("Revenue CAGR", fmt(metric_values["Revenue CAGR"], "%"))
c6.metric("Free Cash Flow", f"₹ {fmt(metric_values['Free Cash Flow']).replace('N/A', 'N/A')} Cr")

if not pl.empty and {"sales", "net_profit"}.issubset(pl.columns):
    fig = px.bar(
        pl,
        x="year",
        y=["sales", "net_profit"],
        barmode="group",
        title="Revenue vs Net Profit",
    )
    st.plotly_chart(fig, width='stretch')
else:
    st.info("P/L chart data is unavailable for this company.")

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=ratios["year"],
        y=ratios["return_on_equity_pct"],
        mode="lines+markers",
        name="ROE (%)",
        yaxis="y",
    )
)
fig.add_trace(
    go.Scatter(
        x=ratios["year"],
        y=ratios["return_on_capital_employed"],
        mode="lines+markers",
        name="ROCE (%)",
        yaxis="y2",
    )
)
fig.update_layout(
    title="ROE vs ROCE",
    xaxis_title="Year",
    yaxis=dict(title="ROE (%)"),
    yaxis2=dict(
        title="ROCE (%)",
        overlaying="y",
        side="right",
    ),
    template="plotly_white",
)

st.plotly_chart(fig, width='stretch')
pros = get_pros_cons(company_id)

if not pros.empty:
    st.subheader("Pros & Cons")

    if "pros" in pros.columns:
        st.success(pros.iloc[0]["pros"])

    if "cons" in pros.columns:
        st.error(pros.iloc[0]["cons"])
end_time = time.perf_counter()

st.caption(
    f"⚡ Page loaded in {end_time - start_time:.2f} seconds"
)
