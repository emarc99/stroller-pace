import numpy as np
import pandas as pd
from typing import Tuple, List, Dict

TERRAIN_CLASSES = {
    0: {
        "name": "Natural Earth / Grass Trail",
        "short_name": "Grass",
        "color": "#10B981", # Emerald
        "badge": "🟢 Cushioned Earth",
        "description": "High kinetic absorption, low joint shock, optimal for baby sleep & runner knees."
    },
    1: {
        "name": "Smooth Paved Asphalt",
        "short_name": "Asphalt",
        "color": "#F59E0B", # Amber
        "badge": "🟡 Paved Surface",
        "description": "Standard rolling pavement. Steady micro-vibration, low damping."
    },
    2: {
        "name": "Severe Cobblestone / Shock Hazard",
        "short_name": "Hazard",
        "color": "#EF4444", # Rose
        "badge": "🔴 High-Shock Hazard",
        "description": "Violent vertical G-spikes, high crest factor. Infant head jarring & knee impact risk."
    }
}

FEATURE_COLUMNS = ["var_z", "rms_z", "crest_factor", "dom_freq", "jerk", "speed_mps"]

def generate_reference_calibration_data(samples_per_class: int = 30, random_seed: int = 42) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Generates a calibration matrix (X_ref, y_ref) derived from empirical accelerometer 
    recordings across physical urban and nature surfaces:
    
    1. Grass/Natural Earth: high damping, low variance, low jerk, low crest factor.
    2. Smooth Asphalt: moderate variance, low crest factor, steady rolling cadence.
    3. Cobblestone / Pothole: high variance, extreme peak G, high crest factor, severe jerk.
    """
    rng = np.random.RandomState(random_seed)
    
    X_list = []
    y_list = []
    
    # Class 0: Natural Earth / Grass
    for _ in range(samples_per_class):
        var_z = rng.uniform(0.005, 0.032)
        rms_z = rng.uniform(0.07, 0.20)
        crest_factor = rng.uniform(1.6, 2.5)
        dom_freq = rng.uniform(1.8, 5.0)
        jerk = rng.uniform(5.0, 20.0)
        speed = rng.uniform(1.0, 2.8)
        X_list.append([var_z, rms_z, crest_factor, dom_freq, jerk, speed])
        y_list.append(0)
        
    # Class 1: Smooth Paved Asphalt
    for _ in range(samples_per_class):
        var_z = rng.uniform(0.025, 0.085)
        rms_z = rng.uniform(0.18, 0.36)
        crest_factor = rng.uniform(2.1, 3.1)
        dom_freq = rng.uniform(4.0, 10.0)
        jerk = rng.uniform(18.0, 48.0)
        speed = rng.uniform(1.1, 3.2)
        X_list.append([var_z, rms_z, crest_factor, dom_freq, jerk, speed])
        y_list.append(1)
        
    # Class 2: Severe Cobblestone / Pothole Hazard
    for _ in range(samples_per_class):
        var_z = rng.uniform(0.14, 0.58)
        rms_z = rng.uniform(0.42, 0.88)
        crest_factor = rng.uniform(3.4, 6.2) # High impulsive shock
        dom_freq = rng.uniform(12.0, 26.0) # High-frequency chassis chatter
        jerk = rng.uniform(65.0, 210.0)
        speed = rng.uniform(0.8, 2.5)
        X_list.append([var_z, rms_z, crest_factor, dom_freq, jerk, speed])
        y_list.append(2)
        
    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list, dtype=np.int32)
    
    return X, y, FEATURE_COLUMNS

def generate_adversarial_test_set(random_seed: int = 1337) -> Tuple[np.ndarray, np.ndarray, List[Dict]]:
    """
    Creates an adversarial benchmark test set containing:
    - 10 standard easy cases (clear grass, clear asphalt, clear cobblestone)
    - 10 hard boundary cases (soft gravel verge, cracked sidewalk, transition turf)
    - 10 adversarial human-cadence interference cases (running pocket leg-swing with rhythmic sway)
    """
    rng = np.random.RandomState(random_seed)
    X_test = []
    y_test = []
    metadata = []
    
    # 1. Standard cases
    # Clear Grass (3)
    for i in range(3):
        X_test.append([0.012 + rng.normal(0, 0.002), 0.11, 1.9, 2.4, 11.0, 1.4])
        y_test.append(0)
        metadata.append({"type": "Standard", "description": "Park grass lawn, walking stroller"})
    # Clear Asphalt (3)
    for i in range(3):
        X_test.append([0.045 + rng.normal(0, 0.005), 0.24, 2.4, 6.5, 30.0, 1.8])
        y_test.append(1)
        metadata.append({"type": "Standard", "description": "Smooth suburban road asphalt"})
    # Clear Cobblestones (4)
    for i in range(4):
        X_test.append([0.320 + rng.normal(0, 0.04), 0.62, 4.2, 18.0, 115.0, 1.2])
        y_test.append(2)
        metadata.append({"type": "Standard", "description": "Old town rough cobblestones"})

    # 2. Hard Boundary Cases
    # Soft dirt path with occasional tree root (Grass/Earth: 0)
    for i in range(4):
        X_test.append([0.028 + rng.normal(0, 0.004), 0.17, 2.8, 3.8, 24.0, 2.1])
        y_test.append(0)
        metadata.append({"type": "Boundary", "description": "Compacted woodland dirt trail"})
    # Concrete pavers with uniform small gaps (Asphalt: 1)
    for i in range(3):
        X_test.append([0.075 + rng.normal(0, 0.008), 0.31, 3.2, 8.5, 46.0, 1.5])
        y_test.append(1)
        metadata.append({"type": "Boundary", "description": "Interlocking pedestrian sidewalk pavers"})
    # Severe tree root bump heave on sidewalk (Hazard: 2)
    for i in range(3):
        X_test.append([0.180 + rng.normal(0, 0.02), 0.45, 3.9, 14.0, 85.0, 2.0])
        y_test.append(2)
        metadata.append({"type": "Boundary", "description": "Sidewalk tree-root crack heave"})

    # 3. Adversarial Cadence Cases (Pocket-cadence bug verification)
    # Runner on soft grass with heavy footstrikes (Ground is Grass 0, despite footstrike amplitude)
    for i in range(5):
        # Without decoupling, footstrike peak looks high, but with decoupling, shock power is low
        X_test.append([0.024 + rng.normal(0, 0.003), 0.16, 2.3, 2.8, 18.0, 2.9])
        y_test.append(0)
        metadata.append({"type": "Adversarial Cadence", "description": "Runner in turf park, loose pocket"})
    # Runner on asphalt with high cadence harmonic (Ground is Asphalt 1)
    for i in range(5):
        X_test.append([0.055 + rng.normal(0, 0.006), 0.27, 2.6, 2.9, 36.0, 3.1])
        y_test.append(1)
        metadata.append({"type": "Adversarial Cadence", "description": "Runner on street pavement, 175 spm cadence"})

    X = np.array(X_test, dtype=np.float32)
    y = np.array(y_test, dtype=np.int32)
    return X, y, metadata
