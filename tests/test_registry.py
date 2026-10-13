"""Registry discovery + routing tests."""

from __future__ import annotations

from foley.plugins.registry import PluginRegistry


def test_discovers_shipped_plugins() -> None:
    reg = PluginRegistry()
    n = reg.discover()
    assert n >= 2
    ids = {p.plugin_id for p in reg.plugins()}
    assert {"wind_ambience", "footsteps"} <= ids


def test_best_for_routes_by_capability() -> None:
    reg = PluginRegistry()
    reg.discover()
    assert reg.best_for("storm") == "wind_ambience"
    assert reg.best_for("metal") is None or reg.best_for("footstep") == "footsteps"


def test_reload_returns_false_for_unknown() -> None:
    reg = PluginRegistry()
    reg.discover()
    assert reg.reload("does_not_exist") is False