r"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
"""

import os

shared_data_dir = ""
for prefix in [
    os.getenv("PREFIX", "/usr/share"),
    "/usr/local/share",
    "/run/current-system/sw/share",
    "/sdcard",
]:
    path = os.path.expanduser(os.path.join(prefix, "rime-data"))
    if os.path.isdir(path):
        shared_data_dir = path
        break

user_data_dir = ""
for prefix in [
    "~/.config/ibus",
    "~/.local/share/fcitx5",
    "~/.config/fcitx",
    "/sdcard",
]:
    path = os.path.expanduser(os.path.join(prefix, "rime"))
    if os.path.isdir(path):
        user_data_dir = path
        break

if __name__ == "__main__":
    print(shared_data_dir)
    print(user_data_dir)
