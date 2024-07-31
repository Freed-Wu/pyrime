r"""Prompt Toolkit
==================
"""

from dataclasses import dataclass

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import BufferControl
from ptpython.repl import PythonRepl


@dataclass
class Rime:
    repl: PythonRepl
    focus: Window | None = None
    editing_mode: str | EditingMode = "RIME"

    def __post_init__(self) -> None:
        for order in range(ord(" "), ord("~")):
            char = chr(order)

            @self.repl.add_key_binding(char, filter=self.filter())  # type: ignore
            def _(event: KeyPressEvent, char: str = char) -> None:
                event.cli.current_buffer.insert_text(char * 2)

    def filter(self) -> Condition:
        @Condition
        def _() -> bool:
            return self.repl.app.editing_mode == "RIME"

        return _

    def swap(self):
        (self.editing_mode, self.repl.app.editing_mode) = (  # type: ignore
            self.repl.app.editing_mode,
            self.editing_mode,
        )

    def disable(self) -> None:
        self.repl.app.layout.container.children.pop()  # type: ignore
        if self.focus:
            self.repl.app.layout.focus(self.focus)
        self.focus = None
        self.swap()

    def enable(self) -> None:
        self.focus = next(iter(self.repl.app.layout.get_focusable_windows()))
        window = Window(content=BufferControl(buffer=Buffer()), height=2)
        self.repl.app.layout.container.children += [window]  # type: ignore
        self.repl.app.layout.focus(window)
        self.swap()

    def toggle(self) -> None:
        # from pudb import set_trace
        #
        # set_trace()
        if self.focus:
            self.disable()
        else:
            self.enable()
