r"""Parse Key
=============
"""

import json
import os

json_dir = os.path.join(os.path.dirname(__file__), "assets", "json")
with open(os.path.join(json_dir, "keys.json")) as f:
    keys: dict = json.load(f)
with open(os.path.join(json_dir, "modifiers.json")) as f:
    modifiers_: list = json.load(f)  # type: ignore


def parse_key(key: str, modifiers: list[str]) -> tuple[int, int]:
    r"""Parse key. Convert prompt-toolkit key name to rime key code and mask.

    Refer `<https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/key_bindings.html#list-of-special-keys>`_

    :param key:
    :type key: str
    :param modifiers:
    :type modifiers: list[str]
    :rtype: tuple[int, int]
    """
    key = {"c-i": "tab", "c-m": "enter", "c-space": "c-@"}.get(key, key)
    if key.startswith("c-"):
        modifiers += ["Control"]
        _, _, key = key.partition("c-")
        key = {"@": "2", "^": "6", "-": "_"}.get(key, key)
    if key.startswith("s-"):
        modifiers += ["Shift"]
        _, _, key = key.partition("s-")
    key = key.capitalize()
    key = {
        "Enter": "Return",
        "Pageup": "Page_Up",
        "Pagedown": "Page_Down",
    }.get(key, key)
    keycode = keys.get(key, ord(key))
    mask = 0
    for modifier in modifiers:
        index = modifiers_.index(modifier)
        if index != -1:
            mask += 2**index
    return keycode, mask
