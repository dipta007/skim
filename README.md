# skim

Generate plain-language narratives and technical summaries from arxiv papers.

## Three Ways to Use skim

| Method                                                 | Best for                                                                          | API key needed? |
| ------------------------------------------------------ | --------------------------------------------------------------------------------- | --------------- |
| [**CLI + OpenAI**](#option-1-cli-tool)                 | Regular use, any OpenAI-compatible API (OpenAI, OpenRouter, Ollama, local models) | Yes             |
| [**CLI + Claude**](#option-1-cli-tool)                 | Already have a Claude Code subscription, don't want another API key               | No              |
| [**Claude Code Plugin**](#option-2-claude-code-plugin) | Already inside Claude Code, want one-command summaries                            | No              |

---

### Option 1: CLI Tool

Install once, use anywhere from your terminal.

```bash
uv tool install git+https://github.com/dipta007/skim   # or pipx, or pip
skim init                                                # pick backend + configure
skim -p 2509.16538 -t story                              # generate summary
```

During `skim init`, choose your backend:

- **openai** — works with OpenAI, OpenRouter, Ollama, or any service that speaks the OpenAI API
- **claude** — uses your Claude Code subscription via `claude -p` subprocess (no API key, but slightly slower)

### Option 2: Claude Code Plugin

If you're already in Claude Code, install the plugin and use slash commands — no setup, no API key.

```
/plugin marketplace add dipta007/skim
/plugin install skim@dipta007-skim
```

Then:

```
/skim:story 2509.16538
/skim:deep 2509.16538
```

Claude reads the paper and generates the summary directly.

---

## Usage (CLI)

```bash
skim -p 2509.16538 -t story                        # plain-language narrative
skim -p 2509.16538 -t deep                         # technical summary
skim -p 2509.16538 -t all                          # both
skim -p https://arxiv.org/abs/2509.16538 -t story  # works with URLs too
skim -p 2509.16538 -t story --output-dir ./custom/ # custom output dir
cd $(skim cd)                                      # jump to output directory
```

## Summary Types

| Type    | What you get                                                                    |
| ------- | ------------------------------------------------------------------------------- |
| `story` | A plain-language, analogy-driven narrative — no jargon, no equations            |
| `deep`  | A structured technical summary with methodology, results, and key contributions |

## Configuration

Config lives at `~/.config/skim/config.toml`. Re-run `skim init` to change settings.

<details>
<summary>Example configs</summary>

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

</details>

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
