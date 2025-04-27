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
