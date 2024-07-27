""" Utils for pretty table """

from typing import List
from prettypi.pretty_table.table_config import Border


class JsonRow:
    """Class to represent a row in the table"""

    def __init__(self, row_type, row_data, border, separator) -> None:
        self.row_type = row_type
        self.row_data = row_data
        if not isinstance(border, Border):
            raise ValueError("border must be an instance of Border")
        self.border = border
        self.separator = separator
        self.row_computed = None

    @staticmethod
    def create_header(row_data: List[str], border: Border, separator: str):
        """Create a header row object

        :param row_data: The data of the row
        :type row_data: List[str]
        :param border: The border of the row
        :type border: Border
        :param separator: The separator of the row
        :type separator: str

        :return: The JsonRow object
        :rtype: JsonRow

        """
        return JsonRow("header", row_data, border, separator)

    @staticmethod
    def create_data(row_data, border, separator):
        """Create a data row object

        :param row_data: The data of the row
        :type row_data: List[str]
        :param border: The border of the row
        :type border: Border
        :param separator: The separator of the row
        :type separator: str

        :return: The JsonRow object
        :rtype: JsonRow

        """
        return JsonRow("data", row_data, border, separator)

    @staticmethod
    def create_separator(border, separator):
        """Create a separator row object

        :param border: The border of the row
        :type border: Border
        :param separator: The separator of the row
        :type separator: str

        :return: The JsonRow object
        :rtype: JsonRow

        """
        border.left = border.left.rstrip()
        border.right = border.right.lstrip()
        return JsonRow("separator", [], border, separator)

    def len_border_left(self):
        """Check the length of the left border

        :return: The length of the left border
        :rtype: int

        """
        return len(self.border.left)

    def len_border_right(self):
        """Check the length of the right border

        :return: The length of the right border
        :rtype: int
        """
        return len(self.border.right)

    def len_columns(self):
        """Check the length of the columns

        :return: The length of the columns
        :rtype: List[int]
        """
        if self.row_data:
            return [len(item) for item in self.row_data]
        return []

    def __str__(self) -> str:
        return f"{self.border.left}, {self.row_data}, {self.border.right}"

    def compute_row_data(self, max_len_left, max_len_right, max_len_columns):
        """Compute the row data

        :param max_len_left: The maximum length of the left border
        :type max_len_left: int
        :param max_len_right: The maximum length of the right border
        :type max_len_right: int
        :param max_len_columns: The maximum length of the columns
        :type max_len_columns: List[int]

        """
        if self.row_type != "separator":
            left = self.border.left.ljust(max_len_left)
            right = self.border.right.ljust(max_len_right)

            columns = [
                item.ljust(max_len_columns[i]) for i, item in enumerate(self.row_data)
            ]
            self.row_computed = f"{left} {self.separator.join(columns)} {right}"

    def compute_row_separator(self, max_len_computed):
        """Compute the row separator

        :param max_len_computed: The maximum length of the computed row
        :type max_len_computed: int

        """
        remove_len = len(self.border.left) + len(self.border.right)
        separator_line = self.separator * (max_len_computed - remove_len)
        self.row_computed = f"{self.border.left}{separator_line}{self.border.right}"


class JsonRowsManager:
    """Class to manage the rows of the table"""

    def __init__(self) -> None:
        self.json_rows = []
        self.max_len_after = 0
        self.max_len_before = 0
        self.max_len_columns = []
        self.data = None
        self.header = None

    def init(self, header, data, config):
        """Initialize the rows of the table

        :param header: The header of the table
        :type header: List[str]
        :param data: The data of the table
        :type data: List[List[str]]
        :param config: The configuration of the table
        :type config: TableConfig
        """
        self.data = data
        self.header = header

        if self.header:
            self._init_header(header, config)
        if self.data:
            self._init_data(self.data, config)
        self._update_max_len()

    def _init_header(self, header, config):
        """Initialize the header of the table"""
        if config.border_header.top:
            self.json_rows.append(
                JsonRow.create_separator(config.border_header, config.border_header.top)
            )
        self.json_rows.append(
            JsonRow.create_header(header, config.border_header, config.column_separator)
        )
        if config.border_header.bottom:
            self.json_rows.append(
                JsonRow.create_separator(
                    config.border_header, config.border_header.bottom
                )
            )

    def _init_data(self, data, config):
        """Initialize the data of the table"""
        for i, row in enumerate(data):
            self.json_rows.append(
                JsonRow.create_data(row, config.border_data, config.column_separator)
            )
            if i == len(data) - 1 and config.border_data.bottom:
                self.json_rows.append(
                    JsonRow.create_separator(
                        config.border_header, config.border_data.bottom
                    )
                )
            elif config.row_separator:
                self.json_rows.append(
                    JsonRow.create_separator(config.border_data, config.row_separator)
                )

    def set_config(self, config):
        """Set the configuration of the table (reset the rows)

        :param config: The configuration of the table
        :type config: TableConfig

        """
        self.json_rows = []
        self.init(self.header, self.data, config)

    def _update_max_len(self):
        if not self.json_rows:
            return
        self.max_len_before = max(len(row.border.left) for row in self.json_rows)
        self.max_len_after = max(len(row.border.right) for row in self.json_rows)

        for row in self.json_rows:
            for i, column in enumerate(row.len_columns()):
                while len(self.max_len_columns) <= i:
                    self.max_len_columns.append(column)

                self.max_len_columns[i] = max(self.max_len_columns[i], column)

    def process(self):
        """Process the rows of the table"""
        # Compute the row with data
        for row in self.json_rows:
            row.compute_row_data(
                self.max_len_before, self.max_len_after, self.max_len_columns
            )

        # Calculate the max length of the computed row
        max_len_computed = max(
            len(row.row_computed)
            for row in self.json_rows
            if row.row_type != "separator"
        )

        # Compute the row with separator
        for row in self.json_rows:
            if row.row_type == "separator":
                row.compute_row_separator(max_len_computed)

    def __str__(self) -> str:
        return "\n".join(row.row_computed for row in self.json_rows)
