r"""Parse Key
=============
"""

import json
import os

json_dir = os.path.join(os.path.dirname(__file__), "assets", "json")
with open(os.path.join(json_dir, "keys.json")) as f:
    keys = json.load
with open(os.path.join(json_dir, "modifiers.json")) as f:
    modifiers = json.load


def parse_key(key: str, modifiers: list[str]) -> tuple[int, int]:
    r"""Parse key. Convert prompt-toolkit key name to rime key code and mask.

    :param key:
    :type key: str
    :param modifiers:
    :type modifiers: list[str]
    :rtype: tuple[int, int]
    """
    keycode = 0
    mask = 0
    return keycode, mask
