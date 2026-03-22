from unittest.mock import patch
from skim.init_cmd import run_init
from skim.config import load_config


def test_run_init_creates_config(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    output_dir = tmp_path / "papers"

    with patch(
        "skim.init_cmd.Prompt.ask",
        side_effect=[
            "openai-compatible",
            "https://api.openai.com/v1",
            "sk-test-key",
            "gpt-5.4-nano",
            str(output_dir),
        ],
    ):
        run_init()

    cfg = load_config()
    assert cfg.api_key == "sk-test-key"
    assert cfg.output_dir == output_dir
    assert output_dir.exists()


def test_run_init_overwrite_declined(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    cfg_dir = tmp_path / "skim"
    cfg_dir.mkdir()
    (cfg_dir / "config.toml").write_text("existing")

    with patch("skim.init_cmd.Prompt.ask", return_value="n"):
        with patch("skim.init_cmd.Confirm.ask", return_value=False):
            run_init()

    assert (cfg_dir / "config.toml").read_text() == "existing"
