from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

router = APIRouter()

class ExamSession(BaseModel):
    session_id: str
    candidate_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str

exam_sessions: Dict[str, ExamSession] = {}

@router.post("/start_exam", response_model=ExamSession)
def start_exam(session_id: str, candidate_id: str):
    if session_id in exam_sessions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session already exists")
    exam_session = ExamSession(session_id=session_id, candidate_id=candidate_id, start_time=datetime.now(), status="ongoing")
    exam_sessions[session_id] = exam_session
    return exam_session

@router.post("/stop_exam", response_model=ExamSession)
def stop_exam(session_id: str):
    if session_id not in exam_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    exam_session = exam_sessions[session_id]
    exam_session.end_time = datetime.now()
    exam_session.status = "completed"
    return exam_session

@router.get("/monitor_exam/{session_id}", response_model=ExamSession)
def monitor_exam(session_id: str):
    if session_id not in exam_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return exam_sessions[session_id]
