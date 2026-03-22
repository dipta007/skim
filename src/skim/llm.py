import base64
import hashlib
import importlib.resources
from pathlib import Path

from openai import OpenAI

from skim.config import Config

PROMPT_MAP = {
    "story": "story.md",
    "deep": "deep.md",
}


def prompt_hash(summary_type: str) -> str:
    prompt_path = importlib.resources.files("skim.prompts") / PROMPT_MAP[summary_type]
    content = prompt_path.read_text(encoding="utf-8")
    return hashlib.sha256(content.encode()).hexdigest()[:8]


def _generate_openai(pdf_path: Path, summary_type: str, config: Config) -> str:
    prompt_path = importlib.resources.files("skim.prompts") / PROMPT_MAP[summary_type]
    system_prompt = prompt_path.read_text(encoding="utf-8")

    pdf_base64 = base64.b64encode(pdf_path.read_bytes()).decode("utf-8")

    client = OpenAI(api_key=config.api_key, base_url=config.base_url)

    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "file",
                        "file": {
                            "filename": pdf_path.name,
                            "file_data": f"data:application/pdf;base64,{pdf_base64}",
                        },
                    },
                    {
                        "type": "text",
                        "text": "Generate the summary for this paper.",
                    },
                ],
            },
        ],
    )

    return response.choices[0].message.content


def generate_summary(pdf_path: Path, summary_type: str, config: Config) -> str:
    if config.backend == "claude":
        from skim.claude_backend import generate_summary_claude

        return generate_summary_claude(pdf_path, summary_type, config)
    return _generate_openai(pdf_path, summary_type, config)
