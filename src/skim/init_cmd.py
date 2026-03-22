from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm, Prompt

from skim.config import Config, config_path, load_config, save_config

console = Console()


def run_init() -> None:
    path = config_path()

    existing: Config | None = None
    if path.exists():
        if not Confirm.ask(
            f"[yellow]Config already exists at {path}. Overwrite?[/]",
            default=False,
        ):
            console.print("[dim]Cancelled.[/]")
            return
        try:
            existing = load_config()
        except SystemExit:
            existing = None

    console.print("[bold]Setting up skim...[/]\n")

    default_backend = existing.backend if existing else "openai-compatible"
    backend = Prompt.ask(
        "[bold]Backend[/] (openai or claude)",
        choices=["openai-compatible", "claude"],
        default=default_backend,
    )

    if backend == "openai-compatible":
        default_base_url = (
            existing.base_url if existing else "https://api.openai.com/v1"
        )
        default_api_key = existing.api_key if existing else None
        default_model = existing.model if existing else "gpt-5.4-nano"

        base_url = Prompt.ask("[bold]Base URL[/]", default=default_base_url)
        api_key = Prompt.ask("[bold]API key[/]", default=default_api_key)
        model = Prompt.ask("[bold]Model[/]", default=default_model)
    else:
        base_url = ""
        api_key = ""
        default_model = existing.model if existing else "sonnet"
        model = Prompt.ask(
            "[bold]Model[/] (haiku, sonnet, opus)", default=default_model
        )

    default_output_dir = str(existing.output_dir) if existing else "~/papers/skim"
    output_dir_str = Prompt.ask("[bold]Output directory[/]", default=default_output_dir)

    output_dir = Path(output_dir_str).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    config = Config(
        backend=backend,
        api_key=api_key,
        base_url=base_url,
        model=model,
        output_dir=output_dir,
    )
    saved_path = save_config(config)
    console.print(f"\n[green bold]Done![/] Config saved to [cyan]{saved_path}[/]")
