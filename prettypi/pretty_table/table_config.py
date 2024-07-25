""" This module contains the TableConfig class and TableConfigBuilder class. """

from dataclasses import dataclass


@dataclass
class Border:
    """Class to represent the borders of the table."""

    top: str = ""
    bottom: str = ""
    left: str = ""
    right: str = ""


class TableConfig:
    """Class to represent the configuration of the table.

    With builder method, you can create a TableConfig object with the desired configuration.
    Check the TableConfigBuilder class for more information.

    """

    def __init__(self, **kwargs) -> None:  # pylint: disable=too-many-arguments
        self.border_header = kwargs.get(
            "border_header", Border(top="", bottom="", left="", right="")
        )
        self.border_data = kwargs.get("border_data", Border(left="", right=""))
        self.column_separator = kwargs.get("column_separator", " | ")
        self.row_separator = kwargs.get("row_separator", "-")
        self.alignment_default = kwargs.get("alignment", "left")
        self.alignments = kwargs.get("alignments", [])

    def get_config(self):
        """Get the configuration of the table.

        :return: The configuration of the table
        :rtype: dict

        """
        return vars(self)

    @staticmethod
    def builder():
        """Create a TableConfigBuilder object to build a TableConfig object
        with the desired configuration.
        """
        return TableConfigBuilder()


class TableConfigBuilder:
    """ Class to build a TableConfig object with the desired configuration.

    **Example:**

    .. code-block:: python

            from prettypi.pretty_table.table_config import TableConfigBuilder

            config = TableConfigBuilder()\
                .set_border(top="═", bottom="═", left="│ ", right=" │", data_bottom="═")\
                .set_column_separator(" ║ ")\
                .set_row_separator("┈")\
                .build()

    """

    def __init__(self) -> None:
        self.border_header = Border()
        self.border_data = Border()
        self.column_separator = " | "
        self.row_separator = "-"
        self.alignment_default = "left"
        self.alignments = []

    def set_border(
        self, top="", bottom="", left="", right="", data_bottom=""
    ):  # pylint: disable=too-many-arguments
        """Set the border of the table.

        :param top: The top border of the table, defaults to ""
        :type top: str, optional
        :param bottom: The bottom border of the table, defaults to ""
        :type bottom: str, optional
        :param left: The left border of the table, defaults to ""
        :type left: str, optional
        :param right: The right border of the table, defaults to ""
        :type right: str, optional
        :param data_bottom: The bottom border of the data rows, defaults to ""
        :type data_bottom: str, optional

        :return: The TableConfigBuilder object
        :rtype: TableConfigBuilder

        """
        self.border_header = Border(top, bottom, left, right)
        self.border_data = Border(left=left, right=right, bottom=data_bottom)
        return self

    def set_column_separator(self, column_separator):
        """Set the column separator of the table.

        :param column_separator: The column separator of the table
        :type column_separator: str

        :return: The TableConfigBuilder object
        :rtype: TableConfigBuilder
        """
        self.column_separator = column_separator
        return self

    def set_row_separator(self, row_separator):
        """Set the row separator of the table.

        :param row_separator: The row separator of the table
        :type row_separator: str

        :return: The TableConfigBuilder object
        :rtype: TableConfigBuilder

        """
        self.row_separator = row_separator
        return self

    def build(self):
        """Build a TableConfig object with the desired configuration.

        :return: The TableConfig object
        :rtype: TableConfig

        """
        return TableConfig(
            border_header=self.border_header,
            border_data=self.border_data,
            column_separator=self.column_separator,
            row_separator=self.row_separator,
            alignment=self.alignment_default,
            alignments=self.alignments,
        )
