```
SafeTest-Matrix/
├── backend/
│   ├── app/                           # Python backend application code (FastAPI)
│   │   ├── __init__.py
│   │   ├── main.py                    # Entry point: sets up FastAPI and registers routes
│   │   ├── config.py                  # Configuration settings (e.g., API keys, DB URLs)
│   │   ├── routes/                    # API endpoints for exam modules
│   │   │   ├── exam.py                # Endpoints for exam sessions
│   │   │   ├── secure_env.py          # Secure environment operations (file isolation, app blocking, etc.)
│   │   │   ├── data_collection.py     # Endpoints for behavioral & media data collection
│   │   │   ├── feature_processing.py  # Feature engineering and data normalization
│   │   │   ├── risk_scoring.py        # Implements ML models (LSTM, decision tree) for risk scoring
│   │   │   ├── llm_integration.py     # API for LLM decision-making using SafeTest-Matrix with Llama
│   │   │   ├── interventions.py       # Adaptive interventions based on risk levels
│   │   │   └── post_exam.py           # Post-exam processing (state restoration, risk reports)
│   │   ├── models/                    # Machine Learning and LLM model implementations
│   │   │   ├── risk_model.py          # Risk scoring ML models
│   │   │   └── safe_test_matrix_llama.py  # LLM integration code using Llama (SafeTest-Matrix approach)
│   │   └── utils/                     # Utility modules (logging, data helpers, etc.)
│   │       └── logger.py
│   ├── requirements.txt               # Python dependencies
│   └── Dockerfile                     # Container configuration for deployment
```
