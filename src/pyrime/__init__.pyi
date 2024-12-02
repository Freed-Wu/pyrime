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
def create_session() -> int: ...
def destroy_session(session_id: int) -> None: ...
def get_current_schema(session_id: int) -> str: ...
def get_schema_list() -> list[tuple[str, str]]: ...
def select_schema(session_id: int, name: str) -> None: ...
def process_key(session_id: int, keycode: int, mask: int) -> None: ...
def get_context(session_id: int) -> Context: ...
def get_commit(session_id: int) -> Commit: ...
def commit_composition(session_id: int) -> bool: ...
def clear_composition(session_id: int) -> None: ...
