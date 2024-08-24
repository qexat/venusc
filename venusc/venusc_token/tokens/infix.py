"""
Definition of the infix operator properties.
"""

from __future__ import annotations

import enum
import typing

type PrecedenceIndex = typing.Literal[0, 1, 2, 3, 4, 5, 6, 7]
"""
Integer representing the precedence of an infix operator.
Lowest means last to be evaluated, highest means first.

The default is `1`, as `0` is meant for `:=`.
"""


class Associativity(enum.Enum):
    """
    Represents the associativity of an infix operator.
    """

    LEFT = enum.auto()
    RIGHT = enum.auto()
