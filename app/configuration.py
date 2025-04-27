from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # Application settings loaded from env variables
    mongo_uri: str
    mongo_db_name: str = "ml_db"
    model_storage_path: str = str(BASE_DIR / "models/model.pkl")
    iris_csv_path: str = str(BASE_DIR / "data/iris.csv")
    # iris_csv_path: str = "data/iris.csv"

    class Config:
        env_file = ".env"


settings = Settings()
