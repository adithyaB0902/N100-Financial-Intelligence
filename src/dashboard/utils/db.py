import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def run_query(query, params=None):
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)
@st.cache_data(ttl=600)
def get_companies():
    return run_query(
        """
        SELECT *
        FROM companies
        ORDER BY company_name
        """
    )


@st.cache_data(ttl=600)
def search_companies():
    return run_query(
        """
        SELECT
            id,
            company_name
        FROM companies
        ORDER BY company_name
        """
    )


@st.cache_data(ttl=600)
def get_company(company_id):
    return run_query(
        """
        SELECT *
        FROM companies
        WHERE id = ?
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_ratios(company_id, year=None):
    query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
    """

    params = [company_id]

    if year is not None:
        query += " AND year LIKE ?"
        params.append(f"%{year}")

    query += " ORDER BY year DESC"

    return run_query(query, params)


@st.cache_data(ttl=600)
def get_company_ratios(company_id):

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year
    """

    df = run_query(query, [company_id])

    if df.empty:
        return df

    df = df.drop_duplicates(
        subset=["year"],
        keep="last"
    )

    return df


@st.cache_data(ttl=600)
def get_pl(company_id):
    return run_query(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year DESC
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_bs(company_id):
    return run_query(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        ORDER BY year DESC
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_cf(company_id):
    return run_query(
        """
        SELECT *
        FROM cashflow
        WHERE company_id=?
        ORDER BY year DESC
        """,
        [company_id],
    )
@st.cache_data(ttl=600)
def get_sectors():
    return run_query(
        """
        SELECT *
        FROM sectors
        ORDER BY broad_sector
        """
    )


@st.cache_data(ttl=600)
def get_peers(group_name):
    return run_query(
        """
        SELECT *
        FROM peer_groups
        WHERE peer_group=?
        """,
        [group_name],
    )


@st.cache_data(ttl=600)
def get_peer_groups():
    return run_query(
        """
        SELECT DISTINCT peer_group
        FROM peer_groups
        ORDER BY peer_group
        """
    )


@st.cache_data(ttl=600)
def get_valuation(company_id):
    return run_query(
        """
        SELECT *
        FROM market_cap
        WHERE company_id=?
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_documents(company_id):
    return run_query(
        """
        SELECT *
        FROM documents
        WHERE company_id=?
        ORDER BY year DESC
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_pros_cons(company_id):
    return run_query(
        """
        SELECT *
        FROM prosandcons
        WHERE company_id=?
        """,
        [company_id],
    )
@st.cache_data(ttl=600)
def get_latest_ratios(year=None):

    query = "SELECT * FROM financial_ratios"

    if year is not None:
        query += " WHERE year LIKE ?"
        return run_query(query, [f"%{year}"])

    return run_query(query)

# ==========================================================
# Peer Comparison Functions
# ==========================================================

@st.cache_data(ttl=600)
def get_peer_group_names():
    return run_query(
        """
        SELECT DISTINCT peer_group_name
        FROM peer_groups
        WHERE peer_group_name IS NOT NULL
        ORDER BY peer_group_name
        """
    )


@st.cache_data(ttl=600)
def get_peer_group_companies(group_name):
    return run_query(
        """
        SELECT
            pg.company_id,
            pg.is_benchmark,
            c.company_name
        FROM peer_groups pg
        JOIN companies c
            ON pg.company_id = c.id
        WHERE pg.peer_group_name = ?
        ORDER BY pg.is_benchmark DESC,
                 c.company_name
        """,
        [group_name],
    )


@st.cache_data(ttl=600)
def get_latest_company_ratios(company_ids):
    placeholders = ",".join(["?"] * len(company_ids))

    query = f"""
    SELECT *
    FROM financial_ratios fr
    WHERE fr.company_id IN ({placeholders})
      AND fr.year = (
            SELECT MAX(f2.year)
            FROM financial_ratios f2
            WHERE f2.company_id = fr.company_id
      )
    """

    return run_query(query, company_ids)


@st.cache_data(ttl=600)
def get_company_name(company_id):
    return run_query(
        """
        SELECT company_name
        FROM companies
        WHERE id = ?
        """,
        [company_id],
    )