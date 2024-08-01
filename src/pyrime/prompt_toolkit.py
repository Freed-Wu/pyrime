r"""Prompt Toolkit
==================
"""

from dataclasses import dataclass

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout.containers import (
    Float,
    FloatContainer,
    Window,
)
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame
from ptpython.repl import PythonRepl


@dataclass
class Rime:
    repl: PythonRepl
    is_enabled: bool = False
    window: Window | None = None
    layout: Layout | None = None
    editing_mode: str | EditingMode = "RIME"

    def __post_init__(self) -> None:
        for order in range(ord(" "), ord("~")):
            char = chr(order)

            @self.repl.add_key_binding(char, filter=self.filter())  # type: ignore
            def _(event: KeyPressEvent, char: str = char) -> None:
                event.cli.current_buffer.text = char
                self.window.content.buffer.text = char * 2  # type: ignore
                left, top = self.calculate()
                self.repl.app.layout.container.floats[0].left = left  # type: ignore
                self.repl.app.layout.container.floats[0].top = top  # type: ignore

    def filter(self) -> Condition:
        @Condition
        def _() -> bool:
            return self.repl.app.editing_mode == "RIME"

        return _

    def swap_editing_mode(self):
        (self.editing_mode, self.repl.app.editing_mode) = (  # type: ignore
            self.repl.app.editing_mode,
            self.editing_mode,
        )

    def swap_layout(self):
        (self.layout, self.repl.app.layout) = (  # type: ignore
            self.repl.app.layout,
            self.layout,
        )

    def disable(self) -> None:
        self.swap_editing_mode()
        self.swap_layout()
        self.is_enabled = False

    def calculate(self) -> tuple[int, int]:
        left = 0
        for _, text in self.repl.all_prompt_styles[  # type: ignore
            self.repl.prompt_style
        ].in_prompt():
            left += len(text)
        top = 0
        if self.repl.app.layout.current_buffer:
            lines = self.repl.app.layout.current_buffer.text[
                : self.repl.app.layout.current_buffer.cursor_position
            ].split("\n")
            top += len(lines)
            left += len(lines[-1])
        return left, top

    def enable(self) -> None:
        left, top = self.calculate()
        self.window = Window(
            BufferControl(buffer=Buffer()), width=10, height=2
        )
        self.layout = Layout(
            FloatContainer(  # type: ignore
                self.repl.app.layout.container,
                [
                    Float(
                        Frame(
                            self.window,
                        ),
                        left=left,
                        top=top,
                    )
                ],
            )
        )
        self.swap_editing_mode()
        self.swap_layout()
        self.is_enabled = True

    def toggle(self) -> None:
        if self.is_enabled:
            self.disable()
        else:
            self.enable()
