import tomli_w
from pathlib import Path
from skim.config import load_config, save_config, config_path, Config


def test_config_path_default(monkeypatch):
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    path = config_path()
    assert str(path).endswith(".config/skim/config.toml")


def test_config_path_xdg(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    path = config_path()
    assert path == tmp_path / "skim" / "config.toml"


def test_save_and_load_config(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    cfg = Config(
        api_key="sk-test",
        base_url="https://api.openai.com/v1",
        model="gpt-5.4-nano",
        output_dir=Path("/tmp/skim-output"),
    )
    save_config(cfg)
    loaded = load_config()
    assert loaded.api_key == "sk-test"
    assert loaded.base_url == "https://api.openai.com/v1"
    assert loaded.model == "gpt-5.4-nano"
    assert loaded.output_dir == Path("/tmp/skim-output")


def test_load_config_missing_file(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    try:
        load_config()
        assert False, "Should have raised SystemExit"
    except SystemExit:
        pass


def test_load_config_empty_api_key(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    cfg_dir = tmp_path / "skim"
    cfg_dir.mkdir()
    cfg_file = cfg_dir / "config.toml"
    cfg_file.write_text(
        tomli_w.dumps(
            {
                "api": {"key": "", "base_url": "x", "model": "y"},
                "output": {"dir": "/tmp"},
            }
        )
    )
    try:
        load_config()
        assert False, "Should have raised SystemExit"
    except SystemExit:
        pass
