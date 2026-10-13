"""Allow `python -m foley` to bootstrap the desktop tool."""

from foley.cli import main

if __name__ == "__main__":
    raise SystemExit(main())