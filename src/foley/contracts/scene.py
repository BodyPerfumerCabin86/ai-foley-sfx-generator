"""SceneSpec — declarative description of a foley render.

A scene is a list of layers. Each layer names a `kind` (which the
registry routes to a plugin) and carries params (distance, wetness,
material, intensity, ...).
"""

from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Layer:
    name: str
    kind: str
    at_s: float
    params: dict[str, float | str | bool]


@dataclass(frozen=True)
class SceneSpec:
    title: str
    duration_s: float
    layers: list[Layer]

    @classmethod
    def from_file(cls, path: Path) -> "SceneSpec":
        raw = path.read_bytes()
        data = tomllib.loads(raw.decode("utf-8")) if path.suffix == ".toml" else json.loads(raw)
        layers = [
            Layer(
                name=l["name"],
                kind=l["kind"],
                at_s=float(l.get("at_s", 0.0)),
                params=dict(l.get("params", {})),
            )
            for l in data["layers"]
        ]
        return cls(title=data.get("title", path.stem), duration_s=float(data.get("duration_s", 10.0)), layers=layers)