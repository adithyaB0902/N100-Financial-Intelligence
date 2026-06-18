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