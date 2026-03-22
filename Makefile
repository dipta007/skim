.PHONY: install test lint format clean

install:
	uv sync

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/

clean:
	rm -rf .venv dist build *.egg-info .pytest_cache .ruff_cache
