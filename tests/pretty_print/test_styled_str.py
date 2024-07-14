import pytest
from prettypi.pretty_print import StyledStr, Color, Style


class TestStyledStr:

    @pytest.mark.parametrize(
        "params",
        [
            pytest.param(
                {"string": "Toto", "color": Color.RED, "style": Style.BOLD},
                id="all param",
            ),
            pytest.param({"color": Color.RED}, id="color param"),
            pytest.param({"style": Style.BOLD}, id="style param"),
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
        styled_str._check_input.assert_called_once()

    @pytest.mark.parametrize(
        "params",
        [
            pytest.param(
                {"string": "Toto", "color": Color.RED, "style": Style.BOLD},
                id="all param",
            ),
            pytest.param({"color": Color.RED}, id="color param"),
            pytest.param({"style": Style.BOLD}, id="style param"),
            pytest.param({"string": "Toto"}, id="Str param"),
            pytest.param({}, id="no param"),
            pytest.param(
                {"string": "Toto", "color": Color.RED}, id="string and color param"
            ),
            pytest.param(
                {"string": "Toto", "style": Style.BOLD}, id="string and style param"
            ),
            pytest.param(
                {"color": Color.RED, "style": Style.BOLD}, id="color and style param"
            ),
        ],
    )
    def test_check_input_valid(self, params):
        styled_str = StyledStr(**params)
        assert styled_str.string == params.get("string", "")
        assert styled_str.color == params.get("color", Color.RESET)
        assert styled_str.style == params.get("style", Style.RESET)

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
                {"color": Color.RED, "style": Style.BOLD},
                f"{Color.RED}{Style.BOLD}{Style.RESET}{Color.RESET}",
                id="color and style param",
            ),
            pytest.param(
                {"string": "Toto", "color": Color.RED, "style": Style.BOLD},
                f"{Color.RED}{Style.BOLD}Toto{Style.RESET}{Color.RESET}",
                id="all param",
            ),
        ],
    )
    def test_str(self, params, expexted):
        styled_str = StyledStr(**params)
        assert str(styled_str) == expexted
