"""End-to-end render smoke test (no audio device required)."""

from __future__ import annotations

import json
from pathlib import Path

from foley.contracts.scene import SceneSpec
from foley.plugins.registry import PluginRegistry
from foley.services.render_pipeline import RenderPipeline


def test_render_scene_writes_stems_and_mix(tmp_path: Path) -> None:
    spec = {
        "title": "test_scene",
        "duration_s": 2.0,
        "layers": [
            {"name": "wind_take1", "