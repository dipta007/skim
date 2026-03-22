import os
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

import tomli_w
from rich.console import Console

err_console = Console(stderr=True)


@dataclass(frozen=True)
class Config:
    api_key: str
    base_url: str
    model: str
    output_dir: Path


def config_path() -> Path:
    xdg = os.getenv("XDG_CONFIG_HOME")
    config_home = Path(xdg) if xdg else Path.home() / ".config"
    return config_home / "skim" / "config.toml"


def load_config() -> Config:
    path = config_path()
    if not path.exists():
        err_console.print(
            "[red bold]Error:[/] Not configured. Run [cyan]skim init[/] to set up."
        )
        sys.exit(1)

    with open(path, "rb") as f:
        data = tomllib.load(f)

    api_key = data.get("api", {}).get("key", "")
    if not api_key:
        err_console.print(
            "[red bold]Error:[/] API key not set. Run [cyan]skim init[/] to configure."
        )
        sys.exit(1)

    return Config(
        api_key=api_key,
        base_url=data.get("api", {}).get("base_url", "https://api.openai.com/v1"),
        model=data.get("api", {}).get("model", "gpt-5.4-nano"),
        output_dir=Path(data.get("output", {}).get("dir", "~/papers/skim")).expanduser(),
    )


def save_config(config: Config) -> Path:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "api": {
            "key": config.api_key,
            "base_url": config.base_url,
            "model": config.model,
        },
        "output": {
            "dir": str(config.output_dir),
        },
    }

    with open(path, "wb") as f:
        tomli_w.dump(data, f)

    return path
