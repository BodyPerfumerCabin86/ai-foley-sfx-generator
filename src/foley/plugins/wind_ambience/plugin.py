"""Wind ambience generator — filtered noise + gust envelope."""

from __future__ import annotations

import numpy as np
from scipy import signal

from foley.contracts.plugin import FoleyPlugin, RenderRequest, RenderResult


class WindAmbiencePlugin(FoleyPlugin):
    plugin_id = "wind_ambience"
    version = "0.3.1"
    capabilities = ("wind", "gust", "storm")

    def render(self, req: RenderRequest) -> RenderResult:
        rng = np.random.default_rng(req.seed)
        n = int(req.duration_s * req.sample_rate)
        white = rng.standard_normal(n).astype(np.float32)

        intensity = float(req.params.get("intensity", 0.5))
        cutoff = float(req.params.get("cutoff_hz", 900.0))
        sos = signal.butter(4, cutoff / (req.sample_rate / 2), btype="low", output="sos")
        body = signal.sosfilt(sos, white).astype(np.float32)

        # Slow gust envelope via smoothed noise.
        env = signal.sosfilt(signal.butter(2, 0.8 / (req.sample_rate / 2), output="sos"),
                             rng.standard_normal(n)).astype(np.float32)
        env = np.abs(env)
        env /= env.max() + 1e-9
        audio = (body * (0.3 + 0.7 * env) * intensity).astype(np.float32)
        peak = float(20 * np.log10(max(np.max(np.abs(audio)), 1e-9)))
        return RenderResult(audio=audio, sample_rate=req.sample_rate, plugin_id=self.plugin_id, peak_db=peak)