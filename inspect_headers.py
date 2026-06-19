# inspect_headers.py

import pandas as pd

files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx"
]

for file in files:
    print("\n" + "=" * 80)
    print(file)

    df = pd.read_excel(
        f"data/raw/{file}",
        header=None
    )

    print(df.head(10))