""" This module contains the StyledStr class.
    You can use this class to create a string with ANSI color and style codes.
"""

from .ansi_codes import Color, Style, BackgroundColor


class StyledStr:
    """This class represents a string with ANSI color and style codes."""

    def __init__(
        self,
        string: str = "",
        color: Color = Color.RESET,
        style: Style = Style.RESET,
        background_color: BackgroundColor = BackgroundColor.RESET,
    ):
        self.string = string
        self.color = color
        self.background_color = background_color
        self.style = style
        self._check_input()

    def _check_input(self):
        if not isinstance(self.string, str):
            raise ValueError(f"Invalid string: {self.string}")
        if not isinstance(self.color, Color):
            raise ValueError(f"Invalid color: {self.color}")
        if not isinstance(self.style, Style):
            raise ValueError(f"Invalid style: {self.style}")
        if not isinstance(self.background_color, BackgroundColor):
            raise ValueError(f"Invalid background color: {self.background_color}")

    def set_color(self, color: Color):
        """Set the color of the string."""
        self.color = color
        self._check_input()

    def set_background_color(self, background_color: Color):
        """Set the background color of the string."""
        self.background_color = background_color
        self._check_input()

    def set_style(self, style: Style):
        """Set the style of the string."""
        self.style = style
        self._check_input()

    def __str__(self):
        parts = []

        if self.color != Color.RESET:
            parts.append(str(self.color))
        if self.style != Style.RESET:
            parts.append(str(self.style))
        if self.background_color != BackgroundColor.RESET:
            parts.append(str(self.background_color))

        if parts:
            return f"{''.join(parts)}{self.string}{Style.RESET}"
        return self.string
