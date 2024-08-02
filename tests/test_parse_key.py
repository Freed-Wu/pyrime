r"""Test parse_key."""

from pyrime.parse_key import parse_key


class Test:
    r"""Test."""

    @staticmethod
    def test_parse_key() -> None:
        assert parse_key("c-^", []) == parse_key("6", ["Control"])
