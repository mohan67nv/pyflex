"""
Author: Mohana Nyamanahalli Venkatesha
Description: Defines the command-line interface (CLI) for PyFlex using Typer.
"""
import typer
from pathlib import Path
from .roast import roast_file
from .flex import show_flex_card
from rich.console import Console

app = typer.Typer(
    name="pyflex",
    help="PyFlex: A viral hybrid code-profiler and AI-linter.",
    add_completion=False,
)

@app.callback()
def callback():
    pass

console = Console()

@app.command()
def roast(
    filepath: Path = typer.Argument(..., help="Path to the Python file you want to roast."),
    export: str = typer.Option(None, "--export", "-e", help="Path to save the output as an SVG image.")
):
    """
    Statically analyzes a Python file to find the most complex function,
    checks git blame for the author, and generates a humorous roast.
    """
    if not filepath.exists() or not filepath.is_file():
        console.print(f"[bold red]Error:[/bold red] File '{filepath}' does not exist.")
        raise typer.Exit(code=1)
        
    if filepath.suffix != '.py':
        console.print(f"[bold red]Error:[/bold red] File '{filepath}' must be a Python file (.py).")
        raise typer.Exit(code=1)
        
    roast_file(str(filepath), export)

@app.command()
def flex(
    export: str = typer.Option(None, "--export", "-e", help="Path to save the output as an SVG image.")
):
    """
    Generates a viral GitHub Stats Card based on your local Git repository history.
    Calculates total LOC, commit streaks, total functions, and LOC written in the last 30 days!
    """
    show_flex_card(export)

if __name__ == "__main__":
    app()
