# skim

Generate plain-language narratives and technical summaries from arxiv papers.

## Install

```bash
uv tool install git+https://github.com/dipta007/skim
```

Or clone and install locally:

```bash
git clone https://github.com/dipta007/skim.git
cd skim
uv sync
```

## Setup

Run the interactive setup to configure your API key and output directory:

```bash
skim init
```

This creates a config file at `~/.config/skim/config.toml`.

## Usage

```bash
# Generate a plain-language narrative
skim -p 2603.10165 -t story

# Generate a technical summary
skim -p 2603.10165 -t deep

# Generate both
skim -p 2603.10165 -t all

# Use an arxiv URL
skim -p https://arxiv.org/abs/2603.10165 -t story

# Override output directory
skim -p 2603.10165 -t story --output-dir ./my-summaries/
```

## Summary Types

| Type | Description |
|------|-------------|
| `story` | A plain-language, analogy-driven narrative for anyone — no jargon, no equations |
| `deep` | A structured technical summary with methodology, results, and key contributions |

## Configuration

Config is stored at `~/.config/skim/config.toml`:

```toml
[api]
key = "sk-your-key"
base_url = "https://api.openai.com/v1"
model = "gpt-5.4-nano"

[output]
dir = "~/papers/skim"
```

Re-run `skim init` to update settings.

## Development

```bash
git clone https://github.com/dipta007/skim.git
cd skim
make install    # Install dependencies
make test       # Run tests
make lint       # Check code style
make format     # Auto-format code
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, code style, and PR guidelines.

## License

MIT
