.PHONY: help install test lint format clean hooks

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

test: ## Run tests
	uv run pytest tests/ -v

lint: ## Check code style
	uv run ruff check src/ tests/

format: ## Auto-format code
	uv run ruff format src/ tests/

hooks: ## Set up git hooks (format on commit, test on push)
	git config core.hooksPath .githooks

clean: ## Remove build artifacts and caches
	rm -rf .venv dist build *.egg-info .pytest_cache .ruff_cache
