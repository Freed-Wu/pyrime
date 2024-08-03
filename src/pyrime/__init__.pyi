r"""Provide ``__version__`` for
`importlib.metadata.version() <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_.
"""

from dataclasses import dataclass

@dataclass
class Composition:
    length: int
    cursor_pos: int
    sel_start: int
    sel_end: int
    preedit: str

@dataclass
class Candidate:
    text: str
    comment: str | None

@dataclass
class Menu:
    page_size: int
    page_no: int
    is_last_page: int
    highlighted_candidate_index: int
    num_candidates: int
    select_keys: str | None
    candidates: list[Candidate]

@dataclass
class Context:
    composition: Composition
    menu: Menu

@dataclass
class Commit:
    text: str

def init(
    shared_data_dir: str,
    user_data_dir: str,
    log_dir: str,
    distribution_name: str,
    distribution_code_name: str,
    distribution_version: str,
    app_name: str,
    min_log_level: int,
) -> None: ...
def createSession() -> int: ...
def destroySession(session_id: int) -> None: ...
def getCurrentSchema(session_id: int) -> str: ...
def getSchemaList() -> list[tuple[str, str]]: ...
def selectSchema(session_id: int, name: str) -> None: ...
def processKey(session_id: int, keycode: int, mask: int) -> None: ...
def getContext(session_id: int) -> Context: ...
def getCommit(session_id: int) -> Commit: ...
def commitComposition(session_id: int) -> bool: ...
def clearComposition(session_id: int) -> None: ...
