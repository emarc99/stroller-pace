import numpy as np
from typing import List, Dict, Any, Union
from .filters import CadenceDecouplingFilter

class KinematicFeatureExtractor:
    """
    Extracts physically grounded vibration, shock, and terrain kinematic features 
    from rolling inertial sensor windows (typically 2.0s window at 50 Hz = ~100 samples).
    
    Adheres strictly to the ISO 2631 Mechanical Vibration & Shock Evaluation Standard.
    """
    def __init__(self, sampling_rate: float = 50.0):
        self.sampling_rate = sampling_rate
        self.dt = 1.0 / sampling_rate
        self.cadence_filter = CadenceDecouplingFilter(sampling_rate=sampling_rate)

    def extract_window_features(
        self, 
        accel_z: Union[List[float], np.ndarray], 
        speed_mps: float = 1.4,
        apply_cadence_decoupling: bool = True
    ) -> Dict[str, Any]:
        """
        Transforms raw vertical acceleration series into the 6D feature vector 
        required by TabPFN, plus diagnostic telemetry.
        
        Args:
            accel_z: Raw vertical acceleration values (in g or m/s^2 normalized to 1g = 9.81 m/s^2).
                     Expected input in g (where 1.0g = standard Earth gravity).
            speed_mps: Current forward speed in meters/sec (from GPS or pedometer).
            apply_cadence_decoupling: Whether to apply the Butterworth high-pass filter.
        
        Returns:
            Dictionary containing both the raw TabPFN feature vector and telemetry metadata.
        """
        z_arr = np.asarray(accel_z, dtype=np.float64)
        if len(z_arr) == 0:
            return self._empty_feature_set()

        # Center raw acceleration by subtracting 1.0g gravity baseline if not already centered
        mean_val = np.mean(z_arr)
        if 0.6 <= mean_val <= 1.4:
            # Contains gravity offset; center around baseline
            z_dyn = z_arr - mean_val
        else:
            z_dyn = z_arr - mean_val

        # 1. Spectral Analysis & Cadence Decoupling
        spectral_metrics = self.cadence_filter.analyze_spectral_bands(z_dyn)

        # 2. Filtered vibration series (high-passed to remove leg sway if enabled)
        if apply_cadence_decoupling:
            filtered_z = self.cadence_filter.apply_filter(z_dyn)
        else:
            filtered_z = z_dyn

        # 3. Variance
        var_z = float(np.var(filtered_z))

        # 4. Root Mean Square (RMS) Vibration (ISO 2631)
        rms_z = float(np.sqrt(np.mean(filtered_z ** 2)))
        rms_z = max(rms_z, 1e-5)

        # 5. Crest Factor (Impulsive Shock Severity: Peak / RMS)
        peak_z = float(np.max(np.abs(filtered_z)))
        crest_factor = float(peak_z / rms_z)

        # 6. Jerk Magnitude (Rate of Acceleration Change: da/dt)
        if len(filtered_z) > 1:
            jerk_series = np.diff(filtered_z) / self.dt
            mean_jerk = float(np.mean(np.abs(jerk_series)))
        else:
            mean_jerk = 0.0

        # 7. Dominant Frequency Harmonic
        dom_freq = spectral_metrics["dominant_freq"]

        # 8. G-Shock Hazard Index (0 to 100 continuous score)
        # Empirical weighting: 40% Peak G, 30% RMS, 20% Crest Factor, 10% Jerk
        raw_hazard = (peak_z * 25.0) + (rms_z * 40.0) + (max(0.0, crest_factor - 1.5) * 8.0) + (mean_jerk * 0.15)
        # Attenuate hazard if Cadence Decoupling identifies purely rhythmic runner leg-sway on smooth ground
        if spectral_metrics["is_cadence_dominated"] and peak_z < 1.6:
            raw_hazard *= 0.35  # Suppress false alarm from body sway

        hazard_score = float(np.clip(raw_hazard, 0.0, 100.0))

        # Vector format for TabPFN: [var_z, rms_z, crest_factor, dom_freq, jerk, speed_mps]
        feature_vector = [
            round(var_z, 5),
            round(rms_z, 5),
            round(crest_factor, 4),
            round(dom_freq, 2),
            round(mean_jerk, 4),
            round(float(speed_mps), 2)
        ]

        return {
            "feature_vector": feature_vector,
            "feature_names": ["var_z", "rms_z", "crest_factor", "dom_freq", "jerk", "speed_mps"],
            "metrics": {
                "var_z": var_z,
                "rms_z": rms_z,
                "crest_factor": crest_factor,
                "peak_g": peak_z,
                "mean_jerk": mean_jerk,
                "dom_freq": dom_freq,
                "speed_mps": speed_mps,
                "hazard_score": hazard_score,
                "cadence_power": spectral_metrics["cadence_power"],
                "shock_power": spectral_metrics["shock_power"],
                "is_cadence_dominated": spectral_metrics["is_cadence_dominated"]
            }
        }

    def _empty_feature_set(self) -> Dict[str, Any]:
        return {
            "feature_vector": [0.0, 0.0, 1.0, 0.0, 0.0, 1.4],
            "feature_names": ["var_z", "rms_z", "crest_factor", "dom_freq", "jerk", "speed_mps"],
            "metrics": {
                "var_z": 0.0,
                "rms_z": 0.0,
                "crest_factor": 1.0,
                "peak_g": 0.0,
                "mean_jerk": 0.0,
                "dom_freq": 0.0,
                "speed_mps": 1.4,
                "hazard_score": 0.0,
                "cadence_power": 0.0,
                "shock_power": 0.0,
                "is_cadence_dominated": False
            }
        }
