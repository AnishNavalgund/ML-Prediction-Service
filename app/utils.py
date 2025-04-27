import pandas as pd

from app.schema import IrisData


def load_iris_csv(csv_path: str) -> pd.DataFrame:
    """
    Load the Iris CSV and rename columns if necessary.
    """
    df = pd.read_csv(csv_path)

    if "species" in df.columns:
        df = df.rename(columns={"species": "label"})

    return df
