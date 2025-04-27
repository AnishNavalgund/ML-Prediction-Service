from pathlib import Path
from typing import Dict, List

import pandas as pd


def load_csv(csv_path: str) -> pd.DataFrame:
    path_obj = Path(csv_path)
    if not path_obj.exists():
        raise FileNotFoundError(f"CSV file '{csv_path}' does not exist.")

    return pd.read_csv(path_obj)
