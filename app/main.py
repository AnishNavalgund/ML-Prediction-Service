from typing import List

from fastapi import Body, FastAPI, HTTPException

from app import model, mongodb
from app.configuration import settings
from app.schema import IrisData, IrisPredictionRequest, IrisPredictionResponse
from app.utils import load_iris_csv

app = FastAPI(
    title="ML Classification Service API",
    description="API for ingesting data, training a model, and serving predictions",
    version="1.0.0",
)


@app.post("/data/iris", response_model=dict)
async def upload_iris_data() -> dict:
    """
    Upload the entire Iris dataset into MongoDB.
    Returns:
        dict: Success message.
    """
    try:
        # iris_samples = load_iris_csv(settings.iris_csv_path)
        df = load_iris_csv(settings.iris_csv_path)
        iris_data = [IrisData(**row) for row in df.to_dict(orient="records")]
        mongodb.insert_data(iris_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load CSV: {str(e)}")

    return {"message": f"Successfully uploaded {len(iris_data)} Iris data."}


@app.get("/data/iris", response_model=List[IrisData])
async def get_samples(label: str = None) -> List[IrisData]:
    """
    Get Iris samples from MongoDB.
    Args:
        label: Optional label to filter samples.
    Returns:
        List[IrisData]: List of Iris samples.
    """
    samples = mongodb.get_samples(label)
    if not samples:
        raise HTTPException(status_code=404, detail="No samples found")
    return samples


@app.post("/train/iris", response_model=dict)
async def train_model() -> dict:
    """
    Train the model using samples from MongoDB.
    Returns:
        dict: Success message.
    """
    samples = mongodb.get_samples()
    if not samples:
        raise HTTPException(status_code=400, detail="No data to train on")
    model.train(samples)
    return {"message": "Iris Model trained successfully!!"}


@app.post("/predict/iris", response_model=IrisPredictionResponse)
async def predict_iris(sample: IrisPredictionRequest) -> IrisPredictionResponse:
    """
    Predict the label of an Iris sample
    Args:
        sample: Input Iris sample
    Returns:
        IrisPredictionResponse: Prediction result
    """
    try:
        prediction = model.predict(sample)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=f"Prediction failed: {error}",
        ) from error

    return prediction
