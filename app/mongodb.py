import os
from typing import List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from app.configuration import Settings
from app.schema import IrisData

settings = Settings()

# Initialize MongoDB client and database
client: MongoClient = MongoClient(settings.mongo_uri)
db = client[settings.mongo_db_name]
sample_collection: Collection = db["samples"]


# Injest data into MongoDB
def insert_sample(sample):
    sample_collection.insert_one(sample.dict())


def get_samples(label=None):
    query = {"label": label} if label else {}
    documents = sample_collection.find(query, {"_id": 0})
    return [IrisData(**doc) for doc in documents]
