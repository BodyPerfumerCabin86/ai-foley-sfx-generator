"""manifest.toml schema for extension modules."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PluginManifest:
    name: str
    version: str
    api: str
    capabilities: tuple[str, ...]
    entry: str = "plugin.py"

    @classmethod
    def load(cls, pkg_dir: Path) -> "PluginManifest":
        data = tomllib.loads((pkg_dir / "manifest.toml").read_text("utf-8"))
        return cls(
            name=data["name"],
            version=data["version"],
            api=data["api"],
            capabilities=tuple(data.get("capabilities", [])),
            entry=data.get("entry", "plugin.py"),
        )