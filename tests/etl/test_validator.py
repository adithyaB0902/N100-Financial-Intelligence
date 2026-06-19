import pandas as pd

from src.etl.validator import DataValidator
def test_duplicate_company_id():

    df = pd.DataFrame({
        "company_id": [1, 1]
    })

    validator = DataValidator()

    validator.validate_company_id_unique(df)

    assert len(validator.failures) == 1
def test_duplicate_company_year():

    df = pd.DataFrame({
        "company_id": [1, 1],
        "year": [2024, 2024]
    })

    validator = DataValidator()

    validator.validate_company_year_unique(df)

    assert len(validator.failures) == 1
def test_invalid_fk():

    companies = pd.DataFrame({
        "company_id": [1]
    })

    pnl = pd.DataFrame({
        "company_id": [999]
    })

    validator = DataValidator()

    validator.validate_fk_integrity(
        pnl,
        companies
    )

    assert len(
        validator.failures
    ) == 1
def test_negative_cash():
    df = pd.DataFrame({
        "company_id": [1],
        "cash": [-10]
    })

    validator = DataValidator()
    validator.validate_net_cash(df)

    assert len(validator.failures) == 1
def test_invalid_tax_rate():
    df = pd.DataFrame({
        "company_id": [1],
        "tax_rate": [120]
    })

    validator = DataValidator()
    validator.validate_tax_rate(df)

    assert len(validator.failures) == 1
def test_dividend_exceeds_profit():
    df = pd.DataFrame({
        "company_id": [1],
        "dividend": [100],
        "net_profit": [50]
    })

    validator = DataValidator()
    validator.validate_dividend(df)

    assert len(validator.failures) == 1
def test_invalid_url():
    df = pd.DataFrame({
        "company_id": [1],
        "url": ["invalid-url"]
    })

    validator = DataValidator()
    validator.validate_urls(df)

    assert len(validator.failures) == 1
def test_eps_sign_mismatch():
    df = pd.DataFrame({
        "company_id": [1],
        "net_profit": [-100],
        "eps": [5]
    })

    validator = DataValidator()
    validator.validate_eps_sign(df)

    assert len(validator.failures) == 1
def test_negative_interest_coverage():
    df = pd.DataFrame({
        "company_id": [1],
        "interest_coverage": [-2]
    })

    validator = DataValidator()
    validator.validate_interest_coverage(df)

    assert len(validator.failures) == 1
def test_year_out_of_range():
    df = pd.DataFrame({
        "company_id": [1],
        "year": [1990]
    })

    validator = DataValidator()
    validator.validate_year_range(df)

    assert len(validator.failures) == 1
def test_missing_company_name():
    df = pd.DataFrame({
        "company_id": [1],
        "company_name": [None]
    })

    validator = DataValidator()
    validator.validate_null_company_name(df)

    assert len(validator.failures) == 1
def test_duplicate_ticker():
    df = pd.DataFrame({
        "company_id": [1, 2],
        "ticker": ["TCS", "TCS"]
    })

    validator = DataValidator()
    validator.validate_duplicate_ticker(df)

    assert len(validator.failures) == 1
def test_profit_exceeds_sales():
    df = pd.DataFrame({
        "company_id": [1],
        "sales": [100],
        "net_profit": [150]
    })

    validator = DataValidator()
    validator.validate_profit_consistency(df)

    assert len(validator.failures) == 1
