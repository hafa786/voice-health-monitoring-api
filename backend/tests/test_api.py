import io
import pytest # type: ignore
import soundfile as sf # type: ignore
import numpy as np # type: ignore
from fastapi.testclient import TestClient # type: ignore
from app.main import app, API_KEY

client = TestClient(app)

HEADERS = {"X-API-KEY": API_KEY}
PATIENT_ID = "P001"


def test_upload_invalid_file_format():
    """Uploading wrong file type should return 400"""
    response = client.post(
        f"/patients/{PATIENT_ID}/voice-samples",
        headers=HEADERS,
        files={"file": ("test.txt", b"fake data", "text/plain")},
    )
    assert response.status_code == 400
    assert "Invalid file format" in response.json()["detail"]


def test_upload_and_analysis_flow(tmp_path):
    """Upload audio -> get latest -> get history"""
    # Generate a fake silent wav file

    wav_path = tmp_path / "test.wav"
    sr = 16000
    data = np.zeros(sr)  # 1 second of silence
    sf.write(wav_path, data, sr)

    with open(wav_path, "rb") as f:
        response = client.post(
            f"/patients/{PATIENT_ID}/voice-samples",
            headers=HEADERS,
            files={"file": ("test.wav", f, "audio/wav")},
        )
    assert response.status_code == 200
    result = response.json()
    assert "metrics" in result
    assert result["patient_id"] == PATIENT_ID

    # Latest analysis
    response = client.get(f"/patients/{PATIENT_ID}/analysis", headers=HEADERS)
    assert response.status_code == 200
    latest = response.json()
    assert latest["patient_id"] == PATIENT_ID
    assert "health_indicators" in latest

    # History (should include at least 1 entry)
    response = client.get(f"/patients/{PATIENT_ID}/history", headers=HEADERS)
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) >= 1


def test_configure_alerts():
    """Update threshold config"""
    response = client.post(
        "/alerts/configure",
        headers=HEADERS,
        json={"metric": "pitch", "low": 50, "high": 400},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["config"]["low"] == 50
    assert data["config"]["high"] == 400


def test_authentication_required():
    """Requests without API key should fail"""
    response = client.get(f"/patients/{PATIENT_ID}/analysis")
    assert response.status_code == 422 or response.status_code == 401
