"""
Definition of the token kind categories.
"""

from __future__ import annotations

import abc
import typing

import attrs

from .infix import Associativity
from .infix import PrecedenceIndex

if typing.TYPE_CHECKING:
    import type  # noqa: A004


class TokenKindCategoryVisitor[R_co](typing.Protocol):
    """
    Interface for visiting token kind categories.
    """

    def visit_atom_category(self, category: Atom) -> R_co:
        """
        Visit an element of the atom category.
        """
        ...

    def visit_grouper_category(self, category: Grouper) -> R_co:
        """
        Visit an element of the grouper category.
        """
        ...

    def visit_keyword_category(self, category: Keyword) -> R_co:
        """
        Visit an element of the keyword category.
        """
        ...

    def visit_literal_category(self, category: Literal) -> R_co:
        """
        Visit an element of the literal category.
        """
        ...

    def visit_misc_category(self, category: Miscellaneous) -> R_co:
        """
        Visit an element of the miscellaneous category.
        """
        ...

    def visit_operator_category(self, category: Operator) -> R_co:
        """
        Visit an element of the operator category.
        """
        ...

    def visit_punctuation_category(self, category: Punctuation) -> R_co:
        """
        Visit an element of the punctuation category.
        """
        ...

    def visit_relation_category(self, category: Relation) -> R_co:
        """
        Visit an element of the relation category.
        """
        ...


@attrs.frozen
class AbstractTokenKindCategory(abc.ABC):
    """
    Represents an abstract token kind category.
    """

    is_identifier_alike: bool = attrs.field(default=False, kw_only=True)

    @abc.abstractmethod
    def accept[R](self, visitor: TokenKindCategoryVisitor[R]) -> R:
        """
        Accept a visitor.
        """


@attrs.frozen
class Atom(AbstractTokenKindCategory):
    """
    Represents atom token kinds, e.g. `IDENTIFIER`.
    """

    # defined for consistency with other categories
    lexeme: str = attrs.field(init=False, default="<atom>")

    @typing.override
    def accept[R](self, visitor: TokenKindCategoryVisitor[R]) -> R:
        return visitor.visit_atom_category(self)


@attrs.frozen
class Grouper(AbstractTokenKindCategory):
    """
    Represents grouper token kinds, e.g. parentheses.
    """

    lexeme: str

    @typing.override
    def accept[R](self, visitor: TokenKindCategoryVisitor[R]) -> R:
        return visitor.visit_grouper_category(self)


@attrs.frozen
class Keyword(AbstractTokenKindCategory):
    """
    Represents keyword token kinds, e.g. `LET` or `MATCH`.
    """

    lexeme: str
    leading: bool = attrs.field(default=True, kw_only=True)
    is_identifier_alike: bool = attrs.field(default=True, kw_only=True)

    @typing.override
    def accept[R](self, visitor: TokenKindCategoryVisitor[R]) -> R:
        return visitor.visit_keyword_category(self)


@attrs.frozen
class Literal(AbstractTokenKindCategory):
    """
    Represents literal token kinds, e.g. `INTEGER` or `STRING`.
    """

    kind: type.PrimitiveKind
    # NOTE: defined for consistency with other categories
    lexeme: str = attrs.field(init=False, default="<literal>")

    @typing.override
    def accept[R](self, visitor: TokenKindCategoryVisitor[R]) -> R:
        return visitor.visit_literal_category(self)


@attrs.frozen
class Miscellaneous(AbstractTokenKindCategory):
    """
    Represents miscellaneous token kinds, such as `EOF`.
    """

    # NOTE: defined for consistency with other categories
    lexeme: str = attrs.field(init=False, default="<misc>")

    @typing.override
    def accept[R](self, visitor: TokenKindCategoryVisitor[R]) -> R:
        return visitor.visit_misc_category(self)


@attrs.frozen
class Operator(AbstractTokenKindCategory):
    """
    Represents operator token kinds, such as `PLUS`.
    """

    lexeme: str
    associativity: Associativity = attrs.field(default=Associativity.LEFT)
    precedence: PrecedenceIndex = attrs.field(default=1, kw_only=True)

    @typing.override
    def accept[R](self, visitor: TokenKindCategoryVisitor[R]) -> R:
        return visitor.visit_operator_category(self)


@attrs.frozen
class Punctuation(AbstractTokenKindCategory):
    """
    Represents punctuation token kinds, such as `COMMA`.
    """

    lexeme: str

    @typing.override
    def accept[R](self, visitor: TokenKindCategoryVisitor[R]) -> R:
        return visitor.visit_punctuation_category(self)


@attrs.frozen
class Relation(AbstractTokenKindCategory):
    """
    Represents relation token kinds, such as `EQUAL`.
    """

    lexeme: str

    @typing.override
    def accept[R](self, visitor: TokenKindCategoryVisitor[R]) -> R:
        return visitor.visit_relation_category(self)


type TokenKindCategory = (
    Atom | Keyword | Literal | Miscellaneous | Operator | Punctuation | Relation
)
