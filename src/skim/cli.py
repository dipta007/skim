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
from skim.llm import generate_summary, prompt_hash
from skim.viewer import open_in_browser

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
    clean_parser = subparsers.add_parser("clean", help="Clear cached summaries")
    clean_parser.add_argument(
        "-p",
        "--paper",
        help="Only clear cache for this arxiv paper ID or URL",
    )

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
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open summaries in browser with LaTeX rendering",
    )

    args = parser.parse_args()

    if args.command == "init":
        run_init()
        return

    if args.command == "cd":
        config = load_config()
        print(config.output_dir)
        return

    if args.command == "clean":
        config = load_config()
        output_dir = config.output_dir
        if not output_dir.exists():
            err_console.print("[dim]Nothing to clean.[/]")
            return
        if args.paper:
            try:
                arxiv_id = parse_arxiv_id(args.paper)
            except ValueError as e:
                err_console.print(f"[red bold]Error:[/] {e}")
                sys.exit(1)
            files = list(output_dir.glob(f"{arxiv_id}_*.md"))
        else:
            files = list(output_dir.glob("*.md"))
        if not files:
            err_console.print("[dim]Nothing to clean.[/]")
            return
        for f in files:
            f.unlink()
        label = "summary" if len(files) == 1 else "summaries"
        err_console.print(f"[green]Removed {len(files)} cached {label}.[/]")
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

    prompt_hashes = {st: prompt_hash(st) for st in summary_types}

    all_cached = all(
        get_cached(arxiv_id, st, prompt_hashes[st], output_dir) is not None
        for st in summary_types
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

    sections: list[str] = []
    try:
        for st in summary_types:
            cached_content = get_cached(arxiv_id, st, prompt_hashes[st], output_dir)
            if cached_content is not None:
                if not args.open:
                    print_summary(st, cached_content, cached=True)
                sections.append(cached_content)
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

            out_path = save(arxiv_id, st, prompt_hashes[st], result, output_dir)
            err_console.print(f"[dim]Saved to {out_path}[/]")
            if not args.open:
                print_summary(st, result)
            sections.append(result)

    finally:
        if pdf_path is not None and pdf_path.exists():
            os.unlink(pdf_path)

    if args.open and sections:
        combined = "\n\n---\n\n".join(sections)
        open_in_browser(combined, title=f"skim — {arxiv_id}")

    if sections:
        for st in summary_types:
            p = output_dir / f"{arxiv_id}_{st}_{prompt_hashes[st]}.md"
            if p.exists():
                err_console.print(f"[bold green]>>>[/] [cyan]{p}[/]")
