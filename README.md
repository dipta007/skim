# skim

Generate plain-language narratives and technical summaries from arxiv papers.

## Install

**With uv (recommended):**

```bash
uv tool install git+https://github.com/dipta007/skim
```

**With pipx:**

```bash
pipx install git+https://github.com/dipta007/skim
```

**With pip:**

```bash
pip install git+https://github.com/dipta007/skim
```

**From source:**

```bash
git clone https://github.com/dipta007/skim.git
cd skim
make install
```

## Setup

```bash
skim init
```

This walks you through picking a backend and creates a config at `~/.config/skim/config.toml`.

### Backends

**OpenAI** (or any OpenAI-compatible API): Requires an API key. Works with OpenAI, OpenRouter, Ollama, etc.

**Claude**: Uses your existing [Claude Code](https://claude.ai/code) subscription — no API key needed. Requires the `claude` CLI to be installed and logged in. Slower than the OpenAI backend (~30-60s per summary due to subprocess overhead) but free if you already have a Claude Pro/Max plan.

**As a Claude Code plugin:**

```
/plugin marketplace add dipta007/skim
/plugin install skim@dipta007-skim
```

Then use `/skim:story 2509.16538` or `/skim:deep 2509.16538` inside Claude Code.

## Usage

```bash
# Generate a plain-language narrative
skim -p 2509.16538 -t story

# Generate a technical summary
skim -p 2509.16538 -t deep

# Generate both
skim -p 2509.16538 -t all

# Use an arxiv URL
skim -p https://arxiv.org/abs/2509.16538 -t story

# Override output directory
skim -p 2509.16538 -t story --output-dir ./my-summaries/

# Jump to your output directory
cd $(skim cd)
```

## Summary Types

| Type | Description |
|------|-------------|
| `story` | A plain-language, analogy-driven narrative for anyone — no jargon, no equations |
| `deep` | A structured technical summary with methodology, results, and key contributions |

## Configuration

Config is stored at `~/.config/skim/config.toml`. Re-run `skim init` to update.

**OpenAI backend:**
```toml
[api]
backend = "openai"
key = "sk-your-key"
base_url = "https://api.openai.com/v1"
model = "gpt-5.4-nano"

[output]
dir = "~/papers/skim"
```

**Claude backend:**
```toml
[api]
backend = "claude"
key = ""
base_url = ""
model = "sonnet"

[output]
dir = "~/papers/skim"
```

## Development

```bash
git clone https://github.com/dipta007/skim.git
cd skim
make install    # Install dependencies + set up git hooks
make test       # Run tests
make lint       # Check code style
make format     # Auto-format code
```

`make install` also configures git hooks that run the formatter/linter on commit and tests on push.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, code style, and PR guidelines.

## License

MIT
