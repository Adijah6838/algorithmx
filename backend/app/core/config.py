from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AlgorithmX API"
    VERSION: str = "0.1.0"
    
    # Database Configuration (Explicitly using psycopg2 driver)
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/algorithmx"
    
    class Config:
        env_file = ".env"

settings = Settings()
