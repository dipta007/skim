from pathlib import Path


def _cache_path(arxiv_id: str, summary_type: str, output_dir: Path) -> Path:
    return output_dir / f"{arxiv_id}_{summary_type}.md"


def get_cached(arxiv_id: str, summary_type: str, output_dir: Path) -> str | None:
    path = _cache_path(arxiv_id, summary_type, output_dir)
    if path.exists():
        return path.read_text()
    return None


def save(arxiv_id: str, summary_type: str, content: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = _cache_path(arxiv_id, summary_type, output_dir)
    path.write_text(content)
    return path
