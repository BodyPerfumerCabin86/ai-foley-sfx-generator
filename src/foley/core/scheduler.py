"""RenderScheduler — picks plugins, runs the render graph, writes output.

A scene spec maps to one or more *layers* (foley events). Each layer is
routed to the plugin whose `capabilities` best match the layer's `kind`.
"""

from __future__ import annotations

from pathlib import Path

from foley.contracts.scene import SceneSpec
from foley.plugins.registry import PluginRegistry
from foley.services.render_pipeline import RenderPipeline
from foley.utils.logging import get_logger

_log = get_logger(__name__)


class RenderScheduler:
    def __init__(self, registry: PluginRegistry) -> None:
        self._registry = registry

    def render(self, scene_path: str, out_dir: Path, force_plugin: str | None) -> int:
        scene_file = Path(scene_path)
        if not scene_file.is_file():
            _log.error("scene spec not found: %s", scene_file)
            return 2

        scene = SceneSpec.from_file(scene_file)
        pipeline = RenderPipeline(self._registry, out_dir=out_dir)
        rendered = pipeline.run(scene, force_plugin=force_plugin)
        _log.info("wrote %d stem(s) to %s", rendered, out_dir)
        return 0

    def _route(self, kind: str) -> str | None:
        return self._registry.best_for(kind)

    def route_all(self, scene: SceneSpec) -> dict[str, str | None]:
        return {layer.name: self._route(layer.kind) for layer in scene.layers}