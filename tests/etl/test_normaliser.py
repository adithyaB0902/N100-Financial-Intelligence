import pytest

from src.etl.normaliser import (
    normalize_ticker,
    normalize_year
)
def test_ticker_upper():
    assert normalize_ticker("tcs") == "TCS"

def test_ticker_spaces():
    assert normalize_ticker(" infy ") == "INFY"

def test_ticker_mixed():
    assert normalize_ticker("ReLiAnCe") == "RELIANCE"

def test_ticker_none():
    assert normalize_ticker(None) is None

def test_year_mar():
    assert normalize_year("Mar 2024") == 2024

def test_year_fy():
    assert normalize_year("FY2023") == 2023

def test_year_int():
    assert normalize_year(2022) == 2022

def test_year_string():
    assert normalize_year("2021") == 2021

def test_invalid_year():
    with pytest.raises(ValueError):
        normalize_year("hello")