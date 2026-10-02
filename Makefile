.PHONY: help all setup build lint fmt mypy pylint isort black ruff pyright yamllint prettier clean distclean maintclean

PY_FILES = $$(git ls-files '*.py')
YAML_FILES = $$(git ls-files '*.yaml' '*.yml' '.yamllint')

all: setup

help:
	@echo "konsave helper:"
	@echo ""
	@echo " - setup:        Install dependencies and dev tools with uv"
	@echo " - build:        Build sdist and wheel with uv"
	@echo " - lint:         Run all linters (same checks as CI)"
	@echo " - fmt:          Apply isort, black, ruff fixes and prettier"
	@echo " - mypy:         Run mypy"
	@echo " - pylint:       Run pylint"
	@echo " - isort:        Check import order"
	@echo " - black:        Check formatting"
	@echo " - ruff:         Run ruff check"
	@echo " - pyright:      Run pyright"
	@echo " - yamllint:     Run yamllint"
	@echo " - prettier:     Check prettier formatting"
	@echo " - clean:        Remove all pyc files"
	@echo " - distclean:    Remove any eggs/builds"
	@echo " - maintclean:   Remove virtual env and dist files"
	@echo ""

setup:
	@echo "Setting up"
	@uv sync --all-extras --all-packages

build:
	@echo " * Building"
	@uv build

lint: mypy pylint isort black ruff pyright yamllint prettier

fmt:
	@echo " * Running isort"
	@uv run isort $(PY_FILES)
	@echo " * Running black"
	@uv run black $(PY_FILES)
	@echo " * Running ruff --fix"
	@uv run ruff check --fix $(PY_FILES)
	@echo " * Running prettier"
	@npx --yes prettier --write .

mypy:
	@echo " * Running mypy"
	@uv run mypy $(PY_FILES)

pylint:
	@echo " * Running pylint"
	@uv run pylint $(PY_FILES)

isort:
	@echo " * Running isort"
	@uv run isort --check-only $(PY_FILES)

black:
	@echo " * Running black"
	@uv run black --check $(PY_FILES)

ruff:
	@echo " * Running ruff"
	@uv run ruff check $(PY_FILES)

pyright:
	@echo " * Running pyright"
	@uv run pyright

yamllint:
	@echo " * Running yamllint"
	@uv run yamllint $(YAML_FILES)

prettier:
	@echo " * Running prettier"
	@npx --yes prettier --check .

clean:
	@find . -path ./.venv -prune -o -name "*.pyc" -exec rm -f {} \;
	@find . -path ./.venv -prune -o -name '__pycache__' -type d -exec rm -fr {} +

distclean: clean
	rm -fr *.egg *.egg-info/ .eggs/ dist/ build/

maintclean: distclean
	rm -fr .venv/
