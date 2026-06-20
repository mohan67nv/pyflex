import ast
import subprocess
import random
from typing import Tuple, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexities = {}

    def visit_FunctionDef(self, node):
        complexity = 1  # Base complexity
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                # Count boolean operators like 'and', 'or'
                complexity += len(child.values) - 1
        
        self.complexities[node.name] = {
            'complexity': complexity,
            'lineno': node.lineno,
            'end_lineno': getattr(node, 'end_lineno', node.lineno)
        }
        self.generic_visit(node)

def get_most_complex_function(filepath: str) -> Optional[dict]:
    """Finds the function with the highest cyclomatic complexity in the given file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=filepath)
    
    visitor = ComplexityVisitor()
    visitor.visit(tree)
    
    if not visitor.complexities:
        return None
    
    # Return the function info with max complexity
    most_complex_name = max(visitor.complexities, key=lambda k: visitor.complexities[k]['complexity'])
    result = visitor.complexities[most_complex_name]
    result['name'] = most_complex_name
    return result

def get_git_blame_author(filepath: str, start_line: int, end_line: int) -> str:
    """Uses git blame to find the author who contributed the most lines to a block."""
    try:
        # Run git blame for the specific line range
        result = subprocess.run(
            ['git', 'blame', '-L', f'{start_line},{end_line}', '--line-porcelain', filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        # Extract authors from output (lines starting with 'author ')
        authors = []
        for line in result.stdout.splitlines():
            if line.startswith('author '):
                authors.append(line.replace('author ', '').strip())
                
        if not authors:
            return "Anonymous Coward"
            
        # Return the most frequent author
        return max(set(authors), key=authors.count)
    except subprocess.CalledProcessError:
        return "Unknown Git-less Developer"
    except Exception:
        return "Mystery Coder"

def generate_roast(author: str, func_name: str, complexity: int) -> str:
    """Generates a humorous roast string."""
    roasts = [
        f"Hey {author}, your function '{func_name}' has a complexity of {complexity}. Are you trying to heat up your room with CPU cycles?",
        f"Dear {author}, I saw your function '{func_name}'. We are writing Python, not solving a 4D Rubik's Cube. (Complexity: {complexity})",
        f"{author}, '{func_name}' is so nested that it needs its own ZIP code. Please refactor. (Complexity: {complexity})",
        f"Wow {author}, '{func_name}' has an impressive complexity of {complexity}. Impressively bad, that is.",
        f"Attention {author}: '{func_name}' looks like a plate of spaghetti. Time to grab a fork and untangle it. (Complexity: {complexity})"
    ]
    return random.choice(roasts)

def roast_file(filepath: str, export_path: str = None):
    """Parses the file, finds the worst function, and roasts the author."""
    console = Console(record=True)
    
    func_info = get_most_complex_function(filepath)
    if not func_info:
        console.print("[dim]No functions found to roast in this file.[/dim]")
        return
        
    author = get_git_blame_author(filepath, func_info['lineno'], func_info['end_lineno'])
    roast_text = generate_roast(author, func_info['name'], func_info['complexity'])
    
    # Render with neon border
    text = Text(roast_text, justify="center", style="bold white")
    panel = Panel(
        text, 
        title="[bold red]🔥 AI Code Roaster 🔥[/bold red]",
        border_style="bold magenta", 
        padding=(1, 2)
    )
    
    console.print()
    console.print(panel)
    console.print()

    if export_path:
        console.save_svg(export_path, title=f"Roast: {filepath}")
        console.print(f"[dim]Roast exported to {export_path}[/dim]")

