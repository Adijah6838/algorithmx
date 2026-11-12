from pydantic import BaseModel
from typing import Optional, List
from app.models.problem import Difficulty, Category

class TestCaseBase(BaseModel):
    input_data: str
    expected_output: str
    is_sample: bool = False

class TestCaseCreate(TestCaseBase):
    pass

class TestCaseResponse(TestCaseBase):
    id: int
    class Config:
        from_attributes = True

class ProblemBase(BaseModel):
    title: str
    description: str
    input_spec: str
    output_spec: str
    constraints: Optional[str] = None
    difficulty: Difficulty
    category: Category
    is_published: bool = False

class ProblemCreate(ProblemBase):
    test_cases: List[TestCaseCreate] = []

class ProblemResponse(ProblemBase):
    id: int
    test_cases: List[TestCaseResponse] = []
    
    class Config:
        from_attributes = True
