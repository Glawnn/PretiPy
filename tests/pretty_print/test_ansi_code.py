""" Test ansi module. """

from prettypi.pretty_print import Color, Style


class TestColor:

    def test_color_print(self, capfd):
        for color in Color:
            print(color)
            captured = capfd.readouterr()
            assert captured.out == f"{color}\n"

    def test_color_str(self):
        for color in Color:
            assert str(color) == color.value

    def test_color_print_fstring(self, capfd):
        for color in Color:
            print(f"{color} is an color")
            captured = capfd.readouterr()
            assert captured.out == f"{color} is an color\n"

    def test_color_print_format(self, capfd):
        for color in Color:
            print("{} is an color".format(color))
            captured = capfd.readouterr()
            assert captured.out == f"{color} is an color\n"

    def test_color_print_percent_format(self, capfd):
        for color in Color:
            print("%s is an color" % color)
            captured = capfd.readouterr()
            assert captured.out == f"{color} is an color\n"


class TestStyle:

    def test_style_print(self, capfd):
        for style in Style:
            print(style)
            captured = capfd.readouterr()
            assert captured.out == f"{style}\n"

    def test_style_str(self):
        for style in Style:
            assert str(style) == style.value

    def test_style_print_fstring(self, capfd):
        for style in Style:
            print(f"{style} is an style")
            captured = capfd.readouterr()
            assert captured.out == f"{style} is an style\n"

    def test_style_print_format(self, capfd):
        for style in Style:
            print("{} is an style".format(style))
            captured = capfd.readouterr()
            assert captured.out == f"{style} is an style\n"

    def test_style_print_percent_format(self, capfd):
        for style in Style:
            print("%s is an style" % style)
            captured = capfd.readouterr()
            assert captured.out == f"{style} is an style\n"
