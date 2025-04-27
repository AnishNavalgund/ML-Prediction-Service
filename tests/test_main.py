import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    from app import mongodb

    mongodb.sample_collection.delete_many({})
    yield
    mongodb.sample_collection.delete_many({})


def test_post_data_iris():
    sample_data = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
        "label": "setosa",
    }
    response = client.post("/data/iris", json=sample_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Iris Sample added successfully!!"}


def test_get_data_iris():
    sample_data = {
        "sepal_length": 6.4,
        "sepal_width": 2.9,
        "petal_length": 4.3,
        "petal_width": 1.3,
        "label": "versicolor",
    }
    client.post("/data/iris", json=sample_data)

    response = client.get("/data/iris")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(sample["label"] == "versicolor" for sample in data)
