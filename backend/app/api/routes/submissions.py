from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.submission import Submission
from app.models.user import User
from app.models.problem import Problem
from app.schemas.submission import SubmissionCreate, SubmissionResponse
from app.api.deps import get_current_user
from app.services.evaluator import evaluate_submission

router = APIRouter()

@router.post("/", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
def submit_code(
    submission_in: SubmissionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify problem exists
    problem = db.query(Problem).filter(Problem.id == submission_in.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    new_submission = Submission(
        user_id=current_user.id,
        problem_id=submission_in.problem_id,
        language=submission_in.language,
        code=submission_in.code
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    # Trigger background evaluation
    background_tasks.add_task(evaluate_submission, new_submission.id, db)

    return new_submission

@router.get("/", response_model=List[SubmissionResponse])
def get_my_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Submission).filter(Submission.user_id == current_user.id).order_by(Submission.created_at.desc()).all()
