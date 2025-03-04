from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Optional, List
from datetime import datetime
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from keras.models import Sequential
from keras.layers import LSTM, Dense

router = APIRouter()

class RiskScoringSession(BaseModel):
    session_id: str
    candidate_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str
    features: Optional[Dict[str, float]] = {}
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None

risk_scoring_sessions: Dict[str, RiskScoringSession] = {}

# Initialize ML models
decision_tree_model = DecisionTreeClassifier()
lstm_model = Sequential()
lstm_model.add(LSTM(50, return_sequences=True, input_shape=(1, 10)))
lstm_model.add(LSTM(50))
lstm_model.add(Dense(1, activation='sigmoid'))
lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

@router.post("/start_risk_scoring", response_model=RiskScoringSession)
def start_risk_scoring(session_id: str, candidate_id: str):
    if session_id in risk_scoring_sessions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session already exists")
    risk_scoring_session = RiskScoringSession(session_id=session_id, candidate_id=candidate_id, start_time=datetime.now(), status="ongoing")
    risk_scoring_sessions[session_id] = risk_scoring_session
    return risk_scoring_session

@router.post("/stop_risk_scoring", response_model=RiskScoringSession)
def stop_risk_scoring(session_id: str):
    if session_id not in risk_scoring_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    risk_scoring_session = risk_scoring_sessions[session_id]
    risk_scoring_session.end_time = datetime.now()
    risk_scoring_session.status = "completed"
    return risk_scoring_session

@router.post("/add_feature", response_model=RiskScoringSession)
def add_feature(session_id: str, feature_name: str, feature_value: float):
    if session_id not in risk_scoring_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    risk_scoring_session = risk_scoring_sessions[session_id]
    risk_scoring_session.features[feature_name] = feature_value
    return risk_scoring_session

@router.post("/calculate_risk_score", response_model=RiskScoringSession)
def calculate_risk_score(session_id: str):
    if session_id not in risk_scoring_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    risk_scoring_session = risk_scoring_sessions[session_id]
    features = np.array(list(risk_scoring_session.features.values())).reshape(1, -1)
    
    # Calculate risk score using decision tree
    decision_tree_score = decision_tree_model.predict(features)[0]
    
    # Calculate risk score using LSTM
    lstm_score = lstm_model.predict(features.reshape(1, 1, -1))[0][0]
    
    # Combine scores (example: average)
    risk_score = (decision_tree_score + lstm_score) / 2
    risk_scoring_session.risk_score = risk_score
    
    # Categorize risk level
    if risk_score < 0.3:
        risk_scoring_session.risk_level = "Low"
    elif risk_score < 0.7:
        risk_scoring_session.risk_level = "Medium"
    else:
        risk_scoring_session.risk_level = "High"
    
    return risk_scoring_session

@router.get("/monitor_risk_scoring/{session_id}", response_model=RiskScoringSession)
def monitor_risk_scoring(session_id: str):
    if session_id not in risk_scoring_sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return risk_scoring_sessions[session_id]
