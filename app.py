import os
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from engine.tabpfn_classifier import StrollerPulseTabPFN
from engine.features import KinematicFeatureExtractor
from engine.simulation_profiles import generate_sensor_profile
from engine.benchmark import run_comparative_benchmark

# Initialize application
app = FastAPI(
    title="StrollerPulse API",
    description="Screen-Free Surface Shock & Terrain Watchdog powered by Prior Labs TabPFN",
    version="1.0.0"
)

# Enable CORS for mobile PWA access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy singletons
feature_extractor = KinematicFeatureExtractor(sampling_rate=50.0)
tabpfn_engine = StrollerPulseTabPFN(device="cpu")

# Request Models
class PredictSensorRequest(BaseModel):
    accel_z: Optional[List[float]] = Field(None, description="Raw vertical acceleration samples (approx 50-100 values)")
    feature_vector: Optional[List[float]] = Field(None, description="Precomputed 6D vector: [var_z, rms_z, crest_factor, dom_freq, jerk, speed_mps]")
    speed_mps: float = Field(1.4, description="Forward speed in m/s")
    mode: str = Field("stroller", description="Personality mode: 'stroller' or 'runner'")
    apply_cadence_decoupling: bool = Field(True, description="Enable 4th-order Butterworth filter for leg sway")

class CalibrateRequest(BaseModel):
    custom_reference_vectors: Optional[List[List[float]]] = None
    labels: Optional[List[int]] = None

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "StrollerPulse",
        "primary_partner": "Prior Labs (TabPFN)",
        "model_type": tabpfn_engine.model_type,
        "is_calibrated": tabpfn_engine.is_calibrated,
        "feature_count": 6,
        "classes": ["Natural Earth / Grass", "Smooth Paved Asphalt", "Severe Cobblestone Hazard"],
        "timestamp": time.time()
    }

@app.post("/api/predict")
def predict_terrain(req: PredictSensorRequest):
    """
    Classifies terrain and calculates physical G-shock hazard in real-time.
    """
    if req.feature_vector is not None and len(req.feature_vector) == 6:
        # Pre-computed feature vector passed directly
        features = req.feature_vector
        metrics = {
            "var_z": features[0],
            "rms_z": features[1],
            "crest_factor": features[2],
            "dom_freq": features[3],
            "jerk": features[4],
            "speed_mps": features[5],
            "hazard_score": min(100.0, (features[1] * 45.0) + (features[2] * 7.0)),
            "is_cadence_dominated": False
        }
    elif req.accel_z is not None and len(req.accel_z) > 0:
        # Extract features from raw inertial series
        extracted = feature_extractor.extract_window_features(
            req.accel_z, 
            speed_mps=req.speed_mps,
            apply_cadence_decoupling=req.apply_cadence_decoupling
        )
        features = extracted["feature_vector"]
        metrics = extracted["metrics"]
    else:
        raise HTTPException(status_code=400, detail="Must provide either 'accel_z' series or 'feature_vector'")

    # Run TabPFN Foundation Model inference
    prediction = tabpfn_engine.predict(features)

    # Adjust audio cue based on personality mode
    pred_class = prediction["predicted_class"]
    if req.mode == "runner":
        if pred_class == 0:
            audio_text = "Soft natural trail. Joint reaction forces down 42%. Great cushion for knees."
        elif pred_class == 1:
            audio_text = "Asphalt roadway. Consider drifting to the grass verge for joint cushion."
        else:
            audio_text = f"Warning: Severe road shock detected ({metrics['crest_factor']:.1f} crest factor). High knee impact."
    else: # stroller mode
        audio_text = prediction["audio_cue"]

    return {
        "status": "success",
        "predicted_class": pred_class,
        "class_name": prediction["class_name"],
        "short_name": prediction["short_name"],
        "badge": prediction["badge"],
        "color": prediction["color"],
        "description": prediction["description"],
        "hazard_score": round(metrics["hazard_score"], 1),
        "probabilities": prediction["probabilities"],
        "feature_vector": features,
        "metrics": metrics,
        "audio_cue": audio_text,
        "model_type": prediction["model_type"],
        "latency_ms": prediction["latency_ms"]
    }

@app.get("/api/benchmark")
def get_benchmark():
    """
    Executes on-demand comparative benchmark across TabPFN and all standard baselines.
    """
    return run_comparative_benchmark(n_runs=3)

@app.get("/api/simulate/{profile_id}")
def get_simulation_profile(profile_id: str):
    """
    Returns pre-recorded inertial waveforms for desktop evaluation.
    Available profiles: 'grass', 'asphalt', 'cobblestones', 'runner_cadence', 'mixed_trail'
    """
    allowed = ["grass", "asphalt", "cobblestones", "runner_cadence", "mixed_trail"]
    if profile_id not in allowed:
        raise HTTPException(status_code=404, detail=f"Profile '{profile_id}' not found. Choose from {allowed}")
    return generate_sensor_profile(profile_id)

# Serve client web application
public_dir = os.path.join(os.path.dirname(__file__), "public")
if os.path.exists(public_dir):
    app.mount("/static", StaticFiles(directory=public_dir), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(public_dir, "index.html"))

    @app.get("/{full_path:path}")
    def serve_static(full_path: str):
        path = os.path.join(public_dir, full_path)
        if os.path.exists(path) and os.path.isfile(path):
            return FileResponse(path)
        return FileResponse(os.path.join(public_dir, "index.html"))
