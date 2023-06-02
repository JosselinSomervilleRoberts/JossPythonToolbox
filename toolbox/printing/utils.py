import os
from typing import List, Union, Optional

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

def str_to_color(color_name: str) -> str:
    """
    Returns the color from the color name.
    Usage: str_to_color("red")
    """
    color_name = color_name.upper()
    return getattr(Colors, color_name)

def str_without_colors(text: str) -> str:
    """
    Returns the string without the color characters.
    """
    white_text = text
    for color in Colors.__dict__.values():
        if isinstance(color, str):
            white_text = white_text.replace(color, "")
    return white_text

def str_len_without_colors(text: str) -> int:
    """
    Returns the actual length of the string without couting the color characters.
    Example: 
    >>> len(Color.RED + "Hello world!" + Color.END)
    23
    >>> str_len_without_colors(Color.RED + "Hello world!" + Color.END)
    12
    """
    # Removes all the color characters
    return len(str_without_colors(text))


def print_color(text: str, color: Optional[Union[str, List[str]]] = None) -> None:
    """
    Prints text in the given color.
    Usage: print_color("Hello world!", "red")
    """
    prefix = ""
    if color is None:
        print(text)
        return
    elif isinstance(color, list):
        for c in color:
            prefix += str_to_color(c)
    else:
        prefix = str_to_color(color)
    print(prefix + text + Colors.END)

def print_centered(text: str, color: Optional[Union[str, List[str]]] = None, width: Optional[int] = None, character: str = "█") -> None:
    """
    Prints text centered in the terminal.
    Usage: print_centered("Hello world!")
    """
    if width is None:
        width = get_terminal_width() - 1
    # Compensate for the color characters
    width += len(text) - str_len_without_colors(text)
    str_color = ""
    if color is not None:
        if not isinstance(color, list):
            color = [color]
        for c in color:
            str_color += str_to_color(c)
    print(str_color + f'{" " + Colors.END + text + str_color + " ":{character}^{width + len(str_color) + len(Colors.END)}}' + Colors.END)

def print_wrapped(text: str, color: Optional[Union[str, List[str]]] = None, width: Optional[int] = None, character: str = "█") -> None:
    """
    Prints text wrapped in the character in the terminal.
    """
    if width is None:
        width = get_terminal_width() - 1
    # Compensate for the color characters
    width += len(text) - str_len_without_colors(text)
    str_color = ""
    if color is not None:
        if not isinstance(color, list):
            color = [color]
        for c in color:
            str_color += str_to_color(c)
    print(str_color + character + Colors.END + f'{" " + text + " ":{" "}<{width - 2}}' + str_color + character + Colors.END)

def print_full_line(character: str = "█") -> None:
    """
    Prints a full line in the terminal.
    Usage: print_full_line()
    """
    width = get_terminal_width() - 1
    print(character * width)


def print_visible(text: Union[str, List[str]]) -> None:
    """
    Prints text in the terminal so that it is visible.
    This is printed with a ton of newlines filled with █, all in dark cyan
    Usage: print_visible("Hello world!")
    """
    width = get_terminal_width() - 1
    print("")
    print_color("█" * width, "darkcyan")
    if not isinstance(text, list):
        text = [text]
    # Seperate for each line
    text_list: List[str] = []
    for t in text:
        text_list += t.split("\n")
    for t in text_list:
        print_wrapped(t, "darkcyan", width)
    print_color("█" * width, "darkcyan")
    print("")
    

def strike(text: str) -> str:
    return ''.join([u'\u0336{}'.format(c) for c in text])

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