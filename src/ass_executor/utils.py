from __future__ import annotations

import os
import re
from pathlib import Path

from rich.text import Text
from rich.tree import Tree


def replace_environment_variable(input_string: str) -> str:
    """Returns the `input_string` with all occurrences of ENV['var'] expanded.

    >>> replace_environment_variable("ENV['HOME']/data/CSL")
    '/Users/rik/data/CSL'

    Args:
        input_string (str): the string to replace
    Returns:
        The input string with the ENV['var'] replaced, or None when the environment variable
        doesn't exists.
    """

    match = re.search(r"(.*)ENV\[['\"](\w+)['\"]\](.*)", input_string)
    if not match:
        return input_string
    pre_match, var, post_match = match[1], match[2], match[3]

    result = os.getenv(var, None)

    return pre_match + result + post_match if result else None


def walk_dict_tree(dictionary: dict, tree: Tree, text_style: str = "green"):
    """
    Walk recursively through the dictionary and add all nodes to the given tree.
    The tree is a Rich Tree object.
    """
    for k, v in dictionary.items():
        if isinstance(v, dict):
            branch = tree.add(f"[purple]{k}", style="", guide_style="dim")
            walk_dict_tree(v, branch, text_style=text_style)
        else:
            text = Text.assemble((str(k), "medium_purple1"), ": ", (str(v), text_style))
            tree.add(text)


def expand_path(path: Path | str) -> Path:
    """
    Returns the expanded absolute path.

    Args:
        path: a string representing a path segment or a Path

    Returns:
        An absolute path.
    """
    path = replace_environment_variable(str(path))
    path = Path(path).expanduser()

    return path.resolve()


def get_file_path(path: str | Path, name: str) -> Path:
    full_path = expand_path(path)
    if not full_path.exists():
        raise ValueError(f"The path '{full_path}' was expanded into '{path}' which doesn't exist.")

    filepath = full_path / name
    if not filepath.exists():
        raise ValueError(f"The generated filepath '{filepath}' doesn't exit for command script {name}")

    return filepath


def remove_ansi_escape(line):
    """
    Returns a new line where all ANSI escape sequences are removed.
    """
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)
