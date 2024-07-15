""" Test emojis module. """

from prettypi.pretty_print.utils import Emoji


class TestEmojis:

    def test_emojis_print(self, capfd):
        for emoji in Emoji:
            print(emoji)
            captured = capfd.readouterr()
            assert captured.out == f"{emoji}\n"

    def test_emojis_str(self):
        for emoji in Emoji:
            assert str(emoji) == emoji.value

    def test_emojis_print_fstring(self, capfd):
        for emoji in Emoji:
            print(f"{emoji} is an emoji")
            captured = capfd.readouterr()
            assert captured.out == f"{emoji} is an emoji\n"

    def test_emojis_print_format(self, capfd):
        for emoji in Emoji:
            print("{} is an emoji".format(emoji))
            captured = capfd.readouterr()
            assert captured.out == f"{emoji} is an emoji\n"

    def test_emojis_print_percent_format(self, capfd):
        for emoji in Emoji:
            print("%s is an emoji" % emoji)
            captured = capfd.readouterr()
            assert captured.out == f"{emoji} is an emoji\n"
