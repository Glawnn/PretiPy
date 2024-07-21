import pytest
from prettypi.pretty_print import StyledStr
from prettypi.utils import Color, Style, BackgroundColor, Align


class TestStyledStr:

    @pytest.mark.parametrize(
        "params",
        [
            pytest.param(
                {
                    "string": "Toto",
                    "color": Color.RED,
                    "style": Style.BOLD,
                    "background_color": BackgroundColor.GREEN,
                },
                id="all param",
            ),
            pytest.param({"color": Color.RED}, id="color param"),
            pytest.param({"style": Style.BOLD}, id="style param"),
            pytest.param(
                {"background_color": BackgroundColor.GREEN}, id="background_color param"
            ),
            pytest.param({"string": "Toto"}, id="Str param"),
            pytest.param({}, id="no param"),
        ],
    )
    def test_init(self, params, mocker):
        mocker.patch("prettypi.pretty_print.styled_str.StyledStr._check_input")
        styled_str = StyledStr(**params)
        assert styled_str.string == params.get("string", "")
        assert styled_str.color == params.get("color", Color.RESET)
        assert styled_str.style == params.get("style", Style.RESET)
        assert styled_str.background_color == params.get(
            "background_color", BackgroundColor.RESET
        )
        styled_str._check_input.assert_called_once()

    @pytest.mark.parametrize(
        "params",
        [
            pytest.param(
                {
                    "string": "Toto",
                    "color": Color.RED,
                    "style": Style.BOLD,
                    "background_color": BackgroundColor.GREEN,
                },
                id="all param",
            ),
            pytest.param({"color": Color.RED}, id="color param"),
            pytest.param({"style": Style.BOLD}, id="style param"),
            pytest.param(
                {"background_color": BackgroundColor.GREEN}, id="background_color param"
            ),
            pytest.param({"string": "Toto"}, id="Str param"),
            pytest.param({}, id="no param"),
            pytest.param(
                {"string": "Toto", "color": Color.RED}, id="string and color param"
            ),
            pytest.param(
                {"string": "Toto", "style": Style.BOLD}, id="string and style param"
            ),
            pytest.param(
                {"string": "Toto", "background_color": BackgroundColor.GREEN},
                id="string and background_color param",
            ),
            pytest.param(
                {"color": Color.RED, "style": Style.BOLD}, id="color and style param"
            ),
            pytest.param(
                {"color": Color.RED, "background_color": BackgroundColor.GREEN},
                id="color and background_color param",
            ),
            pytest.param(
                {"style": Style.BOLD, "background_color": BackgroundColor.GREEN},
                id="style and background_color param",
            ),
        ],
    )
    def test_check_input_valid(self, params):
        styled_str = StyledStr(**params)
        assert styled_str.string == params.get("string", "")
        assert styled_str.color == params.get("color", Color.RESET)
        assert styled_str.style == params.get("style", Style.RESET)
        assert styled_str.background_color == params.get(
            "background_color", BackgroundColor.RESET
        )

    @pytest.mark.parametrize(
        "params, expected",
        [
            pytest.param(
                {
                    "string": 1,
                },
                "Invalid string: 1",
                id="int string param",
            ),
            pytest.param(
                {
                    "color": "RED",
                },
                "Invalid color: RED",
                id="str color param",
            ),
            pytest.param(
                {"string": "Toto", "color": "RED"},
                "Invalid color: RED",
                id="valid string and str color param",
            ),
            pytest.param(
                {
                    "style": "BOLD",
                },
                "Invalid style: BOLD",
                id="str style param",
            ),
            pytest.param(
                {"string": "Toto", "style": "BOLD"},
                "Invalid style: BOLD",
                id="valid string and str style param",
            ),
            pytest.param(
                {"string": 1, "color": "RED"},
                "Invalid string: 1",
                id="int string and str color param",
            ),
            pytest.param(
                {"string": 1, "style": "BOLD"},
                "Invalid string: 1",
                id="int string and str style param",
            ),
            pytest.param(
                {"color": "RED", "style": "BOLD"},
                "Invalid color: RED",
                id="str color and str style param",
            ),
            pytest.param(
                {"string": 1, "color": "RED", "style": "BOLD"},
                "Invalid string: 1",
                id="int string and str color and str style param",
            ),
            pytest.param(
                {"background_color": "GREEN"},
                "Invalid background color: GREEN",
                id="str background_color param",
            ),
            pytest.param(
                {"string": "Toto", "background_color": "GREEN"},
                "Invalid background color: GREEN",
                id="valid string and str background_color param",
            ),
        ],
    )
    def test_check_input_invalid(self, params, expected):
        with pytest.raises(ValueError) as e:
            StyledStr(**params)
        assert str(e.value) == expected

    def test_set_color(self):
        styled_str = StyledStr()
        styled_str.set_color(Color.RED)
        assert styled_str.color == Color.RED

    def test_set_invalid_color(self):
        styled_str = StyledStr()
        with pytest.raises(ValueError) as e:
            styled_str.set_color("RED")
        assert str(e.value) == "Invalid color: RED"

    def test_set_style(self):
        styled_str = StyledStr()
        styled_str.set_style(Style.BOLD)
        assert styled_str.style == Style.BOLD

    def test_set_invalid_style(self):
        styled_str = StyledStr()
        with pytest.raises(ValueError) as e:
            styled_str.set_style("BOLD")
        assert str(e.value) == "Invalid style: BOLD"

    def test_set_background_color(self):
        styled_str = StyledStr()
        styled_str.set_background_color(BackgroundColor.GREEN)
        assert styled_str.background_color == BackgroundColor.GREEN

    def test_set_invalid_background_color(self):
        styled_str = StyledStr()
        with pytest.raises(ValueError) as e:
            styled_str.set_background_color("GREEN")
        assert str(e.value) == "Invalid background color: GREEN"

    def test_set_align(self):
        styled_str = StyledStr()
        styled_str.set_align(Align.CENTER, 10)
        assert styled_str.align == (Align.CENTER, 10)

    def test_set_invalid_align(self):
        styled_str = StyledStr()
        with pytest.raises(ValueError) as e:
            styled_str.set_align("CENTER", 12)
        assert str(e.value) == "Invalid align: ('CENTER', 12)"

    @pytest.mark.parametrize(
        "params, expexted",
        [
            pytest.param({}, "", id="no param"),
            pytest.param({"string": "Toto"}, "Toto", id="string param"),
            pytest.param(
                {"color": Color.RED}, f"{Color.RED}{Color.RESET}", id="color param"
            ),
            pytest.param(
                {"string": "Toto", "color": Color.RED},
                f"{Color.RED}Toto{Color.RESET}",
                id="string and color param",
            ),
            pytest.param(
                {"style": Style.BOLD}, f"{Style.BOLD}{Style.RESET}", id="style param"
            ),
            pytest.param(
                {"string": "Toto", "style": Style.BOLD},
                f"{Style.BOLD}Toto{Style.RESET}",
                id="string and style param",
            ),
            pytest.param(
                {"background_color": BackgroundColor.GREEN},
                f"{BackgroundColor.GREEN}{BackgroundColor.RESET}",
                id="background_color param",
            ),
            pytest.param(
                {"string": "Toto", "background_color": BackgroundColor.GREEN},
                f"{BackgroundColor.GREEN}Toto{BackgroundColor.RESET}",
                id="string and background_color param",
            ),
            pytest.param(
                {"color": Color.RED, "style": Style.BOLD},
                f"{Color.RED}{Style.BOLD}{Style.RESET}",
                id="color and style param",
            ),
            pytest.param(
                {"color": Color.RED, "background_color": BackgroundColor.GREEN},
                f"{Color.RED}{BackgroundColor.GREEN}{Color.RESET}",
                id="color and background_color param",
            ),
            pytest.param(
                {"style": Style.BOLD, "background_color": BackgroundColor.GREEN},
                f"{Style.BOLD}{BackgroundColor.GREEN}{Style.RESET}",
                id="style and background_color param",
            ),
            pytest.param(
                {
                    "string": "Toto",
                    "color": Color.RED,
                    "style": Style.BOLD,
                    "background_color": BackgroundColor.GREEN,
                },
                f"{Color.RED}{Style.BOLD}{BackgroundColor.GREEN}Toto{Style.RESET}",
                id="all param",
            ),
        ],
    )
    def test_str(self, params, expexted):
        styled_str = StyledStr(**params)
        assert str(styled_str) == expexted

    @pytest.mark.parametrize(
        "params, align, expected",
        [
            pytest.param(
                {"string": "Toto"},
                {"align": Align.LEFT, "width": 10},
                "Toto      ",
                id="left align",
            ),
            pytest.param(
                {"string": "Toto"},
                {"align": Align.RIGHT, "width": 10},
                "      Toto",
                id="right align",
            ),
            pytest.param(
                {"string": "Toto"},
                {"align": Align.CENTER, "width": 10},
                "   Toto   ",
                id="center align",
            ),
            pytest.param(
                {"string": "Toto", "color": Color.RED},
                {"align": Align.LEFT, "width": 10},
                f"{Color.RED}Toto      {Color.RESET}",
                id="color and left align",
            ),
            pytest.param(
                {"string": "Toto", "color": Color.RED},
                {"align": Align.RIGHT, "width": 10},
                f"{Color.RED}      Toto{Color.RESET}",
                id="color and right align",
            ),
            pytest.param(
                {"string": "Toto", "color": Color.RED},
                {"align": Align.CENTER, "width": 10},
                f"{Color.RED}   Toto   {Color.RESET}",
                id="color and center align",
            ),
            pytest.param(
                {
                    "string": "Toto",
                    "style": Style.BOLD,
                    "background_color": BackgroundColor.GREEN,
                },
                {"align": Align.LEFT, "width": 10},
                f"{Style.BOLD}{BackgroundColor.GREEN}Toto      {Style.RESET}",
                id="style and background_color and left align",
            ),
            pytest.param(
                {
                    "string": "Toto",
                    "style": Style.BOLD,
                    "background_color": BackgroundColor.GREEN,
                },
                {"align": Align.RIGHT, "width": 10},
                f"{Style.BOLD}{BackgroundColor.GREEN}      Toto{Style.RESET}",
                id="style and background_color and right align",
            ),
            pytest.param(
                {
                    "string": "Toto",
                    "style": Style.BOLD,
                    "background_color": BackgroundColor.GREEN,
                },
                {"align": Align.CENTER, "width": 10},
                f"{Style.BOLD}{BackgroundColor.GREEN}   Toto   {Style.RESET}",
                id="style and background_color and center align",
            ),
        ],
    )
    def test_str_with_align(self, params, align, expected):
        styled_str = StyledStr(**params)
        styled_str.set_align(**align)
        assert str(styled_str) == expected
