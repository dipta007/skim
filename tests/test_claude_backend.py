import json

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from skim.config import Config
from skim.claude_backend import generate_summary_claude, _check_claude_installed


pytestmark = pytest.mark.claude


@pytest.fixture
def claude_config():
    return Config(
        backend="claude",
        api_key="",
        base_url="",
        model="sonnet",
        output_dir=Path("/tmp/skim-test"),
    )


def test_check_claude_installed_missing():
    with patch("skim.claude_backend.shutil.which", return_value=None):
        with pytest.raises(RuntimeError, match="Claude Code CLI not found"):
            _check_claude_installed()


def test_check_claude_installed_found():
    with patch("skim.claude_backend.shutil.which", return_value="/usr/bin/claude"):
        _check_claude_installed()


def test_generate_summary_success(tmp_path, claude_config):
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 fake")

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = json.dumps({"result": "# Summary\nTest content."})

    with (
        patch("skim.claude_backend.shutil.which", return_value="/usr/bin/claude"),
        patch(
            "skim.claude_backend.subprocess.run", return_value=mock_result
        ) as mock_run,
    ):
        result = generate_summary_claude(pdf_path, "story", claude_config)

    assert result == "# Summary\nTest content."
    call_args = mock_run.call_args[0][0]
    assert call_args[0] == "claude"
    assert "--model" in call_args
    assert "sonnet" in call_args


def test_generate_summary_cli_failure(tmp_path, claude_config):
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 fake")

    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "Something went wrong"

    with (
        patch("skim.claude_backend.shutil.which", return_value="/usr/bin/claude"),
        patch("skim.claude_backend.subprocess.run", return_value=mock_result),
    ):
        with pytest.raises(RuntimeError, match="Claude CLI failed"):
            generate_summary_claude(pdf_path, "story", claude_config)


def test_generate_summary_error_response(tmp_path, claude_config):
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 fake")

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = json.dumps({"is_error": True, "result": "Rate limited"})

    with (
        patch("skim.claude_backend.shutil.which", return_value="/usr/bin/claude"),
        patch("skim.claude_backend.subprocess.run", return_value=mock_result),
    ):
        with pytest.raises(RuntimeError, match="Claude returned error"):
            generate_summary_claude(pdf_path, "story", claude_config)
