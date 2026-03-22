import pytest
import httpx
from unittest.mock import MagicMock, patch
from skim.arxiv import parse_arxiv_id


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("2603.10165", "2603.10165"),
        ("2603.10165v1", "2603.10165"),
        ("2603.10165v3", "2603.10165"),
        ("https://arxiv.org/abs/2603.10165", "2603.10165"),
        ("https://arxiv.org/abs/2603.10165v2", "2603.10165"),
        ("https://arxiv.org/pdf/2603.10165", "2603.10165"),
        ("https://arxiv.org/pdf/2603.10165v1", "2603.10165"),
        ("http://arxiv.org/abs/2603.10165", "2603.10165"),
        ("2601.06767", "2601.06767"),
    ],
)
def test_parse_arxiv_id(input_str, expected):
    assert parse_arxiv_id(input_str) == expected


def test_parse_arxiv_id_invalid():
    with pytest.raises(ValueError, match="Could not parse arxiv ID"):
        parse_arxiv_id("not-an-id")


def test_parse_arxiv_id_invalid_url():
    with pytest.raises(ValueError, match="Could not parse arxiv ID"):
        parse_arxiv_id("https://example.com/some-page")


def test_download_pdf_success():
    from skim.arxiv import download_pdf
    mock_response = MagicMock()
    mock_response.content = b"%PDF-1.4 fake"
    mock_response.raise_for_status = MagicMock()
    with patch("skim.arxiv.httpx.get", return_value=mock_response):
        path = download_pdf("2603.10165")
    assert path.exists()
    assert path.read_bytes() == b"%PDF-1.4 fake"
    path.unlink()


def test_download_pdf_http_error():
    from skim.arxiv import download_pdf
    with patch("skim.arxiv.httpx.get") as mock_get:
        mock_get.side_effect = httpx.HTTPStatusError(
            "404", request=MagicMock(), response=MagicMock()
        )
        with pytest.raises(httpx.HTTPStatusError):
            download_pdf("0000.00000")
