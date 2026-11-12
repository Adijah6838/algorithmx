from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.contest import Contest
from app.models.problem import Problem
from app.models.user import User
from app.schemas.contest import ContestCreate, ContestResponse
from app.api.deps import get_current_user, get_current_admin_or_moderator

router = APIRouter()

@router.post("/", response_model=ContestResponse, status_code=status.HTTP_201_CREATED)
def create_contest(
    contest_in: ContestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_moderator)
):
    new_contest = Contest(
        title=contest_in.title,
        description=contest_in.description,
        start_time=contest_in.start_time,
        end_time=contest_in.end_time,
        is_active=contest_in.is_active
    )
    
    if contest_in.problem_ids:
        problems = db.query(Problem).filter(Problem.id.in_(contest_in.problem_ids)).all()
        new_contest.problems = problems

    db.add(new_contest)
    db.commit()
    db.refresh(new_contest)
    return new_contest

@router.get("/", response_model=List[ContestResponse])
def get_contests(db: Session = Depends(get_db)):
    return db.query(Contest).filter(Contest.is_active == True).all()

@router.post("/{contest_id}/register", status_code=status.HTTP_200_OK)
def register_for_contest(
    contest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contest = db.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(status_code=404, detail="Contest not found")
        
    if current_user in contest.participants:
        raise HTTPException(status_code=400, detail="Already registered for this contest")
        
    contest.participants.append(current_user)
    db.commit()
    return {"message": "Successfully registered for contest"}
