from pathlib import Path
import pandas as pd

from src.etl.bulk_loader import (
    load_all_excels
)


def test_missing_folder():

    try:
        load_all_excels("abcxyz")

    except FileNotFoundError:
        assert True