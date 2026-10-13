# Contributing to ai-foley-sfx-generator

Thanks for wanting to make movie-grade foley on a laptop. This repo is a
Windows-first desktop tool that takes a scene description or a silent video
track and synthesizes cinematic sound effects with a diffusion + DSP hybrid
pipeline. Contributions of new extension modules are the most valuable thing
you can send.

## Ground rules

- Python 3.11+ on Windows 10/11 (x64). Linux/macOS work for the host, but
  the shipped audio drivers target Windows WASAPI.
- Every new SFX generator ships as an **extension module** under
  `src/foley/plugins/`. Do not bolt features into the host. If you need host
  changes, open an RFC issue first.
- Shared contracts live in `src/foley/contracts/`. Breaking a contract means a
  major version bump and a migration note.
- Keep the host dependency-light. Heavy audio/ML deps belong in the plugin's
  own `requirements-<plugin>.txt`.

## Dev setup

```
git clone https://github.com/<org>/ai-foley-sfx-generator
cd ai-foley-sfx-generator
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m foley.cli doctor
```

`doctor` verifies the audio backend, CUDA/Metal availability, and that the
plugin registry resolves. If it passes, you're ready.

## Adding an extension module

1. Create `src/foley/plugins/<your_plugin>/__init__.py`.
2. Subclass `FoleyPlugin` from `foley.contracts.plugin`.
3. Declare `manifest.toml` with `name`, `version`, `api`, `capabilities`.
4. Register your renderer entrypoint with the `@register` decorator.
5. Add a test under `tests/`.
6. Run `python -m foley.cli plugins list` — your module must appear.

## Code style

- `ruff` for lint, `black` for format, `mypy --strict` on `src/foley/contracts/`.
- Type hints required on all public functions.
- No global mutable state in extension modules. The host may load/unload
  modules at runtime; assume you can be reloaded.
- Log via `foley.utils.logging.get_logger(__name__)`, never `print`.

## Commits & PRs

- Conventional commits: `feat(plugin/wind): add gust layering`.
- One plugin per PR. Host changes get their own PR with a linked RFC.
- Attach a short A/B render (`.wav` before/after) for anything that changes
  audio output. Maintainers can't review what they can't hear.

## Reporting audio quality regressions

Include: scene spec used, plugin versions, host commit, GPU/CPU, and the
reference render hash if you have one. Reproducibility is what makes a bug
report actionable.