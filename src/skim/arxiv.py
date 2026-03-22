import re
import tempfile
from pathlib import Path

import httpx

ARXIV_ID_PATTERN = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")
ARXIV_PDF_URL = "https://arxiv.org/pdf/{arxiv_id}"
DOWNLOAD_TIMEOUT = 60.0


def parse_arxiv_id(input_str: str) -> str:
    match = ARXIV_ID_PATTERN.search(input_str)
    if not match:
        raise ValueError(f"Could not parse arxiv ID from: {input_str}")
    return match.group(1)


def download_pdf(arxiv_id: str) -> Path:
    url = ARXIV_PDF_URL.format(arxiv_id=arxiv_id)
    response = httpx.get(url, follow_redirects=True, timeout=DOWNLOAD_TIMEOUT)
    response.raise_for_status()

    tmp = tempfile.NamedTemporaryFile(
        suffix=".pdf", prefix=f"arxiv_{arxiv_id}_", delete=False
    )
    tmp.write(response.content)
    tmp.close()
    return Path(tmp.name)
