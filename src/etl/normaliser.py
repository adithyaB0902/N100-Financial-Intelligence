# src/etl/normaliser.py

import re

def normalize_ticker(ticker):
    """
    Convert ticker to uppercase and remove spaces.
    """
    if ticker is None:
        return None

    return str(ticker).strip().upper()


def normalize_year(year):
    """
    Convert year formats into integer year.
    Examples:
        Mar 2024 -> 2024
        FY2023 -> 2023
        2022 -> 2022
    """
    if year is None:
        return None

    year = str(year).strip()

    match = re.search(r"(20\d{2})", year)

    if match:
        return int(match.group(1))

    raise ValueError(f"Invalid year format: {year}")