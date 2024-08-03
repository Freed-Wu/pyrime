r"""Smartinput
==============

Add spaces around operators.

Refer `vim-smartinput <https://github.com/kana/vim-smartinput>`_.
"""

from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from ptpython.repl import PythonRepl

from ..utils.condition import InsertMode


def smartinput(repl: PythonRepl) -> None:
    r"""Smartinput.

    :param repl:
    :type repl: PythonRepl
    :rtype: None
    """

    # One {{{1 #
    @repl.add_key_binding(",", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.current_char == " ":
            b.insert_text(",")
        else:
            b.insert_text(", ")

    # 1}}} One #

    # Two {{{1 #
    # Operation {{{2 #
    @repl.add_key_binding("+", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.current_char == " ":
            b.insert_text("+")
        else:
            b.insert_text(" + ")

    @repl.add_key_binding("@", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if (
            b.document.char_before_cursor == " "
            or b.document.cursor_position_col == 0
        ):
            b.insert_text("@")
        else:
            b.insert_text(" @ ")

    @repl.add_key_binding("*", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("*")
        else:
            b.insert_text(" * ")

    @repl.add_key_binding("*", "*", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("**")
        else:
            b.insert_text(" ** ")

    @repl.add_key_binding("/", "/", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("//")
        else:
            b.insert_text(" // ")

    @repl.add_key_binding("%", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if (
            b.document.char_before_cursor == " "
            or b.document.cursor_position_col == 0
        ):
            b.insert_text("%")
        else:
            b.insert_text(" % ")

    @repl.add_key_binding("&", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("&")
        else:
            b.insert_text(" & ")

    @repl.add_key_binding("|", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("|")
        else:
            b.insert_text(" | ")

    @repl.add_key_binding("^", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("^")
        else:
            b.insert_text(" ^ ")

    @repl.add_key_binding("<", "<", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("<<")
        else:
            b.insert_text(" << ")

    @repl.add_key_binding(">", ">", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text(">>")
        else:
            b.insert_text(" >> ")

    # 1}}} Operation #

    # Relation {{{2 #
    @repl.add_key_binding("<", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("<")
        else:
            b.insert_text(" < ")

    @repl.add_key_binding(">", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text(">")
        else:
            b.insert_text(" > ")

    @repl.add_key_binding(":", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text(":=")
        else:
            b.insert_text(" := ")

    @repl.add_key_binding("=", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("==")
        else:
            b.insert_text(" == ")

    @repl.add_key_binding("!", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("!=")
        else:
            b.insert_text(" != ")

    @repl.add_key_binding("<", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("<=")
        else:
            b.insert_text(" <= ")

    @repl.add_key_binding(">", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text(">=")
        else:
            b.insert_text(" >= ")

    # 1}}} Relation #

    # Assign {{{2 #
    @repl.add_key_binding("=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("=")
        else:
            b.insert_text(" = ")

    @repl.add_key_binding("+", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("+=")
        else:
            b.insert_text(" += ")

    @repl.add_key_binding("-", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("-=")
        else:
            b.insert_text(" -= ")

    @repl.add_key_binding("@", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("@=")
        else:
            b.insert_text(" @= ")

    @repl.add_key_binding("*", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("*=")
        else:
            b.insert_text(" *= ")

    @repl.add_key_binding("/", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("/=")
        else:
            b.insert_text(" /= ")

    @repl.add_key_binding("*", "*", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("**=")
        else:
            b.insert_text(" **= ")

    @repl.add_key_binding("/", "/", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("//=")
        else:
            b.insert_text(" //= ")

    @repl.add_key_binding("%", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("%=")
        else:
            b.insert_text(" %= ")

    @repl.add_key_binding("&", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("&=")
        else:
            b.insert_text(" &= ")

    @repl.add_key_binding("|", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("|=")
        else:
            b.insert_text(" |= ")

    @repl.add_key_binding("^", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("^=")
        else:
            b.insert_text(" ^= ")

    @repl.add_key_binding("<", "<", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("<<=")
        else:
            b.insert_text(" <<= ")

    @repl.add_key_binding(">", ">", "=", filter=InsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text(">>=")
        else:
            b.insert_text(" >>= ")

    # 2}}} Assign #
    # 1}}} Two #


# ex: foldmethod=marker
