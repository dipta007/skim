from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm, Prompt

from skim.config import Config, config_path, save_config

console = Console()


def run_init() -> None:
    path = config_path()

    if path.exists():
        if not Confirm.ask(
            f"[yellow]Config already exists at {path}. Overwrite?[/]",
            default=False,
        ):
            console.print("[dim]Cancelled.[/]")
            return

    console.print("[bold]Setting up skim...[/]\n")

    api_key = Prompt.ask("[bold]API key[/]")
    base_url = Prompt.ask("[bold]Base URL[/]", default="https://api.openai.com/v1")
    model = Prompt.ask("[bold]Model[/]", default="gpt-5.4-nano")
    output_dir_str = Prompt.ask("[bold]Output directory[/]", default="~/papers/skim")

    output_dir = Path(output_dir_str).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    config = Config(
        api_key=api_key,
        base_url=base_url,
        model=model,
        output_dir=output_dir,
    )
    saved_path = save_config(config)
    console.print(f"\n[green bold]Done![/] Config saved to [cyan]{saved_path}[/]")
