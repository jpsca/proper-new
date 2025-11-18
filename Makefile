.PHONY: install
install:
	uv sync --group dev --group test

.PHONY: test
test:
	pytest -x tests.py

.PHONY: lint
lint:
	ruff check src tests.py
	ty check

.PHONY: lintfix
lintfix:
	ruff check src tests.py --fix
