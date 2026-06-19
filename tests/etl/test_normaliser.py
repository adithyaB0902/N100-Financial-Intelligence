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

def test_ticker_already_upper():
    assert normalize_ticker("TCS") == "TCS"

def test_ticker_lower():
    assert normalize_ticker("hdfc") == "HDFC"

def test_ticker_numeric():
    assert normalize_ticker(123) == "123"

def test_ticker_special():
    assert normalize_ticker("abc-ltd") == "ABC-LTD"

def test_ticker_tabs():
    assert normalize_ticker("\tINFY\t") == "INFY"

def test_ticker_newline():
    assert normalize_ticker("\nTCS\n") == "TCS"

def test_ticker_multiple_spaces():
    assert normalize_ticker("R E L") == "REL"

def test_ticker_empty():
    assert normalize_ticker("") == ""

def test_ticker_single_char():
    assert normalize_ticker("a") == "A"

def test_ticker_long():
    assert normalize_ticker("adaniports") == "ADANIPORTS"

def test_ticker_whitespace_only():
    assert normalize_ticker("   ") == ""
def test_year_mar():
    assert normalize_year("Mar 2024") == 2024

def test_year_fy():
    assert normalize_year("FY2023") == 2023

def test_year_int():
    assert normalize_year(2022) == 2022

def test_year_string():
    assert normalize_year("2021") == 2021

def test_year_with_space():
    assert normalize_year(" 2020 ") == 2020

def test_year_fy_space():
    assert normalize_year("FY 2019") == 2019

def test_year_mar_space():
    assert normalize_year("Mar 2018") == 2018

def test_year_2017():
    assert normalize_year("2017") == 2017

def test_year_2016():
    assert normalize_year("FY2016") == 2016

def test_year_2015():
    assert normalize_year("Mar 2015") == 2015

def test_year_2014():
    assert normalize_year("2014") == 2014

def test_year_2013():
    assert normalize_year("FY2013") == 2013

def test_year_2012():
    assert normalize_year("Mar 2012") == 2012

def test_year_2011():
    assert normalize_year("2011") == 2011

def test_year_2010():
    assert normalize_year("FY2010") == 2010

def test_year_2009():
    assert normalize_year("Mar 2009") == 2009

def test_year_2008():
    assert normalize_year("2008") == 2008

def test_year_invalid_text():
    with pytest.raises(ValueError):
        normalize_year("hello")

def test_year_invalid_symbol():
    with pytest.raises(ValueError):
        normalize_year("@@@")

def test_year_invalid_blank():
    with pytest.raises(ValueError):
        normalize_year("")
