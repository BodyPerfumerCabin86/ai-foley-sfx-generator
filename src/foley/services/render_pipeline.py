"""RenderPipeline — routes scene layers to plugins, mixes, writes stems."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf

from foley.contracts.plugin import RenderRequest
from foley.contracts.scene import SceneSpec
from foley.plugins.registry import PluginRegistry
from foley.utils.logging import get_logger

_log = get_logger(__name__)


class RenderPipeline:
    def __init__(self, registry: PluginRegistry, out_dir: Path) -> None:
        self._registry = registry
        self._out = out_dir
        self._out.mkdir(parents=True, exist_ok=True)

    def run(self, scene: SceneSpec, force_plugin: str | None = None) -> int:
        written = 0
        bus_rate = 48000
        bus = np.zeros(int(scene.duration_s * bus_rate), dtype=np.float32)

        for layer in scene.layers:
            pid = force_plugin or self._registry.best_for(layer.kind)
            if pid is None:
                _log.warning("no plugin for kind=%s (layer %s)", layer.kind, layer.name)
                continue
            plugin = self._registry.get(pid)
            if plugin is None:
                continue
            req = RenderRequest(kind=layer.kind, duration_s=scene.duration_s,
                                sample_rate=bus_rate, seed=abs(hash(layer.name)) % (2**31), params=layer.params)
            res = plugin.render(req)
            start = int(layer.at_s * bus_rate)
            end = min(start + res.audio.size, bus.size)
            bus[start:end] += res.audio[: end - start]

            stem = self._out / f"{layer.name}_{pid}.wav"
            sf.write(stem, res.audio, res.sample_rate)
            written += 1

        sf.write(self._out / f"{scene.title}_mix.wav", bus, bus_rate)
        return written