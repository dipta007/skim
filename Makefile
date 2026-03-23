.PHONY: help install test test-claude test-all lint format clean hooks

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies and set up git hooks
	uv sync
	git config core.hooksPath .githooks

test: ## Run tests (excludes claude backend tests)
	uv run python -m pytest tests/ -v

test-claude: ## Run claude backend tests only
	uv run python -m pytest tests/ -v -m claude

test-all: ## Run all tests including claude backend
	uv run python -m pytest tests/ -v -m ""

lint: ## Check code style
	uv run ruff check src/ tests/

format: ## Auto-format code
	uv run ruff format src/ tests/

hooks: ## Set up git hooks (format on commit, test on push)
	git config core.hooksPath .githooks

clean: ## Remove build artifacts and caches
	rm -rf .venv dist build *.egg-info .pytest_cache .ruff_cache
