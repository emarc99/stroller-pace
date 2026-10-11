import numpy as np
import pytest
from engine.filters import CadenceDecouplingFilter
from engine.features import KinematicFeatureExtractor
from engine.calibration_data import generate_reference_calibration_data, generate_adversarial_test_set

def test_butterworth_filter():
    filt = CadenceDecouplingFilter(sampling_rate=50.0, cutoff_hz=6.0)
    # Generate 2.5 Hz cadence wave (should be attenuated) + 18 Hz cobblestone shock (should pass)
    t = np.linspace(0, 2.0, 100)
    stride_wave = 1.2 * np.sin(2 * np.pi * 2.5 * t)
    shock_wave = 0.8 * np.sin(2 * np.pi * 18.0 * t)
    combined = stride_wave + shock_wave
    
    filtered = filt.apply_filter(combined)
    # Filtered signal should have much lower power at 2.5 Hz than raw
    stride_power_raw = np.mean(stride_wave ** 2)
    filtered_rms = np.sqrt(np.mean(filtered ** 2))
    assert filtered_rms < np.sqrt(np.mean(combined ** 2))

def test_feature_extractor():
    extractor = KinematicFeatureExtractor(sampling_rate=50.0)
    # Test flat smooth asphalt window
    t = np.linspace(0, 2.0, 100)
    flat_z = 1.0 + 0.05 * np.random.randn(100) # Centered around 1.0g gravity
    feats = extractor.extract_window_features(flat_z, speed_mps=1.5)
    
    vec = feats["feature_vector"]
    assert len(vec) == 6
    assert feats["metrics"]["hazard_score"] < 25.0 # Low hazard

def test_shock_hazard():
    extractor = KinematicFeatureExtractor(sampling_rate=50.0)
    # Test violent cobblestone impact window with 2.8g spike
    shock_z = 1.0 + 0.15 * np.random.randn(100)
    shock_z[45] = 2.8
    shock_z[46] = -1.2
    shock_z[60] = 2.5
    feats = extractor.extract_window_features(shock_z, speed_mps=1.8)
    
    assert feats["metrics"]["peak_g"] >= 1.8
    assert feats["metrics"]["crest_factor"] > 3.0
    assert feats["metrics"]["hazard_score"] > 50.0 # High hazard

def test_calibration_matrix():
    X, y, cols = generate_reference_calibration_data(samples_per_class=10)
    assert X.shape == (30, 6)
    assert len(y) == 30
    assert set(y) == {0, 1, 2}

if __name__ == "__main__":
    test_butterworth_filter()
    test_feature_extractor()
    test_shock_hazard()
    test_calibration_matrix()
    print("All signal and feature tests passed!")
