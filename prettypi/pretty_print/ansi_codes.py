""" This module contains the ANSI color and style codes that can be used in the pretty_print """

from enum import Enum


class Color(Enum):
    """This calss contains ANSI color codes that can be used in the pretty print module."""

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"

    def __str__(self):
        return self.value


class BackgroundColor(Enum):
    """This calss contains ANSI color codes that can be used in the pretty print module."""

    BLACK = "\033[40m"
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    MAGENTA = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"
    RESET = "\033[0m"

    def __str__(self):
        return self.value


class Style(Enum):
    """This class contains ANSI style codes that can be used in the pretty print module."""

    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    INVERT = "\033[7m"
    HIDDEN = "\033[8m"
    STRIKETHROUGH = "\033[9m"
    RESET = "\033[0m"

    def __str__(self):
        return self.value
