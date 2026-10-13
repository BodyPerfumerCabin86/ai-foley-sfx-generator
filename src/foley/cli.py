"""Command-line entrypoint for the AI foley host.

Subcommands:
    doctor            verify audio + plugin environment
    render            synthesize SFX for a scene spec
    plugins list      enumerate discovered extension modules
    plugins reload    hot-reload a module without restarting the host
"""

from __future__ import annotations

import argparse
import sys

from rich.console import Console

from foley import __version__
from foley.core.host import FoleyHost
from foley.utils.logging import configure_logging, get_logger

_console = Console()
_log = get_logger(__name__)


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="foley", description="AI foley / cinematic SFX generator")
    p.add_argument("--version", action="version", version=f"ai-foley-sfx-generator {__version__}")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("doctor", help="verify environment")

    r = sub.add_parser("render", help="render SFX from a scene spec")
    r.add_argument("scene", help="path to scene spec (json/toml)")
    r.add_argument("-o", "--out", default="scenes/renders", help="output dir")
    r.add_argument("--plugin", default=None, help="force a specific plugin id")

    pl = sub.add_parser("plugins", help="manage extension modules")
    pl.add_argument("action", choices=["list", "reload"])
    pl.add_argument("name", nargs="?", default=None)

    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    configure_logging(verbose=args.verbose)
    host = FoleyHost()

    if args.cmd == "doctor":
        return host.doctor()
    if args.cmd == "render":
        return host.render_scene(args.scene, out_dir=args.out, force_plugin=args.plugin)
    if args.cmd == "plugins":
        if args.action == "list":
            return host.list_plugins()
        if args.action == "reload":
            return host.reload_plugin(args.name) if args.name else 2
    _console.print("[red]unknown command[/]")
    return 2


if __name__ == "__main__":
    sys.exit(main())