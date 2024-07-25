""" PrettyTable class for creating styled tables."""

from typing import List
from prettypi.pretty_table import TableConfig
from prettypi.pretty_table.utils import JsonRowsManager


class PrettyTable:
    """PrettyTable class for creating styled tables.

    **Features:**

    - Use the PrettyTable class with data and headers to create a styled table.
    - Print the table with the __str__ method.
    - Use the TableConfig class to customize the table.
    - Use the PrettyTable.builder() method to create a TableConfig object.

    :param data: The data to display in the table
    :type data: List[List[str]]
    :param headers: The headers of the table
    :type headers: List[str]
    :param config: The configuration of the table, defaults to TableConfig()
    :type config: TableConfig, optional

    **Example:**

    .. code-block:: python

            from prettypi.pretty_table.table import PrettyTable

            data = [
                ["1", "2", "3"],
                ["4", "5", "6"]
            ]

            headers = ["A", "B", "C"]

            pt = PrettyTable(data, headers)
            print(pt)



    """

    def __init__(
        self,
        data: List[List[str]],
        headers: List[str] = None,
        config: TableConfig = TableConfig(),
    ) -> None:
        self.headers = headers
        self.data = data
        self.config = config
        self.json_rows_manager = JsonRowsManager()
        self.json_rows_manager.init(self.headers, self.data, self.config)
        self.json_rows_manager.process()

    def set_config(self, config: TableConfig):
        """Set the configuration of the table and reprocess the table."""
        self.config = config
        self.json_rows_manager.set_config(config)
        self.json_rows_manager.process()

    def __str__(self) -> str:
        return str(self.json_rows_manager)


# c = TableConfig.builder()\
#     .set_border(top="═", bottom="═", left="│ ", right=" │", data_bottom="═")\
#     .set_column_separator(" ║ ")\
#     .set_row_separator("┈")\
#     .build()


# pt = PrettyTable([["1", "2", "3"], ["4", f"BATEAU TROP BEAU", "6"]],
#  ["AVION", "B", "C"], c)

# print(pt)
