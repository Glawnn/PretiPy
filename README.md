# PrettyPi

PretiPy is a Python library for enhancing console output with colorful and style text, emojis, tables, and more.

## Features
- PrettyPrint
  - [x] **Emoji**: Add emojis to your console messages.
  - [x] **Color**: Easily print text in various colors.
  - [x] **Style**: Easily print text with style.
  - [x] **Background Color**: Print text with colored background.
  - [ ] **Alignment**: Support text alignment (left, center, right).
- PrettyTable
  - [ ] **Display**: Create and display tables in the console.
  - [ ] **Custom**: Customize table formatting and styles.
  - [ ] **Template**: Define and use templates for displaying tables.
  - [ ] **Sorting**: Implement sorting functionality for table columns.
  - [ ] **Filtering**: Add filtering capabilities to tables based on user-defined criteria.
  - [ ] **Pagination**: Enable pagination for large datasets displayed in tables.

## Installation
You can install PretiPy using pip:

```bash
pip install prettypi
```

## Usage
Here's a quick example of how to use PrettyPi:

### pretty_print
```python
from prettypi.pretty_print import StyledStr, Color, Style, Emoji

styled_str = StyledStr("Toto", color=Color.RED, style=Style.BOLD)
print(f"My name is {styled_str} {Emoji.SMILE}")
```

