r"""Prompt Toolkit
==================
"""

import os
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
from wcwidth import wcswidth

from . import (
    commitComposition,
    createSession,
    getCommit,
    getContext,
    init,
    processKey,
)
from .__main__ import Traits
from .draw_ui import UI, draw_ui
from .parse_key import parse_keys


@dataclass
class Rime:
    repl: PythonRepl
    session_id: int = 0
    is_enabled: bool = False
    window: Window = None  # type: ignore
    layout: Layout | None = None
    editing_mode: str | EditingMode = "RIME"
    traits: Traits = None  # type: ignore
    ui: UI = None  # type: ignore

    def __post_init__(self) -> None:
        if self.traits is None:
            self.traits = Traits()
        if self.ui is None:
            self.ui = UI()
        for order in range(ord(" "), ord("~") + 1):
            keys = [chr(order)]

            @self.repl.add_key_binding(*keys, filter=self.filter())  # type: ignore
            def _(event: KeyPressEvent, keys: list[str] = keys) -> None:
                text, lines, col = self.draw(keys)
                ui_text = "\n".join(lines)
                event.cli.current_buffer.insert_text(text)
                self.window.height = len(lines)
                if len(lines):
                    self.window.width = max(wcswidth(line) for line in lines)
                self.window.content.buffer.text = ui_text  # type: ignore
                left, top = self.calculate()
                left += col
                self.repl.app.layout.container.floats[0].left = left  # type: ignore
                self.repl.app.layout.container.floats[0].top = top  # type: ignore

    def get_commit_text(self) -> str:
        if commitComposition(self.session_id):
            return getCommit(self.session_id).text
        return ""

    def draw(self, keys: list[str]) -> tuple[str, list[str], int]:
        if not processKey(self.session_id, *parse_keys(keys)):
            if len(keys) == 1 == len(keys[0]):
                return keys[0], [self.ui.cursor], 0
            return "", [self.ui.cursor], 0
        context = getContext(self.session_id)
        if context.menu.num_candidates == 0:
            return self.get_commit_text(), [self.ui.cursor], 0
        lines, col = draw_ui(context, self.ui)
        return "", lines, col

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
            left += wcswidth(text)
        top = 0
        if self.repl.app.layout.current_buffer:
            lines = self.repl.app.layout.current_buffer.text[
                : self.repl.app.layout.current_buffer.cursor_position
            ].split("\n")
            top += len(lines)
            left += wcswidth(lines[-1])
        return left, top

    def init_(self) -> None:
        if self.session_id == 0:
            os.makedirs(self.traits.log_dir, exist_ok=True)
            init(**vars(self.traits))
            self.session_id = createSession()

    def enable(self) -> None:
        self.init_()
        left, top = self.calculate()
        self.window = Window(BufferControl(buffer=Buffer()), width=1, height=1)
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
