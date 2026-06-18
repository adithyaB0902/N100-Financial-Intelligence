import pandas as pd
from pathlib import Path


def load_excel(file_path):
    """
    Load Excel file into DataFrame.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found")

    return pd.read_excel(file_path)