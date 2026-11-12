from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for the AlgorithmX competitive programming platform"
)

@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} v{settings.VERSION}",
        "status": "online"
    }