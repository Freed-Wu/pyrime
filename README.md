# pyrime

[![readthedocs](https://shields.io/readthedocs/pyrime)](https://pyrime.readthedocs.io)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Freed-Wu/pyrime/main.svg)](https://results.pre-commit.ci/latest/github/Freed-Wu/pyrime/main)
[![github/workflow](https://github.com/Freed-Wu/pyrime/actions/workflows/main.yml/badge.svg)](https://github.com/Freed-Wu/pyrime/actions)
[![codecov](https://codecov.io/gh/Freed-Wu/pyrime/branch/main/graph/badge.svg)](https://codecov.io/gh/Freed-Wu/pyrime)

[![github/downloads](https://shields.io/github/downloads/Freed-Wu/pyrime/total)](https://github.com/Freed-Wu/pyrime/releases)
[![github/downloads/latest](https://shields.io/github/downloads/Freed-Wu/pyrime/latest/total)](https://github.com/Freed-Wu/pyrime/releases/latest)
[![github/issues](https://shields.io/github/issues/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/issues)
[![github/issues-closed](https://shields.io/github/issues-closed/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/issues?q=is%3Aissue+is%3Aclosed)
[![github/issues-pr](https://shields.io/github/issues-pr/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/pulls)
[![github/issues-pr-closed](https://shields.io/github/issues-pr-closed/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/pulls?q=is%3Apr+is%3Aclosed)
[![github/discussions](https://shields.io/github/discussions/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/discussions)
[![github/milestones](https://shields.io/github/milestones/all/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/milestones)
[![github/forks](https://shields.io/github/forks/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/network/members)
[![github/stars](https://shields.io/github/stars/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/stargazers)
[![github/watchers](https://shields.io/github/watchers/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/watchers)
[![github/contributors](https://shields.io/github/contributors/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/graphs/contributors)
[![github/commit-activity](https://shields.io/github/commit-activity/w/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/graphs/commit-activity)
[![github/last-commit](https://shields.io/github/last-commit/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/commits)
[![github/release-date](https://shields.io/github/release-date/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/releases/latest)

[![github/license](https://shields.io/github/license/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime/blob/main/LICENSE)
[![github/languages](https://shields.io/github/languages/count/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime)
[![github/languages/top](https://shields.io/github/languages/top/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime)
[![github/directory-file-count](https://shields.io/github/directory-file-count/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime)
[![github/code-size](https://shields.io/github/languages/code-size/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime)
[![github/repo-size](https://shields.io/github/repo-size/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime)
[![github/v](https://shields.io/github/v/release/Freed-Wu/pyrime)](https://github.com/Freed-Wu/pyrime)

[![pypi/status](https://shields.io/pypi/status/pyrime)](https://pypi.org/project/pyrime/#description)
[![pypi/v](https://shields.io/pypi/v/pyrime)](https://pypi.org/project/pyrime/#history)
[![pypi/downloads](https://shields.io/pypi/dd/pyrime)](https://pypi.org/project/pyrime/#files)
[![pypi/format](https://shields.io/pypi/format/pyrime)](https://pypi.org/project/pyrime/#files)
[![pypi/implementation](https://shields.io/pypi/implementation/pyrime)](https://pypi.org/project/pyrime/#files)
[![pypi/pyversions](https://shields.io/pypi/pyversions/pyrime)](https://pypi.org/project/pyrime/#files)

![screenshot](https://github.com/user-attachments/assets/5c79575c-79c5-4e4f-b6ab-b9cdaad352b2)

rime for python, attached to prompt-toolkit keybindings for some prompt-toolkit
applications such as ptpython.

## Dependence

- [librime](https://github.com/rime/librime)

```sh
# Ubuntu
sudo apt-get -y install librime-dev librime1 pkg-config
sudo apt-mark auto librime-dev pkg-config
# ArchLinux
sudo pacman -S --noconfirm librime pkg-config
# Android Termux
apt-get -y install librime pkg-config
# Nix
# use nix-shell to create a virtual environment then build
# homebrew
brew tap tonyfettes/homebrew-rime
brew install librime pkg-config
# Windows msys2
pacboy -S --noconfirm pkg-config:x librime:x gcc:x
```

## Configure

`~/.config/ptpython/config.py`:

```python
from ptpython.repl import PythonRepl
from prompt_toolkit.filters import EmacsInsertMode, ViInsertMode
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from pyrime.prompt_toolkit import Rime


def configure(repl: PythonRepl) -> None:
    rime = Rime(repl)

    @repl.add_key_binding("c-^", filter=ViInsertMode())
    @repl.add_key_binding("c-^", filter=EmacsInsertMode())
    @repl.add_key_binding("c-^", filter=rime.mode())
    def _(event: KeyPressEvent) -> None:
        rime.toggle()
```

If you defined some key bindings which will disturb rime, try:

```python
    @repl.add_key_binding("c-h", filter=rime.filter(EmacsInsertMode()))
    def _(event: KeyPressEvent) -> None:
        rime.toggle()
```

If you want to exit rime in `ViNavigationMode()`, try:

```python
    @repl.add_key_binding("escape", filter=EmacsInsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.VI
        event.app.vi_state.input_mode = InputMode.NAVIGATION
        rime.conditional_disable()

    # and a, I, A, ...
    @repl.add_key_binding("i", filter=ViNavigationMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.EMACS
        event.app.vi_state.input_mode = InputMode.INSERT
        rime.conditional_enable()
```

It will remember rime status and enable it when reenter `ViInsertMode()` or
`EmacsInsertMode()`.

Some utility functions are defined in this project. Refer
[my ptpython config](https://github.com/Freed-Wu/Freed-Wu/blob/main/.config/ptpython/config.py)
to know more.
