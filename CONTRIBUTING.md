# Contributing to skim

## Development Setup

```bash
git clone https://github.com/dipta007/skim.git
cd skim
make install
```

## Running Tests

```bash
make test
```

## Code Style

We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
make lint       # Check for issues
make format     # Auto-format
```

## Pull Requests

1. Fork the repo and create a branch from `main`.
2. Add tests for any new functionality.
3. Ensure all tests pass (`make test`).
4. Ensure code passes lint (`make lint`).
5. Open a PR with a clear description of the change.

## AI-Generated Code

We welcome contributions that use AI tools (Copilot, Claude, ChatGPT, etc.) to assist with development. However, all contributors must:

- **Review and understand** every line of AI-generated code before submitting
- **Test** that the code works as intended
- **Take responsibility** for the code they submit, regardless of how it was generated

AI-assisted code that passes review and tests is treated the same as manually written code.
