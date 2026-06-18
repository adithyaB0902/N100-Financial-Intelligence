from pathlib import Path
import pandas as pd


def load_all_excels(folder_path):
    folder = Path(folder_path)

    dataframes = {}

    for file in folder.glob("*.xlsx"):
        dataframes[file.stem] = pd.read_excel(file)

    return dataframes