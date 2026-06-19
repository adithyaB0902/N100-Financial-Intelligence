import pandas as pd
from pathlib import Path

folder = Path("data/raw")

for file in folder.glob("*.xlsx"):
    print("\n" + "=" * 60)
    print(file.name)

    df = pd.read_excel(file)

    print("Rows:", len(df))
    print("Columns:")
    print(df.columns.tolist())