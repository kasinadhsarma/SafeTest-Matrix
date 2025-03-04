from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

router = APIRouter()

class InterventionSession(BaseModel):
    session_id: str
    candidate_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    warning: Optional[str] = None
    restriction: Optional[str] = None
    admin_alert: Optional[str] = None

intervention_sessions: Dict[str, InterventionSession] = {}

@router.post("/start_intervention", response_model=InterventionSession)
def start_intervention(session_id: str, candidate_id: str):
    if session_id in intervention_sessions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session already exists")
    intervention_session = InterventionSession(session_id=session_id, candidate_id=candidate_id, start_time=datetime.now(), status="ongoing")
    intervention_sessions[session_id] = intervention_session
    return intervention_session

@router.post("/stop_intervention", response_model=InterventionSession)
def stop_intervention(session_id: str):
    if session_id not in intervention_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    intervention_session = intervention_sessions[session_id]
    intervention_session.end_time = datetime.now()
    intervention_session.status = "completed"
    return intervention_session

@router.post("/warn_candidate", response_model=InterventionSession)
def warn_candidate(session_id: str, risk_score: float):
    if session_id not in intervention_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    intervention_session = intervention_sessions[session_id]
    intervention_session.risk_score = risk_score
    
    # Generate warning based on risk score
    if risk_score < 0.3:
        intervention_session.risk_level = "Low"
        intervention_session.warning = "No significant risk detected."
    elif risk_score < 0.7:
        intervention_session.risk_level = "Medium"
        intervention_session.warning = "Medium risk detected. Please be cautious."
    else:
        intervention_session.risk_level = "High"
        intervention_session.warning = "High risk detected. Immediate action required."
    
    return intervention_session

@router.post("/restrict_features", response_model=InterventionSession)
def restrict_features(session_id: str, risk_score: float):
    if session_id not in intervention_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    intervention_session = intervention_sessions[session_id]
    intervention_session.risk_score = risk_score
    
    # Restrict features based on risk score
    if risk_score < 0.3:
        intervention_session.risk_level = "Low"
        intervention_session.restriction = "No restrictions applied."
    elif risk_score < 0.7:
        intervention_session.risk_level = "Medium"
        intervention_session.restriction = "Some features restricted. Please be cautious."
    else:
        intervention_session.risk_level = "High"
        intervention_session.restriction = "High risk detected. Features restricted. Immediate action required."
    
    return intervention_session

@router.post("/alert_admin", response_model=InterventionSession)
def alert_admin(session_id: str, risk_score: float):
    if session_id not in intervention_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    intervention_session = intervention_sessions[session_id]
    intervention_session.risk_score = risk_score
    
    # Alert admin based on risk score
    if risk_score < 0.3:
        intervention_session.risk_level = "Low"
        intervention_session.admin_alert = "No significant risk detected."
    elif risk_score < 0.7:
        intervention_session.risk_level = "Medium"
        intervention_session.admin_alert = "Medium risk detected. Please review."
    else:
        intervention_session.risk_level = "High"
        intervention_session.admin_alert = "High risk detected. Immediate action required."
    
    return intervention_session

@router.get("/monitor_intervention/{session_id}", response_model=InterventionSession)
def monitor_intervention(session_id: str):
    if session_id not in intervention_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return intervention_sessions[session_id]
