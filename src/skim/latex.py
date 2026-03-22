import re

LATEX_REPLACEMENTS = [
    # Multi-char commands first (longer matches before shorter to avoid prefix conflicts)
    (r"\\rightarrow", "→"),
    (r"\\leftarrow", "←"),
    (r"\\infty", "∞"),
    (r"\\epsilon", "ε"),
    (r"\\lambda", "λ"),
    (r"\\partial", "∂"),
    (r"\\approx", "≈"),
    (r"\\subset", "⊂"),
    (r"\\forall", "∀"),
    (r"\\exists", "∃"),
    (r"\\notin", "∉"),
    (r"\\times", "×"),
    (r"\\alpha", "α"),
    (r"\\beta", "β"),
    (r"\\gamma", "γ"),
    (r"\\delta", "δ"),
    (r"\\theta", "θ"),
    (r"\\sigma", "σ"),
    (r"\\omega", "ω"),
    (r"\\nabla", "∇"),
    (r"\\sqrt", "√"),
    (r"\\prod(?![a-z])", "∏"),
    (r"\\sum(?![a-z])", "∑"),
    (r"\\geq", "≥"),
    (r"\\leq", "≤"),
    (r"\\neq", "≠"),
    (r"\\cdot", "·"),
    (r"\\mu", "μ"),
    (r"\\pi(?![a-z])", "π"),
    (r"\\in(?![a-z])", "∈"),
    (r"\\pm", "±"),
    (r"\\\\", "\\"),
    (r"\\{", "{"),
    (r"\\}", "}"),
]


def latex_to_unicode(text: str) -> str:
    # Strip \(...\) and \[...\] delimiters
    text = re.sub(r"\\\((.+?)\\\)", r"\1", text)
    text = re.sub(r"\\\[(.+?)\\\]", r"\1", text)

    for pattern, replacement in LATEX_REPLACEMENTS:
        # Use a lambda so the replacement string is never interpreted as a regex
        # replacement template (avoids issues with bare backslashes in replacement).
        repl = replacement
        text = re.sub(pattern, lambda m, r=repl: r, text)

    return text
