import functools
import time
import inspect
from memory_profiler import memory_usage
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import big_o

def _assign_rank(time_taken: float, complexity_str: str) -> str:
    """Assigns a humorous rank based on time and complexity."""
    if "O(1)" in complexity_str or time_taken < 0.001:
        return "[bold yellow]S-Tier: The Alchemist[/bold yellow] :sparkles:"
    elif "O(N)" in complexity_str or time_taken < 0.05:
        return "[bold green]A-Tier: The Tryhard[/bold green] :fire:"
    elif "O(N^2)" in complexity_str or time_taken < 0.5:
        return "[bold blue]C-Tier: The Bootcamper[/bold blue] :turtle:"
    else:
        return "[bold red]F-Tier: The Spaghetti Chef[/bold red] :spaghetti:"

def speedrun(guess_complexity: bool = False, export_path: str = None, data_generator=None):
    """
    A decorator to benchmark functions, guess their Big-O complexity, 
    and print a visually striking SpeedRun Certificate.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 1. Measure Execution Time and Memory
            start_time = time.perf_counter()
            # Run the function while profiling memory
            mem_usage, retval = memory_usage((func, args, kwargs), retval=True, interval=0.01)
            end_time = time.perf_counter()
            
            exec_time = end_time - start_time
            peak_memory = max(mem_usage) - min(mem_usage) if mem_usage else 0.0

            # 2. Big-O Complexity Guessing
            complexity_str = "N/A (Use `guess_complexity=True`)"
            if guess_complexity:
                try:
                    # Default to generating integer N if no generator is provided
                    generator = data_generator if data_generator else lambda n: big_o.datagen.n_(n)
                    
                    # Intercept the function to feed scaling dummy data
                    # We suppress output and handle the big_O estimation
                    best_fit, _ = big_o.big_o(func, generator, n_measures=5, min_n=10, max_n=1000)
                    complexity_str = str(best_fit)
                except Exception as e:
                    complexity_str = f"Error: Could not infer ({str(e)})"
            
            # 3. Assign Rank
            rank = _assign_rank(exec_time, complexity_str)

            # 4. Render Output
            console = Console(record=True)
            table = Table(title=f"SpeedRun Certificate: [bold cyan]{func.__name__}[/bold cyan]", show_header=True, header_style="bold magenta")
            table.add_column("Metric", style="dim", width=15)
            table.add_column("Value", justify="right")

            table.add_row("Execution Time", f"{exec_time:.6f} seconds")
            table.add_row("Peak Memory", f"{peak_memory:.4f} MB")
            table.add_row("Est. Big-O", complexity_str)
            table.add_row("Rank", rank)

            # Print to terminal
            console.print()
            console.print(table)
            console.print()

            # 5. Export Image (SVG)
            if export_path:
                console.save_svg(export_path, title=f"SpeedRun: {func.__name__}")
                console.print(f"[dim]Certificate exported to {export_path}[/dim]")

            return retval
        return wrapper
    return decorator
