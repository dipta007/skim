# skim

Generate plain-language narratives and technical summaries from arxiv papers.

## Three Ways to Use skim

| #   | Method                                                 | Best for                                                                          | API key needed? | Cached? |
| --- | ------------------------------------------------------ | --------------------------------------------------------------------------------- | --------------- | ------- |
| 1   | [**CLI + OpenAI**](#option-1-cli--openai)              | Regular use, any OpenAI-compatible API (OpenAI, OpenRouter, Ollama, local models) | Yes             | Yes     |
| 2   | [**CLI + Claude**](#option-2-cli--claude)              | Already have a Claude Code subscription, don't want another API key               | No              | Yes     |
| 3   | [**Claude Code Plugin**](#option-3-claude-code-plugin) | Already inside Claude Code, want one-command summaries                            | No              | No      |

---

### Option 1: CLI + OpenAI

Install once, use anywhere from your terminal. Works with any OpenAI-compatible API — OpenAI, OpenRouter, Ollama, or any local model server.

```bash
uv tool install git+https://github.com/dipta007/skim    # or pipx, or pip, see the Install section below
skim init                                               # select "openai", enter API key
skim -p 2509.16538 -t story                             # generate summary
```

### Option 2: CLI + Claude

Same CLI, but uses your existing Claude Code subscription — no API key needed. Requires the `claude` CLI to be installed and logged in.

```bash
uv tool install git+https://github.com/dipta007/skim    # or pipx, or pip, see the Install section below
skim init                                               # select "claude"
skim -p 2509.16538 -t story                             # generate summary
```

### Option 3: Claude Code Plugin

Already inside Claude Code? Install the plugin and use slash commands — no setup, no API key.

```
/plugin marketplace add dipta007/skim
/plugin install skim@dipta007-skim
```

Then, inside your claude-code:

```
/story 2509.16538
/deep 2509.16538
```

Claude reads the paper and generates the summary directly.

---

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
