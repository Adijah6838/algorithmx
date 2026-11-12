from pydantic import BaseModel
from typing import Dict

class DashboardStats(BaseModel):
    total_users: int
    total_problems: int
    total_submissions: int
    submission_statuses: Dict[str, int]
    total_contests: int
