import pandas as pd

from src.kpi.populate_financial_ratios import calculate_kpis


def test_calculate_kpis_includes_roce_column():
    df = pd.DataFrame([
        {
            "company_id": "CMP1",
            "year": 2023,
            "net_profit": 100,
            "sales": 1000,
            "operating_profit": 150,
            "equity_capital": 200,
            "reserves": 300,
            "borrowings": 500,
            "total_assets": 1000,
            "interest": 10,
            "other_income": 20,
        }
    ])

    result = calculate_kpis(df)

    assert "return_on_capital_employed" in result.columns
    assert result.loc[0, "return_on_capital_employed"] == 15.0
