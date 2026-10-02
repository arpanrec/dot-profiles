# AGENTS.md

This file gives AI coding agents the guidance they need to work in this repository.

## Commands

Dependency management and builds use `uv` (backend `uv_build`, Python >=3.12, `src/` layout). There is no test suite.

```bash
uv sync                  # install deps + dev tools into .venv
uv run dpf -h            # run the CLI
uv build                 # build sdist and wheel
```

CI (`.github/workflows/lint.yml`) runs mypy, pylint, isort, black, ruff, pyright, yamllint and prettier. Line length is 120; mypy/pyright are strict, so all code needs full type hints.

## Architecture

dot-profiles saves/applies desktop "profiles" (dotfile snapshots) from `~/.config/dot-profiles/`. All code is in `src/dot_profiles/`:

- `__main__.py` — argparse CLI (`main()` is the `dpf` script entry point). On first run it writes `CONF_KDE` (if `$XDG_CURRENT_DESKTOP == KDE`) or `CONF_OTHER` from `default_configs.py` to `~/.config/dot-profiles/conf.yaml`, then dispatches to `funcs`.
- `consts.py` — path constants and **import-time side effects**: creates `~/.config/dot-profiles/profiles` and snapshots `list_of_profiles` / `length_of_lop` once at import. These values are passed into `funcs` functions, so they go stale within a single process after a save/remove.
- `funcs.py` — profile operations (save, apply, remove, export, import, wipe) plus `read_config`, which loads `conf.yaml` and runs it through the `parse` module. Public functions are wrapped with `@exception_handler`.
- `parse.py` — expands placeholders in each entry's `location` in `conf.yaml`: keywords (`$HOME`, `$CONFIG_DIR`, `$SHARE_DIR`, `$BIN_DIR`, `$DOT_PROFILES_DIR`, `$PROFILES_DIR`) and functions (`${ENDS_WITH="x"}`, `${BEGINS_WITH="x"}`, which resolve a directory name by listing the parent directory). The token tables (`tokens`, `TOKEN_SYMBOL`) are imported by `funcs.py`.

Config model (`conf.yaml`): two top-level sections. `save` entries are backed up into a profile; `export` entries are only bundled into the exported `.dpf` archive (e.g. icon packs, themes) and are not saved in profiles. Each named entry has a `location` (parent directory) and `entries` (files/folders under it).

`__version__` in `src/dot_profiles/__init__.py` is read from the installed package metadata, so the version is set only in `pyproject.toml` (semantic-release bumps it on release).
