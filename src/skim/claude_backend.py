import importlib.resources
import json
import subprocess
import shutil
from pathlib import Path

from skim.config import Config
from skim.llm import PROMPT_MAP


def _check_claude_installed() -> None:
    if shutil.which("claude") is None:
        raise RuntimeError(
            "Claude Code CLI not found. Install it from https://claude.ai/code"
        )


def generate_summary_claude(pdf_path: Path, summary_type: str, config: Config) -> str:
    _check_claude_installed()

    prompt_resource = (
        importlib.resources.files("skim.prompts") / PROMPT_MAP[summary_type]
    )
    system_prompt = prompt_resource.read_text(encoding="utf-8")

    user_prompt = (
        f"Read the PDF file at {pdf_path} and generate the summary. "
        f"Output ONLY the summary markdown, nothing else."
    )

    result = subprocess.run(
        [
            "claude",
            "-p",
            user_prompt,
            "--system-prompt",
            system_prompt,
            "--model",
            config.model,
            "--output-format",
            "json",
            "--allowedTools",
            "Read",
        ],
        capture_output=True,
        text=True,
        timeout=300,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Claude CLI failed: {result.stderr.strip()}")

    data = json.loads(result.stdout)
    if data.get("is_error"):
        raise RuntimeError(f"Claude returned error: {data.get('result', 'unknown')}")

    return data["result"]
