import sys
import pathlib
SRC_ROOT = pathlib.Path(__file__).resolve().parents[2]

if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

import streamlit as st
import pandas as pd

from dashboard.utils.db import (
    get_latest_ratios,
    get_companies,
    get_sectors,
)

from screener.engine import ScreenerEngine

st.title("📊 Financial Screener")

# -------------------------------------------------
# Load Data
# -------------------------------------------------

df = get_latest_ratios()
companies = get_companies()
sectors = get_sectors()

company_lookup = (
    companies[["id", "company_name"]]
    .drop_duplicates(subset=["id"])
)

df = df.merge(
    company_lookup,
    left_on="company_id",
    right_on="id",
    how="left",
)

if "id" in df.columns:
    df.drop(columns=["id"], inplace=True)

df = df.merge(
    sectors[["company_id", "broad_sector"]],
    on="company_id",
    how="left",
)

# -------------------------------------------------
# Column normalization (to match ScreenerEngine expectations)
# -------------------------------------------------

# Map common alternate column names -> engine-expected names.
# Only renames when the target column does not already exist.
rename_map = {
    # ROE
    "return_on_equity": "return_on_equity_pct",
    "roe": "return_on_equity_pct",
    # Debt / Equity
    "debt_equity": "debt_to_equity",
    "debt_to_equity_ratio": "debt_to_equity",
    # FCF
    "free_cashflow_cr": "free_cash_flow_cr",
    "free_cash_flow": "free_cash_flow_cr",
    # Market multiples
    "pe": "pe_ratio",
    "price_earnings": "pe_ratio",
    "p_e_ratio": "pe_ratio",
    "pb": "pb_ratio",
    "price_book": "pb_ratio",
    # Dividend
    "dividend_yield": "dividend_yield_pct",
    "dividend_yield_percent": "dividend_yield_pct",
    # Operating margin
    "operating_margin": "operating_profit_margin_pct",
    "op_margin": "operating_profit_margin_pct",
}

for src_col, dst_col in rename_map.items():
    if src_col in df.columns and dst_col not in df.columns:
        df = df.rename(columns={src_col: dst_col})

# Ensure numeric columns used by filtering are at least coercible.
for col in [
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "operating_profit_margin_pct",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct",
    "interest_coverage",
]:
    if col in df.columns:
        # errors='ignore' can keep objects/strings; use coercion to keep filtering stable.
        df[col] = pd.to_numeric(df[col], errors="coerce")


# Warn if the dataframe is missing many expected columns.
expected_cols = [
    "company_id",
    "broad_sector",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "operating_profit_margin_pct",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct",
    "interest_coverage",
]

missing = [c for c in expected_cols if c not in df.columns]
if len(missing) > 6:
    st.warning(
        "Some expected financial columns are missing from the screener dataset. "
        "Results may be empty or less accurate. "
        f"Missing: {missing[:8]}" + (" ..." if len(missing) > 8 else "")
    )

engine = ScreenerEngine(df)


# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------

st.sidebar.header("Filters")

filters = {
    "roe_min": st.sidebar.slider(
        "ROE Min (%)",
        0.0, 50.0, 0.0
    ),

    "debt_to_equity_max": st.sidebar.slider(
        "Debt / Equity Max",
        0.0, 10.0, 10.0
    ),

    "free_cash_flow_min": st.sidebar.number_input(
        "FCF Min (Cr)",
        value=-100000.0
    ),

    "revenue_cagr_5yr_min": st.sidebar.slider(
        "Revenue CAGR Min (%)",
        -100.0, 50.0, -100.0
    ),

    "pat_cagr_5yr_min": st.sidebar.slider(
        "PAT CAGR Min (%)",
        -100.0, 50.0, -100.0
    ),

    "operating_profit_margin_min": st.sidebar.slider(
        "OPM Min (%)",
        -100.0, 50.0, -100.0
    ),

    "pe_max": st.sidebar.slider(
        "P/E Max",
        0.0, 1000.0, 1000.0
    ),

    "pb_max": st.sidebar.slider(
        "P/B Max",
        0.0, 100.0, 100.0
    ),

    "dividend_yield_min": st.sidebar.slider(
        "Dividend Yield Min (%)",
        0.0, 10.0, 0.0
    ),

    "interest_coverage_min": st.sidebar.slider(
        "Interest Coverage Min",
        -100.0, 20.0, -100.0
    ),
}
engine.update_filters(filters)

# -------------------------------------------------
# Preset Screeners
# -------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.subheader("Preset Screeners")

preset = None

c1, c2 = st.sidebar.columns(2)

if c1.button("Quality"):
    preset = "quality_compounder"

if c2.button("Value"):
    preset = "value_pick"

c3, c4 = st.sidebar.columns(2)

if c3.button("Growth"):
    preset = "growth_accelerator"

if c4.button("Dividend"):
    preset = "dividend_champion"

c5, c6 = st.sidebar.columns(2)

if c5.button("Debt-Free"):
    preset = "debt_free_blue_chip"

if c6.button("Turnaround"):
    preset = "turnaround_watch"

# -------------------------------------------------
# Apply Filters
# -------------------------------------------------

if preset:
    results = engine.apply_preset(preset)
else:
    results = engine.apply_filters()

# -------------------------------------------------
# Results
# -------------------------------------------------

st.subheader(f"📈 {len(results)} companies match your filters")

display_columns = [
    "company_id",
    "company_name",
    "broad_sector",
    "composite_quality_score",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "operating_profit_margin_pct",
    "interest_coverage",
]

available_columns = [
    c for c in display_columns if c in results.columns
]

display_df = results[available_columns]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download CSV",
    data=csv,
    file_name="screener_results.csv",
    mime="text/csv",
)