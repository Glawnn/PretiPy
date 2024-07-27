import pytest
from prettypi._version import __version__
import requests
from packaging.version import Version


@pytest.fixture
def version_on_pypi():
    response = requests.get("https://pypi.org/pypi/prettypi/json")
    response.raise_for_status()
    data = response.json()
    return data["info"]["version"]


class TestVersion:
    def test_version_bigger_than_pypi(self, version_on_pypi):
        assert Version(__version__) > Version(version_on_pypi)
