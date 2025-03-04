from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
import numpy as np

router = APIRouter()

class LLMIntegrationSession(BaseModel):
    session_id: str
    candidate_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    warning: Optional[str] = None
    explanation: Optional[str] = None

llm_integration_sessions: Dict[str, LLMIntegrationSession] = {}

@router.post("/start_llm_integration", response_model=LLMIntegrationSession)
def start_llm_integration(session_id: str, candidate_id: str):
    if session_id in llm_integration_sessions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session already exists")
    llm_integration_session = LLMIntegrationSession(session_id=session_id, candidate_id=candidate_id, start_time=datetime.now(), status="ongoing")
    llm_integration_sessions[session_id] = llm_integration_session
    return llm_integration_session

@router.post("/stop_llm_integration", response_model=LLMIntegrationSession)
def stop_llm_integration(session_id: str):
    if session_id not in llm_integration_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    llm_integration_session = llm_integration_sessions[session_id]
    llm_integration_session.end_time = datetime.now()
    llm_integration_session.status = "completed"
    return llm_integration_session

@router.post("/generate_warning", response_model=LLMIntegrationSession)
def generate_warning(session_id: str, risk_score: float):
    if session_id not in llm_integration_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    llm_integration_session = llm_integration_sessions[session_id]
    llm_integration_session.risk_score = risk_score
    
    # Generate warning based on risk score
    if risk_score < 0.3:
        llm_integration_session.risk_level = "Low"
        llm_integration_session.warning = "No significant risk detected."
    elif risk_score < 0.7:
        llm_integration_session.risk_level = "Medium"
        llm_integration_session.warning = "Medium risk detected. Please be cautious."
    else:
        llm_integration_session.risk_level = "High"
        llm_integration_session.warning = "High risk detected. Immediate action required."
    
    return llm_integration_session

@router.post("/generate_explanation", response_model=LLMIntegrationSession)
def generate_explanation(session_id: str, risk_score: float):
    if session_id not in llm_integration_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    llm_integration_session = llm_integration_sessions[session_id]
    llm_integration_session.risk_score = risk_score
    
    # Generate explanation based on risk score
    if risk_score < 0.3:
        llm_integration_session.risk_level = "Low"
        llm_integration_session.explanation = "No significant risk detected."
    elif risk_score < 0.7:
        llm_integration_session.risk_level = "Medium"
        llm_integration_session.explanation = "Medium risk detected. Please be cautious."
    else:
        llm_integration_session.risk_level = "High"
        llm_integration_session.explanation = "High risk detected. Immediate action required."
    
    return llm_integration_session

@router.get("/monitor_llm_integration/{session_id}", response_model=LLMIntegrationSession)
def monitor_llm_integration(session_id: str):
    if session_id not in llm_integration_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return llm_integration_sessions[session_id]
