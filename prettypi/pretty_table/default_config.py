
from prettypi.pretty_table.table import PrettyTable
from prettypi.pretty_table.table_config import TableConfig


class DefaultConfigs:
    """Default configuration for PrettyTable."""
    NO_BORDER = TableConfig.builder().build()
    SIMPLE = TableConfig.builder()\
        .set_border(top="-", bottom="-", left="|", right="|", data_bottom="-")\
        .set_column_separator(" | ")\
        .build()
    SIMPLE_WITH_ROW_SEPARATOR = TableConfig.builder()\
        .set_border(top="-", bottom="-", left="|", right="|")\
        .set_column_separator(" | ")\
        .set_row_separator("-")\
        .build()
    DOUBLE = TableConfig.builder()\
        .set_border(top="═", bottom="═", left="║", right="║", data_bottom="═")\
        .set_column_separator(" ║ ")\
        .build()
    DOUBLE_WITH_ROW_SEPARATOR = TableConfig.builder()\
        .set_border(top="═", bottom="═", left="║", right="║", data_bottom="═")\
        .set_column_separator(" ║ ")\
        .set_row_separator("═")\
        .build()
    DOUBLE_WITH_ROW_SEPARATOR2 = TableConfig.builder()\
        .set_border(top="═", bottom="═", left="║", right="║", data_bottom="═")\
        .set_column_separator(" ║ ")\
        .set_row_separator("┈")\
        .build()
    MARKDOWN = TableConfig.builder()\
        .set_border(top="", bottom="-", left="|", right="|")\
        .set_column_separator(" | ")\
        .build()
    PRETTY_WITHOUT_HEADER = TableConfig.builder()\
        .set_border(top="─", bottom="─", left="│ ", right=" │", data_bottom="─")\
        .set_column_separator(" │ ")\
        .set_row_separator("─")\
        .build()
    PRETTY = TableConfig.builder()\
        .set_border(top="═", bottom="═", left="│ ", right=" │", data_bottom="─")\
        .set_column_separator(" │ ")\
        .set_row_separator("─")\
        .build()

