from typing import Literal

from pydantic import BaseModel, Field


class IrisData(BaseModel):
    sepal_length: float = Field(..., gt=0, description="sepal lenght in cm")
    sepal_width: float = Field(..., gt=0, description="sepal width in cm")
    petal_length: float = Field(..., gt=0, description="petal lenght in cm")
    petal_width: float = Field(..., gt=0, description="petal width in cm")
    label: Literal["setosa", "versicolor", "virginica"] = Field(
        ..., description="Species of Iris flower"
    )


class IrisPredictionRequest(BaseModel):
    sepal_length: float = Field(..., gt=0, description="sepal lenght in cm")
    sepal_width: float = Field(..., gt=0, description="sepal width in cm")
    petal_length: float = Field(..., gt=0, description="petal lenght in cm")
    petal_width: float = Field(..., gt=0, description="petal width in cm")


class IrisPredictionResponse(BaseModel):
    label: Literal["setosa", "versicolor", "virginica"] = Field(
        ..., description="Predicted species of Iris"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence of prediction"
    )
