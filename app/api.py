import json, os, time
from pathlib import Path
import joblib, numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .schemas import AssessmentInput, AssessmentResult
from .recommendations import make_recommendations
from .database import init_db, save_assessment, recent_assessments
from .metrics import PREDICTIONS, LATENCY, ERRORS, MODEL_READY

MODEL_PATH = Path(os.getenv("MODEL_PATH", "/app/models/models.joblib"))
FEATURES = ["age","height_cm","weight_kg","athlete","fruit_servings_day","vegetable_servings_day","protein_g_day","fibre_g_day","sugar_g_day","sodium_mg_day","fat_g_day","fried_meals_week","processed_meals_week","exercise_min_week","sleep_hours_day","water_l_day","sedentary_hours_day"]
app = FastAPI(title="AI Health & Lifestyle Risk Monitoring API", version="1.0.0", description="Educational demo only; not a diagnostic tool.")
models = None
@app.on_event("startup")
def startup():
    global models
    init_db()
    if MODEL_PATH.exists():
        models = joblib.load(MODEL_PATH); MODEL_READY.set(1)
    else: print("Model missing:", MODEL_PATH)
@app.get("/")
def root(): return {"message":"AI Health & Lifestyle Risk Monitoring API","docs":"/docs"}
@app.get("/health")
def health(): return {"status":"ok","model_loaded":models is not None}
@app.get("/foods")
def foods():
    from .nutrition import list_foods
    return list_foods()
@app.get("/history")
def history(): return recent_assessments()
@app.get("/metrics")
def metrics(): return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
@app.post("/predict", response_model=AssessmentResult)
def predict(payload: AssessmentInput):
    if models is None:
        ERRORS.inc(); raise HTTPException(status_code=503, detail="Model not loaded. Check trainer logs.")
    x = payload.model_dump()
    row = [float(x[k]) for k in FEATURES]
    try:
        with LATENCY.time():
            score = float(np.clip(models["regressor"].predict([row])[0], 0, 100))
            cls = int(models["classifier"].predict([row])[0])
        risk = {0:"Low",1:"Moderate",2:"High"}.get(cls,"Moderate")
        bmi = round(x["weight_kg"] / ((x["height_cm"]/100)**2), 1)
        recs = make_recommendations(x)
        aid = save_assessment(json.dumps(x), score, risk)
        PREDICTIONS.inc()
        return AssessmentResult(score=round(score,1),risk_category=risk,recommendations=recs,bmi=bmi,
          model_note="Model trained on synthetic demonstration data; not clinically validated.",assessment_id=aid)
    except Exception as e:
        ERRORS.inc(); raise HTTPException(status_code=500, detail=str(e))
