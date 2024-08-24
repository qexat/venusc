"""
Definition of the primitive kinds.
"""

from __future__ import annotations

import enum


class PrimitiveKind(enum.Enum):
    """
    Represents the primitive type kind.
    """

    BOOLEAN = enum.auto()
    INTEGER = enum.auto()
    NATURAL = enum.auto()
    NEVER = enum.auto()
    STRING = enum.auto()
    UNIT = enum.auto()

    @property
    def real_name(self) -> str:
        """
        Name of the type in the language.
        """

        return self.name.title()
