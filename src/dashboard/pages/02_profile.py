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

st.title("🏢 Company Profile")

companies = search_companies()

company_id_key = "company_id" if "company_id" in companies.columns else "id"
ticker_key = "ticker" if "ticker" in companies.columns else company_id_key

company_options = {
    f"{row[ticker_key]} - {row['company_name']}": row[company_id_key]
    for _, row in companies.iterrows()
}

selected = st.selectbox("Search Company", list(company_options.keys()))
company_id = company_options[selected]

company = get_company(company_id)
ratios = get_company_ratios(company_id)
pl = get_pl(company_id)
sector = get_sectors()

if company.empty:
    st.error("Ticker not found — please try another.")
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


month_map = {
    "Mar": 3,
    "Jun": 6,
    "Sep": 9,
    "Dec": 12,
}

pl["sort_year"] = (
    pl["year"].astype(str).str[-4:].astype(int) * 100
    + pl["year"].astype(str).str[:3].map(month_map)
)
pl = pl.sort_values("sort_year").drop_duplicates(subset="year", keep="last")

ratios["sort_year"] = (
    ratios["year"].astype(str).str[-4:].astype(int) * 100
    + ratios["year"].astype(str).str[:3].map(month_map)
)
ratios = ratios.sort_values("sort_year").drop_duplicates(subset="year", keep="last")

if len(pl) < 10:
    st.info(f"Only {len(pl)} years of financial data are available.")

latest = ratios.iloc[-1]

c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

c1.metric("ROE", fmt(latest["return_on_equity_pct"], "%"))
c2.metric("ROCE", fmt(latest["return_on_capital_employed"], "%"))
c3.metric("Net Profit Margin", fmt(latest["net_profit_margin_pct"], "%"))
c4.metric("Debt / Equity", fmt(latest["debt_to_equity"]))
c5.metric("Revenue CAGR", fmt(latest["revenue_cagr_5yr"], "%"))
c6.metric("Free Cash Flow", f"₹ {fmt(latest['free_cash_flow_cr']).replace('N/A', 'N/A')} Cr")

fig = px.bar(
    pl,
    x="year",
    y=["sales", "net_profit"],
    barmode="group",
    title="Revenue vs Net Profit",
)

st.plotly_chart(fig, use_container_width=True)

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
    yaxis_title="ROE (%)",
    yaxis2_title="ROCE (%)",
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)
pros = get_pros_cons(company_id)

if not pros.empty:
    st.subheader("Pros & Cons")

    if "pros" in pros.columns:
        st.success(pros.iloc[0]["pros"])

    if "cons" in pros.columns:
        st.error(pros.iloc[0]["cons"])
