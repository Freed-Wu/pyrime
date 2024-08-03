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

SHIFT_CR = ["escape", *"[13;2u"]
ALT_CR = ["escape", "enter"]
ALT_SHIFT_CR = ["escape", *"[13;4u"]
CONTROL_CR = ["escape", *"[13;5u"]
CONTROL_SHIFT_CR = ["escape", *"[13;6u"]
CONTROL_ALT_CR = ["escape", *"[13;7u"]
CONTROL_ALT_SHIFT_CR = ["escape", *"[13;8u"]


def parse_key(key: str, modifiers: set[str]) -> tuple[int, int]:
    r"""Parse key. Convert prompt-toolkit key name to rime key code and mask.

    Refer `<https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/key_bindings.html#list-of-special-keys>`_

    :param key:
    :type key: str
    :param modifiers:
    :type modifiers: set[str]
    :rtype: tuple[int, int]
    """
    key = {"c-i": "tab", "c-m": "enter", "c-@": "c-space"}.get(key, key)
    if key.startswith("c-"):
        modifiers |= {"Control"}
        _, _, key = key.partition("c-")
        key = {"space": " ", "^": "6", "-": "_"}.get(key, key)
    if key.startswith("s-"):
        modifiers |= {"Shift"}
        _, _, key = key.partition("s-")
    if len(key) > 1:
        key = key.capitalize()
    key = {
        "Enter": "Return",
        "Pageup": "Page_Up",
        "Pagedown": "Page_Down",
    }.get(key, key)
    keycode = keys.get(key, ord(key[0]))
    mask = 0
    for modifier in modifiers:
        index = modifiers_.index(modifier)
        if index != -1:
            mask += 2**index
    return keycode, mask


def parse_keys(keys: list[str]) -> tuple[int, int]:
    r"""Parse keys.

    :param keys:
    :type keys: list[str]
    :rtype: tuple[int, int]
    """
    if keys == SHIFT_CR:
        key = "enter"
        modifiers = {"Shift"}
    elif keys == ALT_SHIFT_CR:
        key = "enter"
        modifiers = {"Shift", "Alt"}
    elif keys == CONTROL_CR:
        key = "enter"
        modifiers = {"Control"}
    elif keys == CONTROL_SHIFT_CR:
        key = "enter"
        modifiers = {"Shift", "Control"}
    elif keys == CONTROL_ALT_CR:
        key = "enter"
        modifiers = {"Alt", "Control"}
    elif keys == CONTROL_ALT_SHIFT_CR:
        key = "enter"
        modifiers = {"Shift", "Alt", "Control"}
    elif len(keys) == 2 and keys[0] == "escape":
        key = keys[1]
        modifiers = {"Alt"}
    elif len(keys) == 1:
        key = keys[0]
        modifiers = set()
    else:
        raise NotImplementedError
    return parse_key(key, modifiers)
