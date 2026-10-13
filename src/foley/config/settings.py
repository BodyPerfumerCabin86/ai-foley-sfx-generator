"""Settings — pydantic model for host config (foley.toml / env)."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class AudioSettings(BaseModel):
    sample_rate: int = 48000
    channels: int = 1
    bit_depth: int = 24


class PathSettings(BaseModel):
    renders_root: Path = Field(default=Path("scenes/renders"))
    plugin_root: Path | None = None


class Settings(BaseModel):
    audio: AudioSettings = AudioSettings()
    paths: PathSettings = PathSettings()
    sandbox_plugins: bool = False

    def resolves_inside_renders(self, candidate: Path) -> bool:
        try:
            candidate.resolve().relative_to(self.paths.renders_root.resolve())
            return True
        except ValueError:
            return False