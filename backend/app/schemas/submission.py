from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.submission import Language, SubmissionStatus

class SubmissionCreate(BaseModel):
    problem_id: int
    language: Language
    code: str

class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    problem_id: int
    language: Language
    status: SubmissionStatus
    execution_time: Optional[float] = None
    memory_used: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True
