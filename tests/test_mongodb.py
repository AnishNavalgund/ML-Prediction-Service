import pytest

from app import mongodb
from app.schema import IrisData

# Dummy IrisData for testing
TEST_SAMPLE = IrisData(
    sepal_length=5.1,
    sepal_width=3.5,
    petal_length=1.4,
    petal_width=0.2,
    label="setosa",
)


@pytest.fixture(autouse=True)
def clear_samples():
    """
    Fixture to clear the sample collection before and after each test.
    """
    mongodb.sample_collection.delete_many({})
    yield
    mongodb.sample_collection.delete_many({})


def test_insert_data():
    """
    Test inserting IrisData sample into MongoDB.
    """
    mongodb.insert_data([TEST_SAMPLE])

    samples = mongodb.get_samples()
    assert len(samples) == 1
    assert isinstance(samples[0], IrisData)
    assert samples[0].label == "setosa"


def test_get_samples():
    """
    Test retrieving samples from MongoDB.
    """
    mongodb.insert_data([TEST_SAMPLE])

    all_samples = mongodb.get_samples()
    assert len(all_samples) == 1
    assert all_samples[0].label == "setosa"
