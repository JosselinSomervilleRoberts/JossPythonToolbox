import os
from typing import List

class Colors:
    """Colors for printing in the terminal."""
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def get_terminal_width() -> int:
    """
    Returns the width of the terminal.
    Usage: get_terminal_width()
    """
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80
   
def print_subset_of_args(args: dict, title: str, list_of_args: List["str"], color: str = Colors.BLUE, print_length: int = 50, var_length: int = 15) -> None:
    """
    Prints a subset of the arguments in a nice format.
    Usage: print_subset_of_args(args, "Title", ["arg1", "arg2", "arg3"])
    """
    print("\n" + color + f'{" " + title + " ":█^{print_length}}')
    for arg in list_of_args:
        print(Colors.BOLD + f'█ {arg + ": ": >{var_length}}' + Colors.END + f'{getattr(args, arg): <{print_length - var_length - 3}}' +  color  + '█')
    print("█" * print_length + Colors.END)

def warn(message: str, color: str = Colors.RED) -> None:
    """
    Prints a warning message in red.
    Usage: warn("This is a warning message")
    """
    print(color + "WARNING: " + message + Colors.END)