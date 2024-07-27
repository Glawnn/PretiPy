import pytest

from prettypi.pretty_table.utils import JsonRow, Border, JsonRowsManager
from prettypi.pretty_table.table_config import TableConfig


class TestJsonRow:

    def test_instantiate(self):
        row = JsonRow("header", ["a", "b"], Border(), "separator")
        assert row.row_type == "header"
        assert row.row_data == ["a", "b"]
        assert row.border.bottom == ""
        assert row.border.left == ""
        assert row.border.right == ""
        assert row.border.top == ""
        assert row.separator == "separator"
        assert row.row_computed is None

    def test_instantiate_invalid_border(self):
        with pytest.raises(ValueError) as e:
            JsonRow("header", ["a", "b"], "border", "separator")
        assert e.match("border must be an instance of Border")

    def test_create_header(self):
        row = JsonRow.create_header(["a", "b"], Border(), "separator")
        assert row.row_type == "header"
        assert row.row_data == ["a", "b"]
        assert row.border.bottom == ""
        assert row.border.left == ""
        assert row.border.right == ""
        assert row.border.top == ""
        assert row.separator == "separator"
        assert row.row_computed is None

    def test_create_data(self):
        row = JsonRow.create_data(["a", "b"], Border(), "separator")
        assert row.row_type == "data"
        assert row.row_data == ["a", "b"]
        assert row.border.bottom == ""
        assert row.border.left == ""
        assert row.border.right == ""
        assert row.border.top == ""
        assert row.separator == "separator"
        assert row.row_computed is None

    def test_create_separator(self):
        row = JsonRow.create_separator(Border(), "separator")
        assert row.row_type == "separator"
        assert row.row_data == []
        assert row.border.bottom == ""
        assert row.border.left == ""
        assert row.border.right == ""
        assert row.border.top == ""
        assert row.separator == "separator"
        assert row.row_computed is None

    @pytest.mark.parametrize(
        "border, expected",
        [
            pytest.param(Border(), 0, id="default border"),
            pytest.param(Border(left="|"), 1, id="border with one character"),
            pytest.param(Border(left=" "), 1, id="border with space"),
            pytest.param(
                Border(left="| "), 2, id="border with one character left and space"
            ),
            pytest.param(
                Border(left=" |"), 2, id="border with space left and one character"
            ),
            pytest.param(
                Border(left=" | "),
                3,
                id="border with space left, one character and space",
            ),
        ],
    )
    def test_len_border_left(self, border, expected):
        row = JsonRow("header", ["a", "b"], border, "separator")
        assert row.len_border_left() == expected

    @pytest.mark.parametrize(
        "border, expected",
        [
            pytest.param(Border(), 0, id="default border"),
            pytest.param(Border(right="|"), 1, id="border with one character"),
            pytest.param(Border(right=" "), 1, id="border with space"),
            pytest.param(
                Border(right="| "), 2, id="border with one character left and space"
            ),
            pytest.param(
                Border(right=" |"), 2, id="border with space left and one character"
            ),
            pytest.param(
                Border(right=" | "),
                3,
                id="border with space left, one character and space",
            ),
        ],
    )
    def test_len_border_right(self, border, expected):
        row = JsonRow("header", ["a", "b"], border, "separator")
        assert row.len_border_right() == expected

    @pytest.mark.parametrize(
        "data, expected",
        [
            pytest.param([], [], id="empty data"),
            pytest.param(None, [], id="None data"),
            pytest.param(["a"], [1], id="one element"),
            pytest.param(["a", "b"], [1, 1], id="two elements"),
            pytest.param(["a", "bc"], [1, 2], id="two elements with different lengths"),
            pytest.param(
                [" abc", "de ", "t t", " v v "],
                [4, 3, 3, 5],
                id="four elements with different lengths and spaces",
            ),
        ],
    )
    def test_len_columns(self, data, expected):
        row = JsonRow("header", data, Border(), "separator")
        assert row.len_columns() == expected

    @pytest.mark.parametrize(
        "border, expected",
        [
            pytest.param(Border(), ", ['a', 'b'], ", id="default None border"),
            pytest.param(
                Border(left="|"), "|, ['a', 'b'], ", id="border with one character"
            ),
            pytest.param(Border(left=" "), " , ['a', 'b'], ", id="border with space"),
            pytest.param(
                Border(left="| "),
                "| , ['a', 'b'], ",
                id="border with one character left and space",
            ),
            pytest.param(
                Border(left=" |"),
                " |, ['a', 'b'], ",
                id="border with space left and one character",
            ),
            pytest.param(
                Border(left=" | "),
                " | , ['a', 'b'], ",
                id="border with space left, one character and space",
            ),
            pytest.param(
                Border(right="|"), ", ['a', 'b'], |", id="border with one character"
            ),
            pytest.param(Border(right=" "), ", ['a', 'b'],  ", id="border with space"),
            pytest.param(
                Border(right="| "),
                ", ['a', 'b'], | ",
                id="border with one character left and space",
            ),
            pytest.param(
                Border(right=" |"),
                ", ['a', 'b'],  |",
                id="border with space left and one character",
            ),
            pytest.param(
                Border(right=" | "),
                ", ['a', 'b'],  | ",
                id="border with space left, one character and space",
            ),
            pytest.param(
                Border(left="|", right="|"),
                "|, ['a', 'b'], |",
                id="border with one character",
            ),
            pytest.param(
                Border(left=" ", right=" "), " , ['a', 'b'],  ", id="border with space"
            ),
            pytest.param(
                Border(left="| ", right="| "),
                "| , ['a', 'b'], | ",
                id="border with one character left and space",
            ),
            pytest.param(
                Border(left=" |", right=" |"),
                " |, ['a', 'b'],  |",
                id="border with space left and one character",
            ),
        ],
    )
    def test_str(self, border, expected):
        row = JsonRow("header", ["a", "b"], border, "separator")
        assert str(row) == expected

    @pytest.mark.parametrize(
        "row, max_len_left, max_len_right, max_len_columns, expected",
        [
            pytest.param(
                JsonRow.create_data(["1", "2"], Border(), "|"),
                0,
                0,
                [1, 1],
                " 1|2 ",
                id="default 0, 0, 0, 0",
            ),
            pytest.param(
                JsonRow.create_data(["1", "2"], Border(left="|"), "|"),
                1,
                0,
                [1, 1],
                "| 1|2 ",
                id="default |, 0, 0, 0",
            ),
            pytest.param(
                JsonRow.create_data(["1", "2"], Border(right="|"), "|"),
                0,
                1,
                [1, 1],
                " 1|2 |",
                id="default 0, |, 0, 0",
            ),
            pytest.param(
                JsonRow.create_data(["1", "2"], Border(left="|", right="|"), "|"),
                1,
                1,
                [1, 1],
                "| 1|2 |",
                id="default |, |, 0, 0",
            ),
            pytest.param(
                JsonRow.create_data(["1", "2"], Border(left="|", right="|"), "|"),
                1,
                1,
                [3, 4],
                "| 1  |2    |",
                id="max_len_columns 3, 4",
            ),
        ],
    )
    def test_compute_row_data(
        self, row, max_len_left, max_len_right, max_len_columns, expected
    ):
        row.compute_row_data(max_len_left, max_len_right, max_len_columns)
        assert row.row_computed == expected

    @pytest.mark.parametrize(
        "row, max_len_computed, expected",
        [
            pytest.param(
                JsonRow.create_separator(Border(), "-"), 0, "", id="default 0"
            ),
            pytest.param(
                JsonRow.create_separator(Border(left="|"), "-"),
                1,
                "|",
                id="default |, 1",
            ),
            pytest.param(
                JsonRow.create_separator(Border(right="|"), "-"),
                1,
                "|",
                id="default 1, |",
            ),
            pytest.param(
                JsonRow.create_separator(Border(), "-"), 6, "------", id="max_len 6"
            ),
            pytest.param(
                JsonRow.create_separator(Border(left="|"), "-"),
                6,
                "|-----",
                id="max_len 6 and left |",
            ),
            pytest.param(
                JsonRow.create_separator(Border(right="|"), "-"),
                6,
                "-----|",
                id="max_len 6 and right |",
            ),
            pytest.param(
                JsonRow.create_separator(Border(left="|", right="|"), "-"),
                6,
                "|----|",
                id="max_len 6 and left and right |",
            ),
        ],
    )
    def test_compute_row_separator(self, row, max_len_computed, expected):
        row.compute_row_separator(max_len_computed)
        assert row.row_computed == expected


###################
# JsonRowsManager #
###################


class TestTableConfigBuilder:
    def test_instantiate(self):
        manager = JsonRowsManager()
        assert manager.json_rows == []
        assert manager.max_len_after == 0
        assert manager.max_len_before == 0
        assert manager.max_len_columns == []
        assert manager.data is None
        assert manager.header is None

    @pytest.mark.parametrize(
        "header, data",
        [
            pytest.param(["a", "b"], [["1", "2"], ["3", "4"]], id="header and data"),
            pytest.param(["a", "b"], [], id="header and empty data"),
            pytest.param([], [["1", "2"], ["3", "4"]], id="empty header and data"),
            pytest.param([], [], id="empty header and data"),
        ],
    )
    def test_init(self, header, data):
        config = TableConfig.builder().build()
        manager = JsonRowsManager()
        manager.init(header, data, config)
        assert manager.data == data
        assert manager.header == header
        if not header and not data:
            assert manager.json_rows == []
        else:
            assert manager.json_rows != []

    def test_init_header(self):
        config = (
            TableConfig.builder()
            .set_border(top="═", bottom="═", left="│ ", right=" │", data_bottom="═")
            .set_column_separator(" ║ ")
            .set_row_separator("┈")
            .build()
        )
        manager = JsonRowsManager()
        manager._init_header(["a", "b"], config)
        assert len(manager.json_rows) == 3
        assert manager.json_rows[0].row_type == "separator"
        assert manager.json_rows[1].row_type == "header"
        assert manager.json_rows[2].row_type == "separator"

    def test_init_data(self):
        config = (
            TableConfig.builder()
            .set_border(top="═", bottom="═", left="│ ", right=" │", data_bottom="═")
            .set_column_separator(" ║ ")
            .set_row_separator("┈")
            .build()
        )
        manager = JsonRowsManager()
        manager._init_data([["1", "2"], ["3", "4"]], config)
        assert len(manager.json_rows) == 4
        assert manager.json_rows[0].row_type == "data"
        assert manager.json_rows[1].row_type == "separator"
        assert manager.json_rows[2].row_type == "data"
        assert manager.json_rows[3].row_type == "separator"

    def test_set_config(self, mocker):
        config = TableConfig.builder().build()
        manager = JsonRowsManager()
        mocker.patch.object(manager, "init")
        manager.set_config(config)
        assert manager.init.call_count == 1

    def test_update_max_len(self):
        manager = JsonRowsManager()
        manager.json_rows = [
            JsonRow("header", ["a", "b"], Border(left="|"), "separator")
        ]
        manager._update_max_len()
        assert manager.max_len_before == 1
        assert manager.max_len_after == 0
        assert manager.max_len_columns == [1, 1]

    def test_process(self):
        manager = JsonRowsManager()
        manager.init(["a", "b"], [["1", "2"]], TableConfig.builder().build())
        manager.process()
        assert manager.json_rows[0].row_computed == " a | b "
        assert manager.json_rows[1].row_computed == " 1 | 2 "
        assert manager.json_rows[2].row_computed == "-------"

    def test_str(self):
        manager = JsonRowsManager()
        manager.init(["a", "b"], [["1", "2"]], TableConfig.builder().build())
        manager.process()
        assert str(manager) == " a | b \n 1 | 2 \n-------"
