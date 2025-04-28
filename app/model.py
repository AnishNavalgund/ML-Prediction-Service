import logging
import pickle

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from app.configuration import settings

logger = logging.getLogger(__name__)

MODEL_PATH = settings.model_storage_path

# Load the model using Pipeline
pipeline = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("classifier", SVC(kernel="linear", probability=True)),
    ]
)


def train(data: list[dict]) -> None:
    """
    Train the model using the provided data.
    Args:
        data (list[dict]): List of dictionaries containing the training data.
    """
    # Load the data into a DataFrame
    if not data:
        raise ValueError("No data provided for training.")

    df = pd.DataFrame(data)

    X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    y = df["label"]

    pipeline.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)

    logger.info(f"Model trained and saved at {MODEL_PATH}")


def predict(sample: dict) -> str:
    """
    Predict the label of a sample using the trained model.
    Args:
        sample (dict): Dictionary containing the sample data.
    Returns:
        str: Predicted label and confidence score.
    """
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    # X = vec.transform([text])
    input_df = pd.DataFrame([sample])
    prediction = model.predict(input_df)[0]
    conf = model.predict_proba(input_df)[0].max()
    return {
        "label": prediction,
        "confidence": float(conf),
    }
