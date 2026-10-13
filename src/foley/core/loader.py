"""Dynamic loader for extension modules.

Modules are plain Python packages under `foley/plugins/*/`. The loader
imports them, validates their manifest, and hands them to the registry.
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path

from foley.contracts.plugin import FoleyPlugin
from foley.utils.logging import get_logger

_log = get_logger(__name__)


def load_module_from_path(pkg_name: str, pkg_dir: Path) -> FoleyPlugin | None:
    """Import `pkg_dir` as `pkg_name` and return the single FoleyPlugin it exposes."""
    init = pkg_dir / "__init__.py"
    if not init.is_file():
        return None
    spec = importlib.util.spec_from_file_location(pkg_name, init)
    if spec is None or spec.loader is None:
        _log.warning("could not build import spec for %s", pkg_name)
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[pkg_name] = module
    spec.loader.exec_module(module)

    candidates = [v for v in vars(module).values() if isinstance(v, type) and issubclass(v, FoleyPlugin) and v is not FoleyPlugin]
    if not candidates:
        _log.warning("plugin package %s exposes no FoleyPlugin subclass", pkg_name)
        return None
    if len(candidates) > 1:
        _log.warning("plugin package %s exposes %d classes; using the first", pkg_name, len(candidates))
    return candidates[0]()