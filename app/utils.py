import pandas as pd

from app.schema import IrisData


def load_iris_csv(csv_path: str) -> list[IrisData]:
    df = pd.read_csv(csv_path)

    df.rename(
        columns={"species": "label"},
        inplace=True,
    )

    records = [IrisData(**row) for row in df.to_dict(orient="records")]
    return records


def clean_iris_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic cleaning on Iris dataset.

    Args:
        df (pd.DataFrame): Raw DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    # Drop rows with missing values
    df = df.dropna()

    # Filter for valid species only (just in case)
    valid_labels = {"setosa", "versicolor", "virginica"}
    df = df[df["label"].isin(valid_labels)]

    # Optional: Enforce data types
    df = df.astype(
        {
            "sepal_length": float,
            "sepal_width": float,
            "petal_length": float,
            "petal_width": float,
            "label": str,
        }
    )

    return df
