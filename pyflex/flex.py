"""
Author: Mohana Nyamanahalli Venkatesha
Description: Computes developer statistics from Git history and generates a GitHub Flex Card.
"""
import subprocess
import ast
import re
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich import box
from rich.align import Align

def _run_git_cmd(args: list) -> str:
    try:
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""

def get_git_author() -> str:
    return _run_git_cmd(["git", "config", "user.name"]) or "Anonymous Developer"

def get_tracked_python_files() -> list:
    output = _run_git_cmd(["git", "ls-files"])
    if not output:
        return []
    return [f for f in output.splitlines() if f.endswith('.py')]

def get_total_loc(files: list) -> int:
    total_loc = 0
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                total_loc += sum(1 for _ in file)
        except Exception:
            pass
    return total_loc

def get_total_functions(files: list) -> int:
    total_funcs = 0
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=filepath)
            total_funcs += sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
        except Exception:
            pass
    return total_funcs

def get_loc_last_month(author: str) -> int:
    # Get shortstat for the last month for the specific author
    output = _run_git_cmd(["git", "log", f"--author={author}", "--since=1 month ago", "--shortstat"])
    if not output:
        return 0
    
    # Example shortstat: 1 file changed, 10 insertions(+), 5 deletions(-)
    insertions = 0
    for line in output.splitlines():
        match = re.search(r'(\d+)\s+insertion', line)
        if match:
            insertions += int(match.group(1))
    return insertions

def get_commit_streak(author: str) -> int:
    output = _run_git_cmd(["git", "log", f"--author={author}", "--format=%ad", "--date=short"])
    if not output:
        return 0
        
    dates_str = output.splitlines()
    if not dates_str:
        return 0
        
    # Convert to unique date objects and sort them ascending
    dates = sorted(list(set(datetime.strptime(d, "%Y-%m-%d").date() for d in dates_str)))
    
    if not dates:
        return 0
        
    # Calculate longest streak
    longest_streak = 1
    current_streak = 1
    
    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1
            
    return longest_streak

def get_time_spent(author: str) -> float:
    # Get all commit UNIX timestamps, sorted oldest to newest
    output = _run_git_cmd(["git", "log", f"--author={author}", "--format=%at"])
    if not output:
        return 0.0
        
    timestamps = sorted([int(t) for t in output.splitlines() if t.strip().isdigit()])
    if not timestamps:
        return 0.0
        
    total_seconds = 1800  # Base 30 mins for the first commit
    for i in range(1, len(timestamps)):
        diff = timestamps[i] - timestamps[i-1]
        # If commits are within 2 hours of each other, count the time. 
        # Otherwise, assume a new session started (add 30 mins).
        if diff < 7200:
            total_seconds += diff
        else:
            total_seconds += 1800
            
    return total_seconds / 3600.0

def get_coding_persona(author: str) -> str:
    output = _run_git_cmd(["git", "log", f"--author={author}", "--format=%at"])
    if not output:
        return "Unknown 👻"
        
    timestamps = [int(t) for t in output.splitlines() if t.strip().isdigit()]
    if not timestamps:
        return "Unknown 👻"
        
    hours = [datetime.fromtimestamp(t).hour for t in timestamps]
    avg_hour = sum(hours) / len(hours)
    
    if avg_hour < 6 or avg_hour >= 23:
        return "Night Owl 🦉"
    elif 6 <= avg_hour < 12:
        return "Early Bird 🌅"
    elif 12 <= avg_hour < 18:
        return "Afternoon Architect ☕"
    else:
        return "Evening Engineer 🌙"

def show_flex_card(export_path: str = None):
    console = Console(record=True)
    
    # 1. Gather stats
    author = get_git_author()
    py_files = get_tracked_python_files()
    
    if not py_files:
        console.print("[bold red]Warning:[/bold red] No tracked Python files found. Are you in a Git repository?")
        # Let's show dummy stats if not in git just so they can see the flex card
        if not _run_git_cmd(["git", "status"]):
            console.print("[dim]Generating a mock flex card for demonstration...[/dim]")
            total_loc = 1337
            total_funcs = 42
            loc_last_month = 500
            streak = 7
            time_spent_hrs = 24.5
            persona = "Mockingbird 🐦"
        else:
            return
    else:
        total_loc = get_total_loc(py_files)
        total_funcs = get_total_functions(py_files)
        loc_last_month = get_loc_last_month(author)
        streak = get_commit_streak(author)
        time_spent_hrs = get_time_spent(author)
        persona = get_coding_persona(author)

    # 2. Design the Card
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
    table.add_column("Stat", style="bold cyan")
    table.add_column("Value", style="bold white", justify="right")
    
    table.add_row("👨‍💻 Developer", f"[bold yellow]{author}[/bold yellow]")
    table.add_row("💻 Primary Language", "Python 🐍")
    table.add_row("🎭 Coding Persona", f"[bold magenta]{persona}[/bold magenta]")
    table.add_row("📈 Total Python LOC", f"{total_loc:,}")
    table.add_row("🛠️ Total Functions", f"{total_funcs:,}")
    table.add_row("⏳ Est. Time Spent", f"{time_spent_hrs:,.1f} hours")
    table.add_row("🔥 Commit Streak", f"{streak} days")
    table.add_row("📅 LOC Last 30 Days", f"+{loc_last_month:,} lines")

    panel = Panel(
        table,
        title="[bold green]🏆 GitHub Flex Card 🏆[/bold green]",
        border_style="bold green",
        padding=(1, 4),
        expand=False
    )
    
    console.print()
    console.print(Align.center(panel))
    console.print()

    if export_path:
        console.save_svg(export_path, title=f"Flex Card: {author}")
        console.print(f"[dim]Flex Card exported to {export_path}[/dim]")
