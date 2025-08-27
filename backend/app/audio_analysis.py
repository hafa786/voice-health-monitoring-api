import librosa # type: ignore
from .models import AnalysisResult, HealthIndicators, Metric
import uuid
import numpy as np # type: ignore
from datetime import datetime
from typing import Dict, List

# --------------------------
# In-memory storage
# --------------------------
patients_data: Dict[str, List[Dict]] = {}
alert_thresholds = {
    "pitch": {"low": 80, "high": 300},
    "speech_rate": {"low": 90, "high": 160},
    "pause_duration": {"low": 0.0, "high": 2.0},
    "voice_energy": {"low": 0.3, "high": 1.0},
}

def analyze_audio(file_path: str, patient_id: str) -> AnalysisResult:
    """Process audio file and compute metrics"""

    y, sr = librosa.load(file_path, sr=16000)

    # 1. Pitch (median fundamental frequency)
    pitches, _, _ = librosa.pyin(
        y, fmin=librosa.note_to_hz("C2"), fmax=librosa.note_to_hz("C7")
    )
    pitch_val = float(np.nanmedian(pitches)) if np.any(~np.isnan(pitches)) else 0.0

    # 2. Energy
    energy_val = float(np.mean(librosa.feature.rms(y=y)))

    # 3. Speaking rate (approx via syllables / sec -> words/min)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    speech_rate_val = float(tempo)  # crude approximation

    # 4. Pauses (count near-zero segments)
    intervals = librosa.effects.split(y, top_db=30)
    pauses = []
    last_end = 0
    for start, end in intervals:
        pause = (start - last_end) / sr
        if pause > 0:
            pauses.append(pause)
        last_end = end
    pause_val = float(np.mean(pauses)) if pauses else 0.0

    # --------------------------
    # Evaluate against thresholds
    # --------------------------
    def status(metric: str, value: float) -> str:
        th = alert_thresholds[metric]
        if value < th["low"] or value > th["high"]:
            return "critical"
        if value < th["low"] * 1.1 or value > th["high"] * 0.9:
            return "warning"
        return "normal"

    metrics = {
        "pitch": Metric(value=round(pitch_val, 2), unit="Hz", status=status("pitch", pitch_val)),
        "speech_rate": Metric(value=round(speech_rate_val, 2), unit="words/min", status=status("speech_rate", speech_rate_val)),
        "pause_duration": Metric(value=round(pause_val, 2), unit="seconds", status=status("pause_duration", pause_val)),
        "voice_energy": Metric(value=round(energy_val, 2), unit="normalized", status=status("voice_energy", energy_val)),
    }

    # --------------------------
    # Health indicators
    # --------------------------
    fatigue_score = min(1.0, 1 - energy_val)  # crude
    stress_indicator = min(1.0, pitch_val / 500)  # crude

    if any(m.status == "critical" for m in metrics.values()):
        overall_status = "critical"
    elif any(m.status == "warning" for m in metrics.values()):
        overall_status = "attention_needed"
    else:
        overall_status = "normal"

    recommendations = []
    if overall_status != "normal":
        recommendations.append("Consider follow-up")
    if fatigue_score > 0.6:
        recommendations.append("Check medication timing")

    result = AnalysisResult(
        sample_id=str(uuid.uuid4()),
        timestamp=datetime.utcnow().isoformat(),
        patient_id=patient_id,
        metrics=metrics,
        health_indicators=HealthIndicators(
            fatigue_score=round(fatigue_score, 2),
            stress_indicator=round(stress_indicator, 2),
            overall_status=overall_status,
        ),
        recommendations=recommendations or ["No action needed"],
    )
    return result