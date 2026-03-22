import argparse
import os
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown

import skim
from skim.arxiv import download_pdf, parse_arxiv_id
from skim.cache import get_cached, save
from skim.config import load_config
from skim.init_cmd import run_init
from skim.latex import latex_to_unicode
from skim.llm import generate_summary

ALL_TYPES = ["story", "deep"]
DISPLAY_LABELS = {"story": "STORY", "deep": "DEEP DIVE"}

console = Console()
err_console = Console(stderr=True)


def resolve_types(raw: list[str]) -> list[str]:
    if "all" in raw:
        return list(ALL_TYPES)
    return list(dict.fromkeys(raw))


def print_summary(summary_type: str, content: str, cached: bool = False) -> None:
    label = DISPLAY_LABELS.get(summary_type, summary_type.upper())
    tag = " [green](cached)[/green]" if cached else ""
    console.print()
    console.rule(f"[bold blue]{label}[/bold blue]{tag}")
    console.print()
    terminal_content = latex_to_unicode(content)
    console.print(Markdown(terminal_content))
    console.print()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="skim",
        description="Generate plain-language narratives and technical summaries from arxiv papers.",
    )
    parser.add_argument(
        "--version", action="version", version=f"skim {skim.__version__}"
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("init", help="Set up skim (API key, output directory, etc.)")
    subparsers.add_parser("cd", help="Print output directory path (use: cd $(skim cd))")

    parser.add_argument(
        "-p",
        "--paper",
        help="Arxiv paper ID or URL (e.g., 2509.16538 or https://arxiv.org/abs/2509.16538)",
    )
    parser.add_argument(
        "-t",
        "--type",
        nargs="+",
        choices=["story", "deep", "all"],
        help="Summary type(s): story, deep, or all",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Override output directory for this invocation",
    )

    args = parser.parse_args()

    if args.command == "init":
        run_init()
        return

    if args.command == "cd":
        config = load_config()
        print(config.output_dir)
        return

    if not args.paper or not args.type:
        parser.print_help()
        sys.exit(1)

    config = load_config()

    try:
        arxiv_id = parse_arxiv_id(args.paper)
    except ValueError as e:
        err_console.print(f"[red bold]Error:[/] {e}")
        sys.exit(1)

    summary_types = resolve_types(args.type)
    output_dir = args.output_dir or config.output_dir

    all_cached = all(
        get_cached(arxiv_id, st, output_dir) is not None for st in summary_types
    )

    pdf_path: Path | None = None
    if not all_cached:
        try:
            with console.status(
                f"[bold cyan]Downloading paper {arxiv_id}...[/]", spinner="dots"
            ):
                pdf_path = download_pdf(arxiv_id)
        except Exception as e:
            err_console.print(f"[red bold]Error:[/] Failed to download paper: {e}")
            sys.exit(1)

    try:
        for st in summary_types:
            cached_content = get_cached(arxiv_id, st, output_dir)
            if cached_content is not None:
                print_summary(st, cached_content, cached=True)
                continue

            try:
                with console.status(
                    f"[bold cyan]Generating {DISPLAY_LABELS.get(st, st)}...[/]",
                    spinner="dots",
                ):
                    result = generate_summary(pdf_path, st, config)
            except Exception as e:
                err_console.print(f"[red bold]Error:[/] Failed to generate {st}: {e}")
                continue

            out_path = save(arxiv_id, st, result, output_dir)
            err_console.print(f"[dim]Saved to {out_path}[/]")
            print_summary(st, result)

    finally:
        if pdf_path is not None and pdf_path.exists():
            os.unlink(pdf_path)
