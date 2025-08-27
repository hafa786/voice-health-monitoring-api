from pydantic import BaseModel, Field # type: ignore
from typing import Dict, List, Optional, Literal


Status = Literal["normal", "warning", "critical"]


class MetricReading(BaseModel):
    value: float
    unit: str
    status: Status

class Metric(BaseModel):
    value: float
    unit: str
    status: str
    
class HealthIndicators(BaseModel):
    fatigue_score: float
    stress_indicator: float
    overall_status: Literal["normal", "attention_needed", "critical"]


class AnalysisResult(BaseModel):
    sample_id: str
    timestamp: str
    patient_id: str
    metrics: Dict[str, MetricReading]
    health_indicators: HealthIndicators
    recommendations: List[str]


class Thresholds(BaseModel):
    # define ranges; missing keys are ignored on update
    pitch: Optional[Dict[str, float]] = None # {low, high, critical_low, critical_high}
    speech_rate: Optional[Dict[str, float]] = None
    pause_duration: Optional[Dict[str, float]] = None
    voice_energy: Optional[Dict[str, float]] = None
    
    
class ThresholdConfig(BaseModel):
    metric: str
    low: float
    high: float
