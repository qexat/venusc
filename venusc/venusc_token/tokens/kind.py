"""
Definition of the token kinds.
"""

from __future__ import annotations

import enum

import type

from .category import Atom
from .category import Grouper
from .category import Keyword
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

    AND = Keyword("and", leading=False)
    CASE = Keyword("case", leading=False)
    DISCARD = Keyword("discard")
    ELSE = Keyword("else", leading=False)
    END = Keyword("end", leading=False)
    FIX = Keyword("fix")
    IF = Keyword("if")
    LET = Keyword("let")
    MATCH = Keyword("match")
    OR = Keyword("or", leading=False)
    PROOF = Keyword("proof")
    THEN = Keyword("then", leading=False)
    USE = Keyword("use")
    WHERE = Keyword("where", leading=False)

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


KEYWORD_MAPPING: dict[str, TokenKind] = {
    kind.value.lexeme: kind
    for kind in TokenKind
    if kind.value.is_identifier_alike
}
