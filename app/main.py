from fastapi import FastAPI, HTTPException, Body
from app import model, mongodb

app = FastAPI()


@app.post("/data")
def add_sample(sample: dict = Body(...)):
    mongodb.insert_sample(sample)
    return {"message": "Sample added"}


@app.get("/data")
def get_samples(label: str = None):
    return mongodb.get_samples(label)


@app.post("/train")
def train_model():
    samples = mongodb.get_samples()
    if not samples:
        raise HTTPException(status_code=400, detail="No data to train on")
    model.train(samples)
    return {"message": "Model trained"}


@app.post("/predict")
def predict(text: str = Body(...)):
    prediction = model.predict(text)
    return {"label": prediction}
