import time
import hashlib
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import joblib
import pandas as pd

from app.model import CreditApplication, PredictionResponse
from app.logging_config import setup_logging

app = FastAPI(title="Credit Risk Scoring API")
logger = setup_logging()

model = joblib.load("model_artifacts/credit_model.joblib")

# personal_status_sex encodes marital status + gender — sensitive, so we hash it
# instead of dropping it (model still needs it as a feature), and only the HASH is logged
def hash_sensitive(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:12]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(application: CreditApplication, request: Request):
    start = time.time()

    input_df = pd.DataFrame([application.model_dump()])
    proba = model.predict_proba(input_df)[0, 1]
    label = "high_risk" if proba >= 0.5 else "low_risk"

    latency_ms = (time.time() - start) * 1000

    # log only non-PII fields + a hash of the sensitive one — never the raw value
    logger.info("prediction_made", extra={
        "duration": application.duration,
        "credit_amount": application.credit_amount,
        "purpose": application.purpose,
        "personal_status_sex_hash": hash_sensitive(application.personal_status_sex),
        "risk_probability": round(float(proba), 4),
        "risk_label": label,
        "latency_ms": round(latency_ms, 2),
    })

    return PredictionResponse(risk_probability=round(float(proba), 4), risk_label=label)