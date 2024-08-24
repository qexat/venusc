"""
Definition of the token data structure.
"""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .kind import TokenKind


class Token(typing.NamedTuple):
    """
    Represents a token.
    """

    kind: TokenKind
    lexeme: str
    offset: int

    @property
    def span(self) -> tuple[int, int]:
        """
        Span of the token, i.e. the position range in the source.
        """

        return (self.offset, self.offset + len(self.lexeme))
