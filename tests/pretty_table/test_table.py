import pytest
from prettypi.pretty_table import TableConfig
from prettypi.pretty_table.table import PrettyTable


class TestPrettyTable:

    def test_set_config(self):
        data = [["1", "2", "3"], ["4", "5", "6"]]
        headers = ["A", "B", "C"]
        config = (
            TableConfig.builder()
            .set_border(top="u", bottom="=", left="i")
            .set_column_separator(" }{ ")
            .build()
        )

        pt = PrettyTable(data, headers)
        pt.set_config(config)

        expected = "iuuuuuuuuuuuuu\ni A }{ B }{ C \ni=============\ni 1 }{ 2 }{ 3 \ni-------------\ni 4 }{ 5 }{ 6 \ni-------------"  # noqa

        assert str(pt) == expected

    @pytest.mark.parametrize(
        "data, headers, expected",
        [
            pytest.param(
                [["1", "2", "3"], ["4", "5", "6"]],
                ["A", "B", "C"],
                " A | B | C \n 1 | 2 | 3 \n-----------\n 4 | 5 | 6 \n-----------",
                id="Test with data and headers",
            ),
            pytest.param(
                [["apple", "banana", "cherry"], ["dog", "elephant", "fox"]],
                ["Fruit", "Animal", "Object"],
                " Fruit | Animal   | Object \n apple | banana   | cherry \n---------------------------\n dog   | elephant | fox    \n---------------------------",  # noqa
                id="Test with data and headers 2",
            ),
        ],
    )
    def test_pretty_table_str(self, data, headers, expected):
        pt = PrettyTable(data, headers)
        assert str(pt) == expected
