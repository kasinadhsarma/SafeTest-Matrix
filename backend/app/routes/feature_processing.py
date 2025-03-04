from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Optional, List

router = APIRouter()

class FeatureProcessingSession(BaseModel):
    session_id: str
    candidate_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str
    features: Optional[Dict[str, float]] = {}
    violations: Optional[List[str]] = []

feature_processing_sessions: Dict[str, FeatureProcessingSession] = {}

@router.post("/start_feature_processing", response_model=FeatureProcessingSession)
def start_feature_processing(session_id: str, candidate_id: str):
    if session_id in feature_processing_sessions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session already exists")
    feature_processing_session = FeatureProcessingSession(session_id=session_id, candidate_id=candidate_id, start_time=datetime.now(), status="ongoing")
    feature_processing_sessions[session_id] = feature_processing_session
    return feature_processing_session

@router.post("/stop_feature_processing", response_model=FeatureProcessingSession)
def stop_feature_processing(session_id: str):
    if session_id not in feature_processing_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    feature_processing_session = feature_processing_sessions[session_id]
    feature_processing_session.end_time = datetime.now()
    feature_processing_session.status = "completed"
    return feature_processing_session

@router.post("/add_feature", response_model=FeatureProcessingSession)
def add_feature(session_id: str, feature_name: str, feature_value: float):
    if session_id not in feature_processing_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    feature_processing_session = feature_processing_sessions[session_id]
    feature_processing_session.features[feature_name] = feature_value
    return feature_processing_session

@router.post("/add_violation", response_model=FeatureProcessingSession)
def add_violation(session_id: str, violation: str):
    if session_id not in feature_processing_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    feature_processing_session = feature_processing_sessions[session_id]
    feature_processing_session.violations.append(violation)
    return feature_processing_session

@router.get("/monitor_feature_processing/{session_id}", response_model=FeatureProcessingSession)
def monitor_feature_processing(session_id: str):
    if session_id not in feature_processing_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return feature_processing_sessions[session_id]
