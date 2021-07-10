import os

def lint(text=""):
    """Print with log"""

    with open("log", "w") as logfile:
        logfile.write(f"\n{text}")
    print(text)
