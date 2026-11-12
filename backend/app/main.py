from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth, problems, submissions

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for the AlgorithmX competitive programming platform"
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(problems.router, prefix="/api/problems", tags=["Problems"])
app.include_router(submissions.router, prefix="/api/submissions", tags=["Submissions"])

@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} v{settings.VERSION}",
        "status": "online"
    }
