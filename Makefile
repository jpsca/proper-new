.PHONY: install
install:
	uv sync --group dev --group test

.PHONY: test
test:
	uv run pytest -x tests.py

.PHONY: lint
lint:
	uv run ruff check proper_new.py tests.py
	uv run ty check

.PHONY: lintfix
lintfix:
	uv run ruff check proper_new.py tests.py --fix
