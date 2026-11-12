import asyncio
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.db.database import get_db, SessionLocal
from app.models.user import User
from app.models.submission import Submission, SubmissionStatus
from app.services.ws_manager import manager

router = APIRouter()

def get_leaderboard_data(db: Session):
    results = db.query(
        User.username, 
        func.count(func.distinct(Submission.problem_id)).label('solved')
    ).join(Submission, User.id == Submission.user_id).filter(
        Submission.status == SubmissionStatus.ACCEPTED
    ).group_by(User.username).order_by(func.count(func.distinct(Submission.problem_id)).desc()).all()
    
    return [{"username": r[0], "solved": r[1]} for r in results]

@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    return get_leaderboard_data(db)

@router.websocket("/ws")
async def websocket_leaderboard(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            db = SessionLocal()
            try:
                data = get_leaderboard_data(db)
                await websocket.send_json(data)
            finally:
                db.close()
            
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
