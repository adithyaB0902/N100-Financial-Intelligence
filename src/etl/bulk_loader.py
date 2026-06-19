from pathlib import Path
import pandas as pd


def load_all_excels(folder_path):

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(
            f"{folder} not found"
        )

    datasets = {}

    for file in folder.glob("*.xlsx"):

        datasets[file.stem] = pd.read_excel(
            file
        )

    return datasets