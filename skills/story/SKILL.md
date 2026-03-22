---
name: story
description: "Generate a plain-language, analogy-driven narrative summary of an arxiv paper. Use when the user wants a simple, jargon-free explanation of a paper. Usage: /skim:story <arxiv-id-or-url>"
---

Generate a plain-language story summary of the arxiv paper `$ARGUMENTS`.

## Steps

1. Download the paper PDF:

```bash
curl -L -o /tmp/skim_paper.pdf "https://arxiv.org/pdf/$ARGUMENTS"
```

If `$ARGUMENTS` is a full URL, extract the arxiv ID first (the `DDDD.DDDDD` part).

2. Read the prompt instructions from `${CLAUDE_SKILL_DIR}/../../src/skim/prompts/story.md`

3. Read the downloaded PDF using the Read tool at `/tmp/skim_paper.pdf`

4. Follow the prompt instructions to generate the summary. Output ONLY the summary markdown.

5. Clean up: `rm /tmp/skim_paper.pdf`
