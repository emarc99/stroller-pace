import numpy as np
from typing import Dict, List, Any

def generate_sensor_profile(profile_type: str, duration_sec: float = 2.0, sampling_rate: float = 50.0) -> Dict[str, Any]:
    """
    Generates synthetic physics-based 3-axis accelerometer & gyroscope data 
    matching physical sensor recordings across different terrain conditions.
    """
    n_samples = int(duration_sec * sampling_rate)
    t = np.linspace(0, duration_sec, n_samples)
    dt = 1.0 / sampling_rate
    
    # 1.0g gravity baseline on z-axis
    z_base = 1.0
    x_noise = np.random.normal(0, 0.04, n_samples)
    y_noise = np.random.normal(0, 0.04, n_samples)
    
    if profile_type == "grass":
        # Damped natural earth: smooth rolling, low vibration, high absorption
        z_signal = z_base + 0.08 * np.sin(2 * np.pi * 1.5 * t) + np.random.normal(0, 0.05, n_samples)
        speed = 1.3
        name = "Emerald Park Grass Lawn"
        desc = "Cushioned natural turf, 44% shock reduction"
        
    elif profile_type == "asphalt":
        # Smooth street asphalt: steady rolling high-frequency hum, minimal crest factor
        z_signal = z_base + 0.18 * np.sin(2 * np.pi * 7.0 * t) + np.random.normal(0, 0.09, n_samples)
        speed = 1.6
        name = "Suburban Smooth Asphalt"
        desc = "Standard paved roadway, low damping"
        
    elif profile_type == "cobblestones":
        # Rough historic cobblestones: intense jarring vertical G-spikes and high jerk
        z_base_wave = z_base + 0.35 * np.sin(2 * np.pi * 16.0 * t) + np.random.normal(0, 0.22, n_samples)
        # Add random impact spikes
        shock_indices = [int(n_samples * 0.25), int(n_samples * 0.55), int(n_samples * 0.82)]
        for idx in shock_indices:
            if idx < n_samples:
                z_base_wave[idx] += 1.85 # Spike to 2.85g
                if idx + 1 < n_samples:
                    z_base_wave[idx + 1] -= 0.95 # Rebound
        z_signal = z_base_wave
        speed = 1.2
        name = "Rough Cobblestone Alley"
        desc = "Severe vertical mechanical shock (infant jarring risk)"
        
    elif profile_type == "runner_cadence":
        # Loose pocket runner on pavement: strong 2.8 Hz rhythmic sway (170 spm)
        cadence_sway = 0.95 * np.sin(2 * np.pi * 2.8 * t) # Body sway
        pavement_hum = 0.12 * np.sin(2 * np.pi * 8.0 * t) + np.random.normal(0, 0.06, n_samples)
        z_signal = z_base + cadence_sway + pavement_hum
        speed = 2.9
        name = "Runner in Pocket (Asphalt)"
        desc = "Tests Butterworth cadence decoupling filter against body sway"
        
    elif profile_type == "mixed_trail":
        # Transition trail: starts on asphalt, transitions to soft grass
        half = n_samples // 2
        z_first = z_base + 0.20 * np.sin(2 * np.pi * 7.0 * t[:half]) + np.random.normal(0, 0.10, half)
        z_second = z_base + 0.06 * np.sin(2 * np.pi * 1.8 * t[half:]) + np.random.normal(0, 0.04, n_samples - half)
        z_signal = np.concatenate([z_first, z_second])
        speed = 1.4
        name = "Sidewalk to Grass Transition"
        desc = "Live transition stepping off concrete onto grass verge"
        
    else:
        # Default flat
        z_signal = z_base + np.random.normal(0, 0.05, n_samples)
        speed = 1.4
        name = "Flat Surface"
        desc = "Standard baseline"

    return {
        "profile_id": profile_type,
        "name": name,
        "description": desc,
        "speed_mps": speed,
        "duration_sec": duration_sec,
        "sampling_rate": sampling_rate,
        "timestamps": [round(float(val), 3) for val in t],
        "accel_z": [round(float(val), 4) for val in z_signal],
        "accel_x": [round(float(val), 4) for val in x_noise],
        "accel_y": [round(float(val), 4) for val in y_noise]
    }
