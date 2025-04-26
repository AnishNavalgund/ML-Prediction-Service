from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongo:27017"))
db = client.ml_db

def insert_sample(sample):
    db.samples.insert_one(sample)

def get_samples(label=None):
    query = {"label": label} if label else {}
    return list(db.samples.find(query, {"_id": 0}))