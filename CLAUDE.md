# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
make install     # Install deps + set up git hooks
make test        # Run all tests
make lint        # Ruff check
make format      # Ruff format
uv run pytest tests/test_cache.py::test_get_cached_miss -v  # Single test
uv run skim --help   # Test CLI locally (picks up source changes immediately)
```

Git hooks (`.githooks/`): pre-commit runs ruff format+check, pre-push runs pytest. Set up automatically by `make install`.

## Architecture

**CLI tool** that takes arxiv paper IDs, downloads PDFs, sends them to an LLM, and generates summaries in two flavors: `story` (layperson narrative) and `deep` (technical summary).

### Data flow

```
arxiv ID → arxiv.py (download PDF) → llm.py (send PDF + prompt to OpenAI) → cache.py (save) → cli.py (render with rich)
```

### Key design decisions

- **Prompts are bundled in the package** at `src/skim/prompts/` and loaded via `importlib.resources` — not from the filesystem. This is what makes `uv tool install git+...` work.
- **Cache invalidation uses prompt hashes.** Cache filenames include the first 8 chars of the prompt's SHA-256: `{arxiv_id}_{type}_{hash}.md`. Changing a prompt automatically invalidates all cached results for that type.
- **Config lives at `~/.config/skim/config.toml`** (respects `$XDG_CONFIG_HOME`). No `.env` files. The `Config` dataclass has: `api_key`, `base_url`, `model`, `output_dir`.
- **PDF is sent as base64 file content block** to the OpenAI chat completions API (not extracted text). The `"type": "file"` message format is used.
- **Two summary types** map to prompt files: `story` → `story.md`, `deep` → `deep.md`. The mapping is `PROMPT_MAP` in `llm.py`.
- **`cli.py` uses argparse with subparsers** for `init` and `cd`, plus top-level flags `-p`/`-t`/`--output-dir` for the main summarize flow.
- **LaTeX → Unicode conversion** (`latex.py`) is applied only for terminal display, not saved files. Uses negative lookahead patterns for short commands (`\in`, `\pi`) to avoid prefix corruption.

### Module dependency graph

```
cli.py → init_cmd.py → config.py
cli.py → llm.py → config.py
cli.py → arxiv.py
cli.py → cache.py
cli.py → latex.py
```

`arxiv.py`, `cache.py`, and `latex.py` are standalone — no internal imports.
