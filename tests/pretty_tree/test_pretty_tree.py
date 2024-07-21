import pytest
from prettypi.pretty_tree import TreeNode
from prettypi.utils import Color, Style


class TestTreeNode:
    @pytest.mark.parametrize(
        "args",
        [
            pytest.param({}, id="Test TreeNode with no arguments"),
            pytest.param({"value": "Root"}, id="Test TreeNode with value"),
            pytest.param(
                {"value": "Root", "color": Color.RED},
                id="Test TreeNode with value and color",
            ),
            pytest.param(
                {"value": "Root", "style": Style.BOLD},
                id="Test TreeNode with value and style",
            ),
            pytest.param(
                {"value": "Root", "color": Color.RED, "style": Style.BOLD},
                id="Test TreeNode with value, color and style",
            ),
        ],
    )
    def test_init(self, args):
        node = TreeNode(**args)
        assert node.value == args.get("value", "")
        assert node.color == args.get("color", None)
        assert node.style == args.get("style", None)

    def test_add_child(self):
        root = TreeNode("Root")
        child1 = TreeNode("Child1", color=Color.GREEN, style=Style.UNDERLINE)
        childchild1 = TreeNode("Child1.1")
        child1.add_child(childchild1)
        root.add_child(child1)
        assert root.children == [child1]
        assert root.children[0].children == [childchild1]

    def test_add_unsupported_child(self):
        root = TreeNode("Root")
        with pytest.raises(TypeError) as exc:
            root.add_child("Child")
        assert str(exc.value) == "child must be of type TreeNode or list[TreeNode]"

    def test_set_color(self):
        root = TreeNode("Root")
        root.set_color(Color.RED)
        assert root.color == Color.RED

    def test_unsupported_color(self):
        root = TreeNode("Root")
        with pytest.raises(ValueError) as exc:
            root.set_color("Red")
        assert str(exc.value) == "Invalid color"

    def test_set_style(self):
        root = TreeNode("Root")
        root.set_style(Style.BOLD)
        assert root.style == Style.BOLD

    def test_unsupported_style(self):
        root = TreeNode("Root")
        with pytest.raises(ValueError) as exc:
            root.set_style("Bold")
        assert str(exc.value) == "Invalid style"

    @pytest.mark.parametrize(
        "color, style, expected",
        [
            pytest.param(
                None, None, "Root", id="Test TreeNode with no color and style"
            ),
            pytest.param(
                Color.RED,
                None,
                f"{Color.RED}Root{Color.RESET}",
                id="Test TreeNode with color and no style",
            ),
            pytest.param(
                None,
                Style.BOLD,
                f"{Style.BOLD}Root{Style.RESET}",
                id="Test TreeNode with no color and style",
            ),
            pytest.param(
                Color.RED,
                Style.BOLD,
                f"{Color.RED}{Style.BOLD}Root{Style.RESET}",
                id="Test TreeNode with color and style",
            ),
        ],
    )
    def test_compute_value(self, color, style, expected):
        root = TreeNode("Root", color=color, style=style)
        assert root._compute_value() == expected

    @pytest.mark.parametrize(
        "prefix, is_last, expected",
        [
            pytest.param(
                "",
                False,
                "├──Root\n",
                id="Test display_tree with no prefix and not last",
            ),
            pytest.param(
                "", True, "└──Root\n", id="Test display_tree with no prefix and last"
            ),
            pytest.param(
                "│   ",
                False,
                "│   ├──Root\n",
                id="Test display_tree with prefix and not last",
            ),
            pytest.param(
                "│   ",
                True,
                "│   └──Root\n",
                id="Test display_tree with prefix and last",
            ),
        ],
    )
    def test_display_tree(self, prefix, is_last, expected, capfd):
        root = TreeNode("Root")
        root._display_tree(prefix, is_last)
        out, _ = capfd.readouterr()
        assert out == expected

    def test_display_tree_with_children(self, capfd):
        root = TreeNode("Root")
        child1 = TreeNode("Child1")
        child2 = TreeNode("Child2")
        root.add_child(child1)
        root.add_child(child2)
        root.display()
        out, _ = capfd.readouterr()
        expected = "Root\n├──Child1\n└──Child2\n"
        assert out == expected
