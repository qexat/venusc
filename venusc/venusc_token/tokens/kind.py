"""
Definition of the token kinds.
"""

from __future__ import annotations

import enum

import type  # noqa: A004

from .category import Atom
from .category import Grouper
from .category import Keyword
from .category import KeywordKind
from .category import Literal
from .category import Miscellaneous
from .category import Operator
from .category import Punctuation
from .category import Relation
from .infix import Associativity


class TokenKind(enum.Enum):
    """
    Represents a token kind.
    """

    IDENTIFIER = Atom()

    LEFT_BRACKET = Grouper("[")
    LEFT_PAREN = Grouper("(")
    RIGHT_BRACKET = Grouper("]")
    RIGHT_PAREN = Grouper(")")

    AND = Keyword("and", KeywordKind.EXPRESSION_CONJUNCTIVE)
    CASE = Keyword("case", KeywordKind.EXPRESSION_CONJUNCTIVE)
    DISCARD = Keyword("discard", KeywordKind.EXPRESSION_STARTER)
    ELSE = Keyword("else", KeywordKind.EXPRESSION_CONJUNCTIVE)
    END = Keyword("end", KeywordKind.EXPRESSION_CONJUNCTIVE)
    FIX = Keyword("fix", KeywordKind.STATEMENT_STARTER)
    IF = Keyword("if", KeywordKind.EXPRESSION_STARTER)
    LET = Keyword("let", KeywordKind.STATEMENT_STARTER)
    MATCH = Keyword("match", KeywordKind.EXPRESSION_STARTER)
    OR = Keyword("or", KeywordKind.EXPRESSION_CONJUNCTIVE)
    PROOF = Keyword("proof", KeywordKind.STATEMENT_STARTER)  # unused
    THEN = Keyword("then", KeywordKind.EXPRESSION_CONJUNCTIVE)
    USE = Keyword("use", KeywordKind.STATEMENT_STARTER)
    WHERE = Keyword("where", KeywordKind.STATEMENT_CONJUNCTIVE)

    NATURAL = Literal(type.PrimitiveKind.NATURAL)
    STRING = Literal(type.PrimitiveKind.STRING)
    UNIT = Literal(type.PrimitiveKind.UNIT)

    EOF = Miscellaneous()

    CARET = Operator("^", Associativity.RIGHT, precedence=5)
    # NOTE: Special-cased operator that isn't actually considered as such.
    # NOTE: Marked as right-associative for documentation ; same for precedence.
    COLON_EQUAL = Operator(":=", Associativity.RIGHT, precedence=0)
    # NOTE: We don't start at 1 to leave some room for lower operators
    MINUS = Operator("-", precedence=3)
    MODULO = Operator("mod", precedence=4, is_identifier_alike=True)
    PLUS = Operator("+", precedence=3)
    SLASH = Operator("/", precedence=4)
    STAR = Operator("*", precedence=4)

    COLON = Punctuation(":")  # means "in set"/"of type"
    COMMA = Punctuation(",")  # for tuples
    PERCENT = Punctuation("%")  # for refining literal type
    PERIOD = Punctuation(".")  # namespaces
    RIGHT_ARROW = Punctuation("->")  # functions & pattern matching
    SEMICOLON = Punctuation(";")  # end of expression marker

    EQUAL = Relation("=")
    GREATER = Relation(">")
    GREATER_EQUAL = Relation(">=")
    IS = Relation("is", is_identifier_alike=True)
    LESS = Relation("<")
    LESS_EQUAL = Relation("<=")


# "Identifier-alike" includes keywords or any operator that would, without
# knowledge of its existence, be tokenized as an identifier.
IDENTIFIER_ALIKE_MAPPING: dict[str, TokenKind] = {
    kind.value.lexeme: kind
    for kind in TokenKind
    if kind.value.is_identifier_alike
}


def starts_statement(kind: TokenKind) -> bool:
    """
    Checks whether the given token kind is a statement starter.

    Returns
    -------
    bool
    """

    return (
        isinstance(kind.value, Keyword)
        and kind.value.kind is KeywordKind.STATEMENT_STARTER
    )


def is_statement_conjunctive(kind: TokenKind) -> bool:
    """
    Checks whether the given token kind is a statement conjunctive.

    Returns
    -------
    bool
    """

    return (
        isinstance(kind.value, Keyword)
        and kind.value.kind is KeywordKind.STATEMENT_CONJUNCTIVE
    )


def starts_expression(kind: TokenKind) -> bool:
    """
    Checks whether the given token kind is an expression starter.

    Returns
    -------
    bool
    """

    return (
        isinstance(kind.value, Keyword)
        and kind.value.kind is KeywordKind.EXPRESSION_STARTER
    )


def is_expression_conjunctive(kind: TokenKind) -> bool:
    """
    Checks whether the given token kind is an expression conjunctive.

    Returns
    -------
    bool
    """

    return (
        isinstance(kind.value, Keyword)
        and kind.value.kind is KeywordKind.EXPRESSION_CONJUNCTIVE
    )
