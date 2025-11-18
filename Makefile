.PHONY: install
install:
	uv sync --group dev --group test

.PHONY: test
test:
	uv run pytest -x tests.py

.PHONY: lint
lint:
	uv run ruff check src tests.py
	uv run ty check

.PHONY: lintfix
lintfix:
	uv run ruff check src tests.py --fix
