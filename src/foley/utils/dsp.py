"""Small DSP helpers shared across plugins."""

from __future__ import annotations

import numpy as np


def normalize_peak(audio: np.ndarray, target_db: float = -3.0) -> np.ndarray:
    peak = float(np.max(np.abs(audio)))
    if peak < 1e-9:
        return audio
    target = 10 ** (target_db / 20.0)
    return (audio * (target / peak)).astype(np.float32)


def apply_fade(audio: np.ndarray, sample_rate: int, ms: float = 8.0) -> np.ndarray:
    n = max(1, int(sample_rate * ms / 1000.0))
    n = min(n, audio.size // 2)
    ramp = np.linspace(0.0, 1.0, n, dtype=np.float32)
    out = audio.copy()
    out[:n] *= ramp
    out[-n:] *= ramp[::-1]
    return out