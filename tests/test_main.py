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
    response = client.post("/data/iris")

    assert response.status_code == 200
    assert "Successfully uploaded" in response.json()["message"]


def test_get_data_iris():
    response = client.post("/data/iris")
    assert response.status_code == 200

    # Fetch all samples
    response = client.get("/data/iris")
    assert response.status_code == 200
    data = response.json()

    # Basic checks
    assert isinstance(data, list)
    assert len(data) > 0  # CSV loaded, should have 150 samples
    assert all("sepal_length" in sample for sample in data)
    assert all("label" in sample for sample in data)
