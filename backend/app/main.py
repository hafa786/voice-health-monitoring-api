import uuid
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, UploadFile, HTTPException, Depends, Header # type: ignore
from .audio_analysis import analyze_audio
from .models import AnalysisResult, ThresholdConfig
from fastapi.middleware.cors import CORSMiddleware # type: ignore

# --------------------------
# Basic API Setup
# --------------------------
app = FastAPI(title="Voice Health Monitoring API")



origins = [
    "http://localhost:5173",  # frontend
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # allow frontend
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, OPTIONS, etc
    allow_headers=["*"],          # allow custom headers like X-API-KEY
)

API_KEY = "mysecretkey"  # ⚠️ Replace in prod

def require_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# # --------------------------
# # In-memory storage
# # --------------------------
patients_data: Dict[str, List[Dict]] = {}
alert_thresholds = {
    "pitch": {"low": 80, "high": 300},
    "speech_rate": {"low": 90, "high": 160},
    "pause_duration": {"low": 0.0, "high": 2.0},
    "voice_energy": {"low": 0.3, "high": 1.0},
}


# --------------------------
# API Endpoints
# --------------------------

@app.post("/patients/{id}/voice-samples", dependencies=[Depends(require_api_key)])
async def upload_sample(id: str, file: UploadFile):
    if not file.filename.endswith((".wav", ".mp3", ".flac")):
        raise HTTPException(status_code=400, detail="Invalid file format")

    try:
        temp_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        result = analyze_audio(temp_path, id)
        patients_data.setdefault(id, []).append(result.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

@app.get("/patients/{id}/analysis", response_model=AnalysisResult, dependencies=[Depends(require_api_key)])
async def get_latest(id: str):
    if id not in patients_data or not patients_data[id]:
        raise HTTPException(status_code=404, detail="No samples found")
    return patients_data[id][-1]

@app.get("/patients/{id}/history", dependencies=[Depends(require_api_key)])
async def get_history(id: str):
    if id not in patients_data or not patients_data[id]:
        raise HTTPException(status_code=404, detail="No history found")
    return patients_data[id][-5:]  # last 5

@app.post("/alerts/configure", dependencies=[Depends(require_api_key)])
async def configure_alerts(cfg: ThresholdConfig):
    if cfg.metric not in alert_thresholds:
        raise HTTPException(status_code=400, detail="Invalid metric")
    alert_thresholds[cfg.metric] = {"low": cfg.low, "high": cfg.high}
    return {"message": "Threshold updated", "config": alert_thresholds[cfg.metric]}