import logging
import pickle

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from app.configuration import settings

logger = logging.getLogger(__name__)

MODEL_PATH = settings.model_storage_path

pipeline = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("classifier", SVC(kernel="linear", probability=True)),
    ]
)


def train(data: list[dict]) -> None:
    if not data:
        raise ValueError("No data provided for training.")

    df = pd.DataFrame(data)

    # labels = [s["label"] for s in samples]
    # X = vectorizer.fit_transform(texts)

    X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    y = df["label"]

    # model.fit(X, labels)
    pipeline.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        # pickle.dump((vectorizer, clf), f)
        pickle.dump(pipeline, f)

    logger.info(f"Model trained and saved at {MODEL_PATH}")

    # labels = [s["label"] for s in samples]
    # X = vectorizer.fit_transform(texts)


def predict(sample) -> str:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    # X = vec.transform([text])
    input_df = pd.DataFrame([sample])
    prediction = model.predict(input_df)[0]
    return prediction
