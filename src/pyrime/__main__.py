r"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
"""

import os
from dataclasses import dataclass

from platformdirs import user_data_path

shared_data_dir = ""
eprefix = os.getenv(
    "PREFIX",
    os.path.dirname(os.path.dirname(os.getenv("SHELL", "/bin/sh"))),
)
for prefix in [
    # /usr merge: /usr/bin/sh -> /usr/share/rime-data
    os.path.join(eprefix, "share"),
    # non /usr merge: /bin/sh -> /usr/share/rime-data
    os.path.join(eprefix, "usr/share"),
    "/run/current-system/sw",
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


@dataclass
class Traits:
    shared_data_dir: str = shared_data_dir
    user_data_dir: str = user_data_dir
    log_dir: str = str(user_data_path("ptpython") / "rime")
    distribution_name: str = "Rime"
    distribution_code_name: str = "pyrime"
    distribution_version: str = "0.0.1"
    app_name: str = "rime.pyrime"
    min_log_level: int = 3


if __name__ == "__main__":
    print(Traits())
