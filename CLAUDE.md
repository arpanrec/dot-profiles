# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Dependency management and builds use `uv` (backend `uv_build`, Python >=3.12, `src/` layout). The `Makefile` wraps these: `make setup`, `make build`, `make lint` (every CI check), `make fmt`, or a single linter such as `make mypy`.

```bash
uv sync                      # install deps + dev tools into .venv
uv run konsave -h            # run the CLI
uv run mypy $(git ls-files '*.py')
uv run pylint $(git ls-files '*.py')
uv run isort --check-only $(git ls-files '*.py')
uv run black --check $(git ls-files '*.py')
uv run ruff check $(git ls-files '*.py')
uv run pyright
npx --yes prettier --check .   # md/yaml/json/etc. (config: .prettierrc.mjs)
```

CI (`.github/workflows/lint.yml`) runs mypy, pylint, isort, black, ruff, pyright, yamllint and prettier. Line length is 120; mypy/pyright are strict, so all code needs full type hints. There is no test suite.

## Architecture

Konsave saves/applies desktop "profiles" (dotfile snapshots) from `~/.config/konsave/`. All code is in `src/konsave/`:

- `__main__.py` — argparse CLI (`main()` is the `konsave` script entry point). On first run it writes `CONF_KDE` (if `$XDG_CURRENT_DESKTOP == KDE`) or `CONF_OTHER` from `default_configs.py` to `~/.config/konsave/conf.yaml`, then dispatches to `funcs`.
- `consts.py` — path constants and **import-time side effects**: creates `~/.config/konsave/profiles` and snapshots `list_of_profiles` / `length_of_lop` once at import. These values are passed into `funcs` functions, so they go stale within a single process after a save/remove.
- `funcs.py` — profile operations (save, apply, remove, export, import, wipe) plus `read_konsave_config`, which loads `conf.yaml` and runs it through the `parse` module. Public functions are wrapped with `@exception_handler`.
- `parse.py` — expands placeholders in each entry's `location` in `conf.yaml`: keywords (`$HOME`, `$CONFIG_DIR`, `$SHARE_DIR`, `$BIN_DIR`) and functions (`${ENDS_WITH="x"}`, `${BEGINS_WITH="x"}`, which resolve a directory name by listing the parent directory). The token tables (`tokens`, `TOKEN_SYMBOL`) are imported by `funcs.py`.

Config model (`conf.yaml`): two top-level sections. `save` entries are backed up into a profile; `export` entries are only bundled into the exported `.knsv` archive (e.g. icon packs, themes) and are not saved in profiles. Each named entry has a `location` (parent directory) and `entries` (files/folders under it).

`__version__` in `src/konsave/__init__.py` is read from the installed package metadata, so the version is set only in `pyproject.toml`.
