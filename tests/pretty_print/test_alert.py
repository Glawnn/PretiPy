import pytest
from prettypi.pretty_print import Alert
from prettypi.utils import Emoji


class TestAlert:
    @pytest.mark.parametrize(
        "args",
        [
            pytest.param({}, id="Test Alert with no arguments"),
            pytest.param({"message": "This is an alert"}, id="Test Alert with message"),
            pytest.param(
                {"message": "This is an alert", "prefix": Emoji.WARNING},
                id="Test Alert with message and prefix",
            ),
            pytest.param(
                {
                    "message": "This is an alert",
                    "prefix": "+",
                    "surround_prefix": "[,]",
                },
                id="Test Alert with message, prefix and surround_prefix",
            ),
        ],
    )
    def test_init(self, args):
        alert = Alert(**args)
        assert alert.message == args.get("message", "")
        assert alert.prefix == args.get("prefix", Emoji.BULB)
        assert alert.surround_prefix == args.get("surround_prefix", " ,")

    @pytest.mark.parametrize(
        "surround_prefix, expected",
        [
            pytest.param(",", None, id="Test Alert with comma without surround"),
            pytest.param(" ,", None, id="Test Alert with left space"),
            pytest.param(", ", None, id="Test Alert with right space"),
            pytest.param("[,]", None, id="Test Alert with left and right brackets"),
            pytest.param("[]", ValueError, id="Test Alert with no comma"),
            pytest.param("", ValueError, id="Test Alert blank string"),
            pytest.param(",,", ValueError, id="Test Alert with two commas"),
            pytest.param(None, ValueError, id="Test Alert with None"),
        ],
    )
    def test_check_surround_prefix(self, surround_prefix, expected):
        if expected:
            with pytest.raises(ValueError) as exc:
                alert = Alert(surround_prefix=surround_prefix)
            assert str(exc.value) == "surround_prefix must be of the form 'left,right'"
        else:
            alert = Alert(surround_prefix=surround_prefix)
            assert alert.surround_prefix == surround_prefix

    @pytest.mark.parametrize(
        "args, expected",
        [
            pytest.param({}, f" {Emoji.BULB} ", id="Test Alert with no arguments"),
            pytest.param(
                {"message": "This is an alert"},
                f" {Emoji.BULB} This is an alert",
                id="Test Alert with message",
            ),
            pytest.param(
                {"message": "This is an alert", "prefix": Emoji.WARNING},
                f" {Emoji.WARNING} This is an alert",
                id="Test Alert with message and prefix",
            ),
            pytest.param(
                {
                    "message": "This is an alert",
                    "prefix": "+",
                    "surround_prefix": " [,]",
                },
                " [+] This is an alert",
                id="Test Alert with message, prefix and surround_prefix",
            ),
        ],
    )
    def test_str(self, args, expected):
        alert = Alert(**args)
        assert str(alert) == expected

    @pytest.mark.parametrize(
        "args, expected",
        [
            pytest.param({}, f" {Emoji.BULB} ", id="Test Alert with no arguments"),
            pytest.param(
                {"message": "This is an alert"},
                f" {Emoji.BULB} This is an alert",
                id="Test Alert with message",
            ),
            pytest.param(
                {"message": "This is an alert", "surround_prefix": " [,]"},
                f" [{Emoji.BULB}] This is an alert",
                id="Test Alert with message and surround_prefix",
            ),
        ],
    )
    def test_info(self, args, expected):
        alert = Alert.info(**args)
        assert str(alert) == expected

    @pytest.mark.parametrize(
        "args, expected",
        [
            pytest.param({}, f" {Emoji.WARNING} ", id="Test Alert with no arguments"),
            pytest.param(
                {"message": "This is an alert"},
                f" {Emoji.WARNING} This is an alert",
                id="Test Alert with message",
            ),
            pytest.param(
                {"message": "This is an alert", "surround_prefix": " [,]"},
                f" [{Emoji.WARNING}] This is an alert",
                id="Test Alert with message and surround_prefix",
            ),
        ],
    )
    def test_warning(self, args, expected):
        alert = Alert.warning(**args)
        assert str(alert) == expected

    @pytest.mark.parametrize(
        "args, expected",
        [
            pytest.param({}, f" {Emoji.CROSS} ", id="Test Alert with no arguments"),
            pytest.param(
                {"message": "This is an alert"},
                f" {Emoji.CROSS} This is an alert",
                id="Test Alert with message",
            ),
            pytest.param(
                {"message": "This is an alert", "surround_prefix": " [,]"},
                f" [{Emoji.CROSS}] This is an alert",
                id="Test Alert with message and surround_prefix",
            ),
        ],
    )
    def test_error(self, args, expected):
        alert = Alert.error(**args)
        assert str(alert) == expected

    @pytest.mark.parametrize(
        "args, expected",
        [
            pytest.param({}, f" {Emoji.CHECK} ", id="Test Alert with no arguments"),
            pytest.param(
                {"message": "This is an alert"},
                f" {Emoji.CHECK} This is an alert",
                id="Test Alert with message",
            ),
            pytest.param(
                {"message": "This is an alert", "surround_prefix": " [,]"},
                f" [{Emoji.CHECK}] This is an alert",
                id="Test Alert with message and surround_prefix",
            ),
        ],
    )
    def test_success(self, args, expected):
        alert = Alert.success(**args)
        assert str(alert) == expected
