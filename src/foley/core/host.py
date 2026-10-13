"""FoleyHost — the top-level orchestrator.

Owns the plugin registry, the render scheduler, and the device layer.
This is the only object the CLI talks to directly.
"""

from __future__ import annotations

from pathlib import Path

from foley.contracts.plugin import FoleyPlugin
from foley.core.scheduler import RenderScheduler
from foley.plugins.registry import PluginRegistry
from foley.services.audio_device import AudioDeviceService
from foley.utils.logging import get_logger

_log = get_logger(__name__)


class FoleyHost:
    """Plugin host for the AI foley tool.

    Lifecycle: discover -> validate -> register -> (render | reload).
    Hot-reload is coordinated by the scheduler so a reload never lands
    mid-render.
    """

    def __init__(self, plugin_root: Path | None = None) -> None:
        self._registry = PluginRegistry(plugin_root=plugin_root)
        self._device = AudioDeviceService()
        self._scheduler = RenderScheduler(self._registry)
        self._registry.discover()

    def doctor(self) -> int:
        ok = True
        if not self._device.has_output_device():
            _log.error("no output audio device detected")
            ok = False
        n = len(self._registry.plugins())
        _log.info("registered %d extension module(s)", n)
        if n == 0:
            _log.warning("no plugins found under src/foley/plugins/")
        return 0 if ok else 1

    def list_plugins(self) -> int:
        for p in self._registry.plugins():
            _log.info("%s v%s  caps=%s", p.plugin_id, p.version, ",".join(p.capabilities))
        return 0

    def reload_plugin(self, name: str | None) -> int:
        if name is None:
            self._registry.reload_all()
            return 0
        return 0 if self._registry.reload(name) else 1

    def render_scene(self, scene_path: str, out_dir: str, force_plugin: str | None) -> int:
        return self._scheduler.render(scene_path, out_dir=Path(out_dir), force_plugin=force_plugin)

    def plugin(self, plugin_id: str) -> FoleyPlugin | None:
        return self._registry.get(plugin_id)