import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2]

if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

import streamlit as st
import pandas as pd

from dashboard.utils.db import (
    get_companies,
    get_documents,
)

st.set_page_config(
    page_title="Annual Reports",
    layout="wide",
)

st.title("📄 Annual Reports")

st.markdown(
    """
Browse annual reports available for each company.
"""
)

# --------------------------------------------------
# Load Companies
# --------------------------------------------------

companies = get_companies()

if companies.empty:

    st.error("No companies found.")

    st.stop()

company_name = st.selectbox(

    "Select Company",

    companies["company_name"].sort_values()

)

company_id = companies.loc[
    companies["company_name"] == company_name,
    "id"
].iloc[0]

documents = get_documents(company_id)

if documents.empty:

    st.warning("No reports available.")

    st.stop()
# --------------------------------------------------
# Detect URL Column
# --------------------------------------------------

possible_url_columns = [

    "bse_pdf_link",
    "pdf_url",
    "document_url",
    "bse_link",
    "url",
    "link",
    "annual_report"

]

url_column = None

for col in possible_url_columns:

    if col in documents.columns:

        url_column = col

        break

if url_column is None:

    st.error(
        "No PDF link column found in documents table."
    )

    st.stop()

# --------------------------------------------------
# Detect Year Column
# --------------------------------------------------

year_column = "year"

if year_column not in documents.columns:

    st.error("Year column missing.")

    st.stop()

documents = documents.sort_values(

    year_column,

    ascending=False

)

st.subheader("Available Reports")

rows = []

for _, row in documents.iterrows():

    year = row[year_column]

    url = row[url_column]

    if pd.isna(url) or str(url).strip() == "":

        status = "🔴 Report Unavailable"

        link = ""

    else:

        status = "🟢 Available"

        link = url

    rows.append({

        "Year": year,

        "Status": status,

        "PDF Link": link

    })

display_df = pd.DataFrame(rows)

# --------------------------------------------------
# Display Reports
# --------------------------------------------------

for _, row in display_df.iterrows():

    col1, col2, col3 = st.columns([2, 2, 6])

    col1.write(row["Year"])

    if row["Status"] == "🟢 Available":

        col2.success("Available")

        col3.link_button(
            "📥 Open PDF",
            row["PDF Link"]
        )

    else:

        col2.error("Unavailable")

        col3.write("—")

# --------------------------------------------------
# Download
# --------------------------------------------------

csv = display_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(

    "📥 Download Report List",

    csv,

    f"{company_id}_reports.csv",

    "text/csv",

)