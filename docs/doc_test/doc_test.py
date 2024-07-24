""" Lib to extract docstrings and code blocks from a python file and execute them """

import ast
import io
import os
import re
import sys
import traceback
import black
import argparse

from prettypi.utils import Color


def extract_docstring(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read())

    return [
        ast.get_docstring(node)
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module))
    ]


def extract_code(docstrings):
    formated_code_blocks = []
    for docstring in docstrings:
        if not docstring:
            continue

        code_blocks = re.findall(
            r"\.\. code-block:: python\n\n(?: {4}|\t)([^\n]+(?:\n(?: {4}|\t)[^\n]+)*)",
            docstring,
            re.MULTILINE,
        )
        code_blocks = [block.replace("    ", "") for block in code_blocks]

        for code_block in code_blocks:
            formated_code_blocks.append(black.format_str(code_block, mode=black.Mode()))

    code = "\n".join(formated_code_blocks)
    code = black.format_str(code, mode=black.Mode())

    return code


def execute_code_block(code_block):
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    new_stdout = io.StringIO()
    new_stderr = io.StringIO()

    sys.stdout = new_stdout
    sys.stderr = new_stderr
    try:
        local_vars = {}
        global_vars = {}
        exec(code_block, global_vars, local_vars)
    except Exception as e:
        raise e
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        help="Path to the file to extract the docstrings and code blocks",
        type=str,
        nargs="?",
        default=os.getcwd(),
    )
    args = parser.parse_args()

    data = {}

    for root, _, files in os.walk(args.path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    dt = extract_docstring(file_path)
                    code = extract_code(dt)
                    execute_code_block(code)
                except Exception as e:
                    print(f"{file_path} {Color.RED}KO{Color.RESET}")
                    error_message = traceback.format_exc()
                    data[file_path] = {"error": str(e), "traceback": error_message}
                print(f"{file_path} {Color.GREEN}OK{Color.RESET}")

    for elem in data:
        print("=========================================")
        print(f"{Color.RED}{elem}{Color.RESET}")
        print(data[elem]["traceback"])
        print("=========================================")

    if data != {}:
        sys.exit(1)


if __name__ == "__main__":
    main()
