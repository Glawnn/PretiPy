""" This module contains the StyledStr class.
    You can use this class to create a string with ANSI color and style codes.
"""

from .ansi_codes import Color, Style


class StyledStr:
    """This class represents a string with ANSI color and style codes."""

    def __init__(
        self, string: str = "", color: Color = Color.RESET, style: Style = Style.RESET
    ):
        self.string = string
        self.color = color
        self.style = style
        self._check_input()

    def _check_input(self):
        if not isinstance(self.string, str):
            raise ValueError(f"Invalid string: {self.string}")
        if not isinstance(self.color, Color):
            raise ValueError(f"Invalid color: {self.color}")
        if not isinstance(self.style, Style):
            raise ValueError(f"Invalid style: {self.style}")

    def set_color(self, color: Color):
        """Set the color of the string."""
        self.color = color
        self._check_input()

    def set_style(self, style: Style):
        """Set the style of the string."""
        self.style = style
        self._check_input()

    def __str__(self):
        if self.color == Color.RESET and self.style == Style.RESET:
            return self.string
        if self.color == Color.RESET:
            return f"{self.style}{self.string}{Style.RESET}"
        if self.style == Style.RESET:
            return f"{self.color}{self.string}{Color.RESET}"
        return f"{self.color}{self.style}{self.string}{Style.RESET}{Color.RESET}"
