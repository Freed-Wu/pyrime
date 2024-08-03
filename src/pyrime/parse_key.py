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


def parse_key(key: str, modifiers: set[str]) -> tuple[int, int]:
    r"""Parse key. Convert prompt-toolkit key name to rime key code and mask.

    Refer `<https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/key_bindings.html#list-of-special-keys>`_

    :param key:
    :type key: str
    :param modifiers:
    :type modifiers: set[str]
    :rtype: tuple[int, int]
    """
    key = {"c-i": "tab", "c-m": "enter", "c-space": "c-@"}.get(key, key)
    if key.startswith("c-"):
        modifiers |= {"Control"}
        _, _, key = key.partition("c-")
        key = {"@": "2", "^": "6", "-": "_"}.get(key, key)
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
    if keys == ["escape", *"[13;2u"]:
        key = "enter"
        modifiers = {"Shift"}
    elif keys == ["escape", *"[13;3u"]:
        key = "enter"
        modifiers = {"Shift", "Alt"}
    elif keys == ["escape", *"[13;5u"]:
        key = "enter"
        modifiers = {"Control"}
    elif keys == ["escape", *"[13;6u"]:
        key = "enter"
        modifiers = {"Shift", "Control"}
    elif keys == ["escape", *"[13;7u"]:
        key = "enter"
        modifiers = {"Alt", "Control"}
    elif keys == ["escape", *"[13;8u"]:
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
