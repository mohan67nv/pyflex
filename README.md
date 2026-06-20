# PyFlex 💪

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

A viral, highly shareable hybrid code-profiler and AI-linter designed purely for developer pride. Benchmark your functions, roast your code, and generate beautiful terminal outputs that you can screenshot and share on LinkedIn and X!

![Flex Card Demo](https://raw.githubusercontent.com/mohan67nv/pyflex/master/assets/flex_demo.svg?v=1)

## Features

- ⏱ **SpeedRun Decorator**: Measure exact execution time, peak memory footprint, and guess the Big-O complexity of your functions.
- 🖼 **Export to Image**: Export your SpeedRun Certificates as beautiful SVGs instantly.
- 🍝 **AI Roaster CLI**: Statically analyzes your Python files, finds the function with the worst cyclomatic complexity, runs `git blame` to find the author, and generates a humorous roast inside a neon terminal panel.
- 🏆 **Developer Flex Card**: Parses your local Git repository to calculate your Total LOC, total functions, maximum commit streak, and 30-day coding volume into a sleek, viral Stats Card!

## Installation

```bash
pip install pyflex
```

## Usage

### 🖼 Exporting Images
Every PyFlex command and decorator supports exporting its beautiful terminal output directly to an SVG image! This is perfect for sharing on X (Twitter) or LinkedIn.

For CLI commands, simply append `--export <filename.svg>`:
```bash
pyflex flex --export my_flex_card.svg
pyflex roast your_script.py --export roast_demo.svg
```
For the decorator, simply add the `export_path` argument: `@speedrun(export_path="my_speedrun.svg")`

### 1. The `@speedrun` Decorator

Add the `@speedrun` decorator to your functions to benchmark them and get a beautifully formatted "SpeedRun Certificate".

```python
from pyflex import speedrun

@speedrun(guess_complexity=True, export_path="my_function.svg")
def my_complex_function(n: int):
    # Some intensive logic...
    return sum(i * i for i in range(n))

my_complex_function(100)
```

**Output:**
A stunning Rich-formatted table in your terminal showing the Execution Time, Peak Memory, Estimated Big-O complexity, and your assigned Rank (e.g., "S-Tier: The Alchemist" or "F-Tier: The Spaghetti Chef"). If `export_path` is specified, it saves an SVG image ready for social media!

![SpeedRun Demo](https://raw.githubusercontent.com/mohan67nv/pyflex/master/assets/dummy_speedrun.svg?v=1)

### 2. The AI Roaster CLI

Want to publicly roast your coworkers (or yourself) for writing spaghetti code? Use the `pyflex roast` command.

```bash
pyflex roast your_script.py
```

**What it does:**
1. Scans `my_script.py` using Python's `ast` module.
2. Identifies the function with the highest cyclomatic complexity (most nested loops and `if` statements).
3. Uses `git blame` to figure out who wrote it.
4. Prints a hilarious, neon-bordered roast directly in your terminal.

![Roast Demo](https://raw.githubusercontent.com/mohan67nv/pyflex/master/assets/roast_demo.svg?v=1)

### 3. The Developer Flex Card

Generate a stunning "GitHub Stats Card" using your local Git history.

```bash
pyflex flex
```

**What it does:**
1. Parses your local `.git` repository.
2. Computes your Total Lines of Code (LOC) for Python files.
3. Uses AST to count the total number of functions in your codebase.
4. Calculates your longest consecutive commit streak in days.
5. Tallies how many lines of code you wrote in the last 30 days!

---

*Made for developers who want to show off their O(1) algorithms or get roasted for their O(N^2) loops.*
