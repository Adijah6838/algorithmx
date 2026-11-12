from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models.user import User
from app.models.problem import Problem
from app.models.submission import Submission
from app.models.contest import Contest
from app.schemas.analytics import DashboardStats
from app.api.deps import get_current_admin_or_moderator

router = APIRouter()

@router.get("/", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_or_moderator) # Only admins/mods can see platform analytics
):
    # 1. Basic counts
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_problems = db.query(func.count(Problem.id)).scalar() or 0
    total_submissions = db.query(func.count(Submission.id)).scalar() or 0
    total_contests = db.query(func.count(Contest.id)).scalar() or 0

    # 2. Group submissions by status
    status_query = db.query(
        Submission.status, func.count(Submission.id)
    ).group_by(Submission.status).all()
    
    # Convert to a dictionary like {"Accepted": 5, "Wrong Answer": 2}
    submission_statuses = {status.value: count for status, count in status_query}

    # 3. Fill in missing statuses with 0 so the frontend charts don't break
    all_statuses = ["Accepted", "Wrong Answer", "Compilation Error", "Runtime Error", "Time Limit Exceeded", "Memory Limit Exceeded", "Pending"]
    for status_name in all_statuses:
        if status_name not in submission_statuses:
            submission_statuses[status_name] = 0

    return {
        "total_users": total_users,
        "total_problems": total_problems,
        "total_submissions": total_submissions,
        "submission_statuses": submission_statuses,
        "total_contests": total_contests
    }
