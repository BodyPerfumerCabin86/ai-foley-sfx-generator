"""PluginRegistry — discovery, capability routing, hot-reload."""

from __future__ import annotations

import importlib
from pathlib import Path

from foley.contracts.manifest import PluginManifest
from foley.contracts.plugin import FoleyPlugin
from foley.core.loader import load_module_from_path
from foley.utils.logging import get_logger

_log = get_logger(__name__)

_DEFAULT_ROOT = Path(__file__).resolve().parent


class PluginRegistry:
    def __init__(self, plugin_root: Path | None = None) -> None:
        self._root = plugin_root or _DEFAULT_ROOT
        self._plugins: dict[str, FoleyPlugin] = {}
        self._manifests: dict[str, PluginManifest] = {}

    def discover(self) -> int:
        self._plugins.clear()
        self._manifests.clear()
        for pkg_dir in sorted(p for p in self._root.iterdir() if p.is_dir() and (p / "__init__.py").is_file()):
            try:
                manifest = PluginManifest.load(pkg_dir)
            except FileNotFoundError:
                _log.debug("no manifest.toml in %s, skipping", pkg_dir.name)
                continue
            plugin = load_module_from_path(f"foley.plugins.{pkg_dir.name}", pkg_dir)
            if plugin is None:
                continue
            self._plugins[plugin.plugin_id] = plugin
            self._manifests[plugin.plugin_id] = manifest
        return len(self._plugins)

    def plugins(self) -> list[FoleyPlugin]:
        return list(self._plugins.values())

    def get(self, plugin_id: str) -> FoleyPlugin | None:
        return self._plugins.get(plugin_id)

    def best_for(self, kind: str) -> str | None:
        for pid, plugin in self._plugins.items():
            if kind in plugin.capabilities:
                return pid
        return None

    def reload(self, plugin_id: str) -> bool:
        plugin = self._plugins.get(plugin_id)
        if plugin is None:
            return False
        pkg_dir = self._root / plugin_id
        plugin.teardown()
        importlib.invalidate_caches()
        fresh = load_module_from_path(f"foley.plugins.{plugin_id}", pkg_dir)
        if fresh is None:
            return False
        self._plugins[plugin_id] = fresh
        return True

    def reload_all(self) -> None:
        for pid in list(self._plugins):
            self.reload(pid)