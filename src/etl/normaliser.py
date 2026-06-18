import re
def normalize_ticker(ticker):
    if ticker is None:
        return None

    ticker = str(ticker).strip().upper()

    ticker = re.sub(r"\s+", "", ticker)

    return ticker


def normalize_year(year):
    if year is None:
        return None

    if isinstance(year, int):
        return year

    year = str(year).strip()

    match = re.search(r"(20\d{2})", year)

    if match:
        return int(match.group(1))

    raise ValueError(
        f"Invalid year format: {year}"
    )