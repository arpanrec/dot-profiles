"""
This module parses conf.yaml
"""

from __future__ import annotations

import os
import re
from collections.abc import Callable
from typing import Any

from .config import Config
from .consts import BIN_DIR, CONFIG_DIR, DOT_PROFILES_DIR, HOME, PROFILES_DIR, SHARE_DIR


def _find_directory(grouped_regex: str, path: str, matches: Callable[[str, str], bool]) -> str:
    """Finds the first folder whose name satisfies `matches` against the text in the regex's second group.

    Args:
        grouped_regex: regex of the function
        path: path
        matches: predicate taking a directory name and the text to compare it with
    """
    found = re.search(grouped_regex, path)
    if found is None:
        return path
    occurence = found.group()
    dirs = os.listdir(path[0 : path.find(occurence)])
    inner = re.search(grouped_regex, occurence)
    if inner is None:
        return occurence
    text = inner.group(2)
    for directory in dirs:
        if matches(directory, text):
            return path.replace(occurence, directory)
    return occurence


def ends_with(grouped_regex: str, path: str) -> str:
    """Finds folder with name ending with the provided string.

    Args:
        grouped_regex: regex of the function
        path: path
    """
    return _find_directory(grouped_regex, path, str.endswith)


def begins_with(grouped_regex: str, path: str) -> str:
    """Finds folder with name beginning with the provided string.

    Args:
        grouped_regex: regex of the function
        path: path
    """
    return _find_directory(grouped_regex, path, str.startswith)


def parse_keywords(tokens_: dict[str, Any], token_symbol: str, parsed: Config) -> None:
    """Replaces keywords with values in conf.yaml. For example, it will replace, $HOME with
    /home/username/

    Args:
        tokens_: the token dictionary
        token_symbol: TOKEN_SYMBOL
        parsed: the validated conf.yaml file
    """
    for section in parsed.sections():
        for entry in section.values():
            for key, value in tokens_["keywords"]["dict"].items():
                word = token_symbol + key
                if word in entry.location:
                    entry.location = entry.location.replace(word, value)


def parse_functions(tokens_: dict[str, Any], token_symbol: str, parsed: Config) -> None:
    """Replaces functions with values in conf.yaml. For example, it will replace,
    ${ENDS_WITH='text'} with a folder whose name ends with "text"

    Args:
        tokens_: the token dictionary
        token_symbol: TOKEN_SYMBOL
        parsed: the validated conf.yaml file
    """
    functions = tokens_["functions"]
    raw_regex = f"\\{token_symbol}{functions['raw_regex']}"
    grouped_regex = f"\\{token_symbol}{functions['grouped_regex']}"

    for section in parsed.sections():
        for entry in section.values():
            location = entry.location
            occurences = re.findall(raw_regex, location)
            if not occurences:
                continue
            for occurence in occurences:
                found = re.search(grouped_regex, occurence)
                if found is None:
                    continue
                func = found.group(1)
                if func in functions["dict"]:
                    entry.location = functions["dict"][func](grouped_regex, location)


TOKEN_SYMBOL = "$"
tokens: dict[str, Any] = {
    "keywords": {
        "dict": {
            "HOME": HOME,
            "CONFIG_DIR": CONFIG_DIR,
            "SHARE_DIR": SHARE_DIR,
            "BIN_DIR": BIN_DIR,
            "PROFILES_DIR": PROFILES_DIR,
            "DOT_PROFILES_DIR": DOT_PROFILES_DIR,
        }
    },
    "functions": {
        "raw_regex": r"\{\w+\=(?:\"|')\S+(?:\"|')\}",
        "grouped_regex": r"\{(\w+)\=(?:\"|')(\S+)(?:\"|')\}",
        "dict": {"ENDS_WITH": ends_with, "BEGINS_WITH": begins_with},
    },
}
