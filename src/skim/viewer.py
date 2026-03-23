import json
import re
import tempfile
import webbrowser
from pathlib import Path

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:wght@400;600&display=swap">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked@15.0.12/marked.min.js"></script>
<style>
  body {{
    max-width: 50rem;
    margin: 3rem auto;
    padding: 0 1.5rem;
    font-family: "Lora", "Georgia", serif;
    font-size: 1.16rem;
    line-height: 1.8;
    letter-spacing: 0.01em;
  }}
  pre {{ padding: 1rem; overflow-x: auto; border-radius: 4px; font-family: "SF Mono", "Fira Code", "Consolas", monospace; font-size: 0.9rem; line-height: 1.5; }}
  code {{ font-size: 0.85em; font-family: "SF Mono", "Fira Code", "Consolas", monospace; }}
  h1, h2, h3, strong {{ font-weight: 600; }}
  h1 {{ font-size: 2rem; margin-top: 2em; }}
  h2 {{ font-size: 1.6rem; margin-top: 1.8em; }}
  h3 {{ font-size: 1.35rem; margin-top: 1.5em; }}
  p, li {{ margin-bottom: 0.8em; }}
  .katex-display {{ overflow-x: auto; }}
  .theme-toggle {{
    position: fixed; top: 1rem; right: 1rem;
    background: none; border: 1px solid currentColor; border-radius: 4px;
    padding: 0.3rem 0.6rem; cursor: pointer; font-size: 1.1em;
    color: inherit; opacity: 0.6;
  }}
  .theme-toggle:hover {{ opacity: 1; }}
  body.dark {{ color: #e0e0e0; background: #1a1a2e; }}
  body.dark pre {{ background: #16213e; }}
  body.dark a {{ color: #6cb4ee; }}
  body.light {{ color: #1a1a1a; background: #fdfdfd; }}
  body.light pre {{ background: #f5f5f5; }}
</style>
</head>
<body>
<button class="theme-toggle" onclick="toggleTheme()" title="Toggle theme"></button>
<div id="content"></div>
<script>
  function setTheme(t) {{
    document.body.className = t;
    document.querySelector(".theme-toggle").textContent = t === "dark" ? "\u2600\ufe0f" : "\ud83c\udf19";
    localStorage.setItem("skim-theme", t);
  }}
  function toggleTheme() {{ setTheme(document.body.className === "dark" ? "light" : "dark"); }}
  setTheme(localStorage.getItem("skim-theme") || "dark");
</script>
<script>
  const md = {markdown_json};
  const mathBlocks = {math_blocks_json};

  let html = marked.parse(md);

  html = html.replace(/%%MATH(\d+)%%/g, (_, idx) => {{
    const b = mathBlocks[parseInt(idx)];
    try {{ return katex.renderToString(b.math.trim(), {{displayMode: b.display, throwOnError: false}}); }}
    catch(e) {{ return b.math; }}
  }});

  document.getElementById("content").innerHTML = html;
</script>
</body>
</html>
"""


def _sanitize(text: str) -> str:
    return text.encode("utf-8", errors="replace").decode("utf-8")


def _extract_math(content: str) -> tuple[str, list[dict]]:
    """Extract math delimiters before marked can mangle them."""
    blocks: list[dict] = []

    def stash(match_obj: re.Match, display: bool) -> str:
        blocks.append({"math": match_obj.group(1), "display": display})
        return f"%%MATH{len(blocks) - 1}%%"

    # Display math: \[...\] and $$...$$
    content = re.sub(r"\\\[([\s\S]*?)\\\]", lambda m: stash(m, True), content)
    content = re.sub(r"\$\$([\s\S]*?)\$\$", lambda m: stash(m, True), content)
    # Inline math: \(...\) and $...$
    content = re.sub(r"\\\((.+?)\\\)", lambda m: stash(m, False), content)
    content = re.sub(
        r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", lambda m: stash(m, False), content
    )

    # Escape bare & in math (KaTeX requires \&)
    for block in blocks:
        block["math"] = re.sub(r"(?<!\\)&", r"\\&", block["math"])

    return content, blocks


def open_in_browser(content: str, title: str = "skim") -> Path:
    content = _sanitize(content)
    processed, math_blocks = _extract_math(content)

    html = HTML_TEMPLATE.format(
        title=_sanitize(title),
        markdown_json=json.dumps(processed),
        math_blocks_json=json.dumps(math_blocks),
    )
    tmp = tempfile.NamedTemporaryFile(
        suffix=".html", prefix="skim_", delete=False, mode="wb"
    )
    tmp.write(html.encode("utf-8", errors="replace"))
    tmp.close()
    path = Path(tmp.name)
    webbrowser.open(path.as_uri())
    return path
