"""FoleyPlugin — the extension contract.

Every SFX generator (wind, footsteps, weapon, ambience, ...) implements
this. The host only ever talks to plugins through this surface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True)
class RenderRequest:
    kind: str
    duration_s: float
    sample_rate: int = 48000
    seed: int | None = None
    params: dict[str, float | str | bool] = field(default_factory=dict)


@dataclass(frozen=True)
class RenderResult:
    audio: np.ndarray          # shape (n_samples,) float32, mono
    sample_rate: int
    plugin_id: str
    peak_db: float = 0.0


class FoleyPlugin(ABC):
    """Base class for extension modules.

    Contract:
      - `plugin_id` + `version` are stable identifiers (registry keys on them).
      - `capabilities` lists the scene `kind`s this plugin can render.
      - `render` is pure: same request + seed -> same audio bytes.
      - Plugins must be reloadable: no module-level mutable state.
    """

    plugin_id: str = "unnamed"
    version: str = "0.0.0"
    capabilities: tuple[str, ...] = ()

    @abstractmethod
    def render(self, req: RenderRequest) -> RenderResult: ...

    def warmup(self) -> None:
        """Optional: preload model weights / impulse responses."""
        return None

    def teardown(self) -> None:
        """Optional: release GPU memory on unload/reload."""
        return None