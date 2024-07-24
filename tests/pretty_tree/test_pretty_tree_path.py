import os
import pytest
from prettypi.pretty_tree import TreePath, Config
from prettypi.utils import Color, Style
import shutil


def create_file(path, names):
    if not isinstance(names, list):
        names = [names]
    for name in names:
        with open(os.path.join(path, name), "w") as f:
            f.write("Hello World")


@pytest.fixture(scope="module", autouse=True)
def create_folders():
    curr_path = os.path.abspath(os.path.dirname(__file__))
    shutil.rmtree(os.path.join(curr_path, "tests_folder"), ignore_errors=True)

    os.makedirs(os.path.join(curr_path, "tests_folder"))
    os.makedirs(os.path.join(curr_path, "tests_folder", "test1"))
    os.makedirs(os.path.join(curr_path, "tests_folder", "test2"))
    os.makedirs(os.path.join(curr_path, "tests_folder", "test1", "test3"))
    os.makedirs(os.path.join(curr_path, "tests_folder", "test1", "test4"))
    os.makedirs(os.path.join(curr_path, "tests_folder", "test2", "test5"))

    create_file(os.path.join(curr_path, "tests_folder"), ["file1.txt", "file2.txt"])
    create_file(
        os.path.join(curr_path, "tests_folder", "test1"), ["file3.txt", "file4.txt"]
    )
    create_file(os.path.join(curr_path, "tests_folder", "test2"), ["file5.txt"])
    create_file(
        os.path.join(curr_path, "tests_folder", "test1", "test3"), ["file6.txt"]
    )
    create_file(
        os.path.join(curr_path, "tests_folder", "test1", "test4"),
        ["file7.txt", "file8.txt", "file9.txt"],
    )

    yield

    shutil.rmtree(os.path.join(curr_path, "tests_folder"), ignore_errors=True)


class TestConfig:
    @pytest.mark.parametrize(
        "args",
        [
            pytest.param({}, id="Test Config with no arguments"),
            pytest.param(
                {"folder_color": Color.RED}, id="Test Config with folder_color"
            ),
            pytest.param(
                {"folder_style": Style.BOLD}, id="Test Config with folder_style"
            ),
            pytest.param({"file_color": Color.RED}, id="Test Config with file_color"),
            pytest.param({"file_style": Style.BOLD}, id="Test Config with file_style"),
            pytest.param(
                {
                    "folder_color": Color.RED,
                    "folder_style": Style.BOLD,
                    "file_color": Color.GREEN,
                    "file_style": Style.UNDERLINE,
                },
                id="Test Config with all arguments",
            ),
            pytest.param(
                {
                    "folder_color": None,
                    "file_color": None,
                    "file_color": None,
                    "file_style": None,
                },
                id="Test Config with None arguments",
            ),
        ],
    )
    def test_init(self, args):
        config = Config(**args)
        assert config.folder_color == args.get("folder_color", None)
        assert config.folder_style == args.get("folder_style", Style.BOLD)
        assert config.file_color == args.get("file_color", None)
        assert config.file_style == args.get("file_style", None)

    @pytest.mark.parametrize(
        "args, expected",
        [
            pytest.param(
                {"folder_color": "Red"},
                "Expected folder_color to be of type Color, got <class 'str'>",
                id="Test Config with invalid folder_color",
            ),
            pytest.param(
                {"folder_style": "Bold"},
                "Expected folder_style to be of type Style, got <class 'str'>",
                id="Test Config with invalid folder_style",
            ),
            pytest.param(
                {"file_color": "Red"},
                "Expected file_color to be of type Color, got <class 'str'>",
                id="Test Config with invalid file_color",
            ),
            pytest.param(
                {"file_style": "Bold"},
                "Expected file_style to be of type Style, got <class 'str'>",
                id="Test Config with invalid file_style",
            ),
        ],
    )
    def test_init_with_invalid_values(self, args, expected):
        with pytest.raises(ValueError) as exc:
            Config(**args)
        assert str(exc.value) == expected


class TestTreePath:
    @pytest.mark.parametrize(
        "path, config",
        [
            pytest.param(
                "tests_folder", Config(), id="Test TreePath with default config"
            ),
            pytest.param(
                "tests_folder",
                Config(folder_color=Color.RED, folder_style=Style.BOLD),
                id="Test TreePath with custom config",
            ),
        ],
    )
    def test_init(self, path, config):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), path)
        tree = TreePath(path, config)
        assert tree.abs_path == os.path.abspath(path)
        assert tree.config == config
        assert tree.color == config.folder_color
        assert tree.style == config.folder_style

    @pytest.mark.parametrize(
        "path, config",
        [
            pytest.param("tests_folder", None, id="Test TreePath with None config"),
            pytest.param("tests_folder", "config", id="Test TreePath with str config"),
            pytest.param("tests_folder", 12, id="Test TreePath with int config"),
        ],
    )
    def test_init_with_invalid_config(self, path, config):
        with pytest.raises(ValueError) as exc:
            TreePath(path, config)
        assert (
            str(exc.value)
            == f"Expected config to be of type Config, got {type(config)}"
        )

    def test_create_tree(self):
        curr_path = os.path.abspath(os.path.dirname(__file__))
        tree = TreePath(os.path.join(curr_path, "tests_folder"))

        assert tree.abs_path == os.path.join(curr_path, "tests_folder")
        assert len(tree.children) == 4
        assert tree.value == "tests_folder"

    @pytest.mark.parametrize(
        "config",
        [
            pytest.param(
                Config(folder_color=Color.RED, folder_style=Style.BOLD),
                id="Test TreePath with custom config",
            ),
            pytest.param(Config(), id="Test TreePath with default config"),
            pytest.param(
                Config(
                    folder_color=Color.RED,
                    folder_style=Style.BOLD,
                    file_color=Color.GREEN,
                    file_style=Style.UNDERLINE,
                ),
                id="Test TreePath with all config",
            ),
        ],
    )
    def test_apply_config(self, config):
        curr_path = os.path.abspath(os.path.dirname(__file__))
        tree = TreePath(os.path.join(curr_path, "tests_folder"), config=config)
        tree._apply_config()

        def check_config(node):
            assert node.color == config.folder_color
            assert node.style == config.folder_style
            for child in node.children:
                if isinstance(child, TreePath):

                    check_config(child)
                else:
                    assert child.color == config.file_color
                    assert child.style == config.file_style

        check_config(tree)

    def test_set_config(self):
        config = Config(folder_color=Color.RED, folder_style=Style.BOLD)
        tree = TreePath(".")
        tree.set_config(config)

        assert tree.config == config

    @pytest.mark.parametrize(
        "config",
        [
            pytest.param("config", id="Test set_config with str config"),
            pytest.param(12, id="Test set_config with int config"),
        ],
    )
    def test_set_config_with_invalid_config(self, config):
        tree = TreePath(".")
        with pytest.raises(ValueError) as exc:
            tree.set_config(config=config)
        assert (
            str(exc.value)
            == f"Expected config to be of type Config, got {type(config)}"
        )

    def test_display(self, capfd):
        curr_path = os.path.abspath(os.path.dirname(__file__))
        tree = TreePath(
            os.path.join(curr_path, "tests_folder"), Config(folder_style=None)
        )
        tree.display()
        out, _ = capfd.readouterr()

        expecteds = [
            "tests_folder",
            "file1.txt",
            "file2.txt",
            "test1",
            "file3.txt",
            "file4.txt",
            "test3",
            "file6.txt",
            "test4",
            "file7.txt",
            "file8.txt",
            "file9.txt",
            "test2",
            "file5.txt",
            "test5",
        ]
        for expected in expecteds:
            assert expected in out
