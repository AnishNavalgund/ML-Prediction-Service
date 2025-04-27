from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings loaded from env variables
    mongo_uri: str
    mongo_db_name: str = "ml_db"
    model_storage_path: str = "model.pkl"

    class Config:
        env_file = ".env"


settings = Settings()
