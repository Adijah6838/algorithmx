from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.problem import Problem, TestCase
from app.models.user import User
from app.schemas.problem import ProblemCreate, ProblemResponse
from app.api.deps import get_current_admin_or_moderator

router = APIRouter()

@router.post("/", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED)
def create_problem(
    problem_in: ProblemCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_moderator)
):
    new_problem = Problem(
        title=problem_in.title,
        description=problem_in.description,
        input_spec=problem_in.input_spec,
        output_spec=problem_in.output_spec,
        constraints=problem_in.constraints,
        difficulty=problem_in.difficulty,
        category=problem_in.category,
        is_published=problem_in.is_published
    )
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)
    
    for tc in problem_in.test_cases:
        new_tc = TestCase(
            problem_id=new_problem.id,
            input_data=tc.input_data,
            expected_output=tc.expected_output,
            is_sample=tc.is_sample
        )
        db.add(new_tc)
    
    db.commit()
    db.refresh(new_problem)
    return new_problem

@router.get("/", response_model=List[ProblemResponse])
def get_problems(db: Session = Depends(get_db)):
    return db.query(Problem).filter(Problem.is_published == True).all()
