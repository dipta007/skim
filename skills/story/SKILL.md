---
name: story
description: Generate a plain-language, analogy-driven narrative summary of an arxiv paper. Use when the user wants a simple, jargon-free explanation of a paper.
argument-hint: <arxiv-id-or-url>
allowed-tools:
  - Bash
---

Summarize the arxiv paper `$ARGUMENTS` as a plain-language story.

First, check if `skim` is installed:

```bash
which skim
```

If not installed, install it:

```bash
uv tool install git+https://github.com/dipta007/skim
```

If `uv` is not available, try:

```bash
pipx install git+https://github.com/dipta007/skim
```

Then check if skim is configured:

```bash
skim cd
```

If it shows "Not configured", tell the user to run `skim init` in their terminal to set up their API key and output directory, then try again.

Once ready, run:

```bash
skim -p $ARGUMENTS -t story
```

Display the generated summary to the user.
