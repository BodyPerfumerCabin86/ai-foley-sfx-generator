"""Footsteps generator — impulse-train through a material filter."""

from __future__ import annotations

import numpy as np
from scipy import signal

from foley.contracts.plugin import FoleyPlugin, RenderRequest, RenderResult

_MATERIAL_CUTOFF = {"gravel": 4200.0, "wood": 1800.0, "carpet": 700.0, "metal": 6000.0}


class FootstepsPlugin(FoleyPlugin):
    plugin_id = "footsteps"
    version = "0.2.0"
    capabilities = ("footstep", "walk", "run")

    def render(self, req: RenderRequest) -> RenderResult:
        rng = np.random.default_rng(req.seed)
        n = int(req.duration_s * req.sample_rate)
        audio = np.zeros(n, dtype=np.float32)

        stride = float(req.params.get("stride_s", 0.48))
        material = str(req.params.get("material", "gravel"))
        cutoff = _MATERIAL_CUTOFF.get(material, 2500.0)

        sos = signal.butter(2, cutoff / (req.sample_rate / 2), btype="low", output="sos")
        t = 0.0
        while t < req.duration_s:
            i0 = int(t * req.sample_rate)
            burst = rng.standard_normal(int(0.06 * req.sample_rate)).astype(np.float32)
            burst *= np.exp(-np.linspace(0, 8, burst.size)).astype(np.float32)
            burst = signal.sosfilt(sos, burst).astype(np.float32)
            end = min(i0 + burst.size, n)
            audio[i0:end] += burst[: end - i0]
            t += stride

        peak = float(20 * np.log10(max(np.max(np.abs(audio)), 1e-9)))
        return RenderResult(audio=audio, sample_rate=req.sample_rate, plugin_id=self.plugin_id, peak_db=peak)