import pandas as pd
import pytest
from fastapi.testclient import TestClient

from app import mongodb
from app.main import app
from app.schema import IrisData

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    from app import mongodb

    mongodb.sample_collection.delete_many({})
    yield
    mongodb.sample_collection.delete_many({})


# Create a dummy DataFrame for mocking
dummy_iris_df = pd.DataFrame(
    [
        {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
            "label": "setosa",
        },
        {
            "sepal_length": 6.2,
            "sepal_width": 2.9,
            "petal_length": 4.3,
            "petal_width": 1.3,
            "label": "versicolor",
        },
    ]
)


def test_post_data_iris(mocker):
    """
    Test uploading Iris data into MongoDB using mocked CSV loading.
    """
    mocker.patch("app.main.load_iris_csv", return_value=dummy_iris_df)

    response = client.post("/data/iris")
    assert response.status_code == 200
    assert "Successfully uploaded" in response.json()["message"]


def test_get_data_iris(mocker):
    """
    Test retrieving uploaded Iris data.
    """
    mocker.patch("app.main.load_iris_csv", return_value=dummy_iris_df)

    client.post("/data/iris")
    response = client.get("/data/iris")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 2
    labels = [d["label"] for d in data]
    assert "setosa" in labels
    assert "versicolor" in labels


def test_train_iris_model():
    """
    Test training the ML model after inserting a sample directly.
    """
    sample_setosa = IrisData(
        sepal_length=5.1,
        sepal_width=3.5,
        petal_length=1.4,
        petal_width=0.2,
        label="setosa",
    )
    sample_versicolor = IrisData(
        sepal_length=6.4,
        sepal_width=3.2,
        petal_length=4.5,
        petal_width=1.5,
        label="versicolor",
    )
    mongodb.insert_data([sample_setosa, sample_versicolor])

    response_train = client.post("/train/iris")
    assert response_train.status_code == 200
    assert "successfully" in response_train.json()["message"].lower()


def test_predict_iris():
    """
    Test prediction on sample Iris input after mock training.
    """
    test_train_iris_model()

    sample_request = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    response = client.post("/predict/iris", json=sample_request)
    assert response.status_code == 200

    prediction = response.json()
    assert prediction["label"] in ["setosa", "versicolor", "virginica"]
    assert 0.0 <= prediction["confidence"] <= 1.0
