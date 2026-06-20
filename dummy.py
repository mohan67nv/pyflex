from pyflex import speedrun
import time

@speedrun(guess_complexity=True, export_path="dummy_speedrun.svg")
def slow_spaghetti(n: int):
    # This is a terrible O(N^2) function
    total = 0
    for i in range(n):
        for j in range(n):
            if i % 2 == 0 and j % 2 == 0:
                total += 1
    return total

if __name__ == "__main__":
    slow_spaghetti(100)
