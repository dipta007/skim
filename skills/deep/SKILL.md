---
name: deep
description: Generate a structured technical summary of an arxiv paper with methodology, results, and key contributions. Use when the user wants a detailed technical breakdown.
argument-hint: <arxiv-id-or-url>
allowed-tools:
  - Bash
---

Summarize the arxiv paper `$ARGUMENTS` as a deep technical summary.

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
skim -p $ARGUMENTS -t deep
```

Display the generated summary to the user.
