from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.problem import ProblemResponse
from app.schemas.user import UserResponse

class ContestBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_active: bool = True

class ContestCreate(ContestBase):
    problem_ids: List[int] = []

class ContestResponse(ContestBase):
    id: int
    problems: List[ProblemResponse] = []
    participants: List[UserResponse] = []

    class Config:
        from_attributes = True
