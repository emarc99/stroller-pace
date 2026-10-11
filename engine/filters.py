import numpy as np
from scipy import signal
from typing import Tuple, Dict

class CadenceDecouplingFilter:
    """
    Dual-Stage Cadence Decoupling Filter for StrollerPulse.
    
    Solves the 'Pocket-Cadence vs Wheel-Rumble' bug documented in our postmortem:
    When a phone is carried in a runner's pocket or strapped to a stroller handle,
    rhythmic vertical leg swing / arm sway generates large amplitude oscillations 
    at 2.0-3.2 Hz (up to 1.8g). Simple peak detectors mistake this for violent cobblestone
    shocks, yielding false alarm rates up to 38.4%.
    
    This filter isolates the high-frequency impact vibrations (>6.0 Hz) using a 4th-order
    Butterworth high-pass filter, while simultaneously estimating the cadence harmonic
    via spectral autocorrelation to decouple human body motion from terrain shock.
    """
    def __init__(self, sampling_rate: float = 50.0, cutoff_hz: float = 6.0, order: int = 4):
        self.sampling_rate = sampling_rate
        self.cutoff_hz = cutoff_hz
        self.order = order
        
        # Design Butterworth filter
        nyquist = 0.5 * sampling_rate
        normal_cutoff = cutoff_hz / nyquist
        # Ensure cutoff is within (0, 1)
        normal_cutoff = max(0.01, min(0.95, normal_cutoff))
        self.b, self.a = signal.butter(order, normal_cutoff, btype='high', analog=False)

    def apply_filter(self, data: np.ndarray) -> np.ndarray:
        """
        Applies zero-phase forward-backward Butterworth filter.
        Removes stride/sway frequencies below 6.0 Hz.
        """
        if len(data) < 15:
            # Need minimum sample length for 4th order filtfilt
            return data
        try:
            return signal.filtfilt(self.b, self.a, data)
        except Exception:
            # Fallback for short buffers
            return data - np.mean(data)

    def analyze_spectral_bands(self, raw_z: np.ndarray) -> Dict[str, float]:
        """
        Computes power distribution across biomechanical and terrain frequency bands:
        - Cadence Band (1.5 - 3.5 Hz): Human walking/running stride.
        - Transition Band (3.5 - 8.0 Hz): Medium stroller wheel bounce & body sway.
        - Shock Band (8.0 - 25.0 Hz): Cobblestone chatter, severe joint jars, chassis vibration.
        """
        n = len(raw_z)
        if n < 16:
            return {
                "cadence_power": 0.0,
                "transition_power": 0.0,
                "shock_power": 0.0,
                "dominant_freq": 0.0,
                "cadence_to_shock_ratio": 1.0,
                "is_cadence_dominated": True
            }

        # Detrend and windowing
        detrended = raw_z - np.mean(raw_z)
        window = np.hanning(n)
        fft_vals = np.fft.rfft(detrended * window)
        fft_freqs = np.fft.rfftfreq(n, d=1.0 / self.sampling_rate)
        psd = (np.abs(fft_vals) ** 2) / n

        # Find dominant peak
        dom_idx = np.argmax(psd[1:]) + 1 if len(psd) > 1 else 0
        dom_freq = float(fft_freqs[dom_idx]) if dom_idx < len(fft_freqs) else 0.0

        # Band powers
        cadence_mask = (fft_freqs >= 1.5) & (fft_freqs < 3.5)
        trans_mask = (fft_freqs >= 3.5) & (fft_freqs < 8.0)
        shock_mask = (fft_freqs >= 8.0) & (fft_freqs <= 25.0)

        cadence_p = float(np.sum(psd[cadence_mask]))
        trans_p = float(np.sum(psd[trans_mask]))
        shock_p = float(np.sum(psd[shock_mask]))
        total_p = cadence_p + trans_p + shock_p + 1e-6

        c_to_s = cadence_p / (shock_p + 1e-4)

        return {
            "cadence_power": float(cadence_p / total_p),
            "transition_power": float(trans_p / total_p),
            "shock_power": float(shock_p / total_p),
            "dominant_freq": dom_freq,
            "cadence_to_shock_ratio": float(c_to_s),
            "is_cadence_dominated": bool(c_to_s > 2.2 and shock_p < 0.25)
        }
