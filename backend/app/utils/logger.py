import logging
from datetime import datetime

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def log_event(event: str):
    """
    Log a general event.
    """
    logger.info(f"Event: {event}")

def log_exam_session_event(session_id: str, event: str):
    """
    Log an event related to an exam session.
    """
    logger.info(f"Exam Session {session_id}: {event}")

def log_risk_score(session_id: str, risk_score: float, risk_level: str):
    """
    Log the risk score and risk level for an exam session.
    """
    logger.info(f"Exam Session {session_id}: Risk Score = {risk_score}, Risk Level = {risk_level}")
