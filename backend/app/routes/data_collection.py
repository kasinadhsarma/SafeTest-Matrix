from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

router = APIRouter()

class DataCollectionSession(BaseModel):
    session_id: str
    candidate_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str
    mouse_movements: Optional[list] = []
    keystrokes: Optional[list] = []
    activity_shifts: Optional[list] = []

data_collection_sessions: Dict[str, DataCollectionSession] = {}

@router.post("/start_data_collection", response_model=DataCollectionSession)
def start_data_collection(session_id: str, candidate_id: str):
    if session_id in data_collection_sessions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session already exists")
    data_collection_session = DataCollectionSession(session_id=session_id, candidate_id=candidate_id, start_time=datetime.now(), status="ongoing")
    data_collection_sessions[session_id] = data_collection_session
    return data_collection_session

@router.post("/stop_data_collection", response_model=DataCollectionSession)
def stop_data_collection(session_id: str):
    if session_id not in data_collection_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    data_collection_session = data_collection_sessions[session_id]
    data_collection_session.end_time = datetime.now()
    data_collection_session.status = "completed"
    return data_collection_session

@router.post("/track_mouse_movement", response_model=DataCollectionSession)
def track_mouse_movement(session_id: str, movement: dict):
    if session_id not in data_collection_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    data_collection_session = data_collection_sessions[session_id]
    data_collection_session.mouse_movements.append(movement)
    return data_collection_session

@router.post("/track_keystroke", response_model=DataCollectionSession)
def track_keystroke(session_id: str, keystroke: dict):
    if session_id not in data_collection_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    data_collection_session = data_collection_sessions[session_id]
    data_collection_session.keystrokes.append(keystroke)
    return data_collection_session

@router.post("/track_activity_shift", response_model=DataCollectionSession)
def track_activity_shift(session_id: str, activity_shift: dict):
    if session_id not in data_collection_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    data_collection_session = data_collection_sessions[session_id]
    data_collection_session.activity_shifts.append(activity_shift)
    return data_collection_session

@router.get("/monitor_data_collection/{session_id}", response_model=DataCollectionSession)
def monitor_data_collection(session_id: str):
    if session_id not in data_collection_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return data_collection_sessions[session_id]
