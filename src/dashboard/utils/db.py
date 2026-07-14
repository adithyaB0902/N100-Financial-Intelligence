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
def get_ratios(ticker, year=None):
    query = """
        SELECT *
        FROM financial_ratios
        WHERE ticker = ?
    """

    params = [ticker]

    if year is not None:
        query += " AND year=?"
        params.append(year)

    query += " ORDER BY year DESC"

    return run_query(query, params)


@st.cache_data(ttl=600)
def get_pl(ticker):
    return run_query(
        """
        SELECT *
        FROM profitandloss
        WHERE ticker=?
        ORDER BY year DESC
        """,
        [ticker],
    )


@st.cache_data(ttl=600)
def get_bs(ticker):
    return run_query(
        """
        SELECT *
        FROM balancesheet
        WHERE ticker=?
        ORDER BY year DESC
        """,
        [ticker],
    )


@st.cache_data(ttl=600)
def get_cf(ticker):
    return run_query(
        """
        SELECT *
        FROM cashflow
        WHERE ticker=?
        ORDER BY year DESC
        """,
        [ticker],
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
def get_valuation(ticker):
    return run_query(
        """
        SELECT *
        FROM market_cap
        WHERE ticker=?
        """,
        [ticker],
    )


@st.cache_data(ttl=600)
def get_documents(ticker):
    return run_query(
        """
        SELECT *
        FROM documents
        WHERE ticker=?
        ORDER BY year DESC
        """,
        [ticker],
    )


@st.cache_data(ttl=600)
def get_pros_cons(ticker):
    return run_query(
        """
        SELECT *
        FROM prosandcons
        WHERE ticker=?
        """,
        [ticker],
    )