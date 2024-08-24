# ruff: noqa: F821  # TODO: remove
"""
Definition of Venus' compiler error tree.
"""

from __future__ import annotations

import abc
import typing

import attrs


class SyntaxErrorVisitor[R_co](typing.Protocol):
    """
    Represents a visitor of the syntax error tree.
    """

    def visit_invalid_string_escape_sequence_error(
        self,
        error: InvalidStringEscapeSequenceError,
    ) -> R_co:
        """
        Visit an invalid string escape sequence error.
        """
        ...

    def visit_unclosed_string_error(
        self,
        error: UnclosedStringError,
    ) -> R_co:
        """
        Visit an unclosed string error.
        """
        ...

    def visit_unexpected_special_character_in_string_error(
        self,
        error: UnexpectedSpecialCharacterInStringError,
    ) -> R_co:
        """
        Visit an unexpected special character in string error.
        """
        ...

    def visit_unrecognized_character_error(
        self,
        error: UnrecognizedCharacterError,
    ) -> R_co:
        """
        Visit an unrecognized character error.
        """
        ...


class GrammarErrorVisitor[R_co](typing.Protocol):
    """
    Represents a visitor of the grammar error tree.
    """

    def visit_incomplete_expression_error(
        self,
        error: IncompleteExpressionError,
    ) -> R_co:
        """
        Visit an incomplete expression error.
        """
        ...

    def visit_keyword_misuse_error(
        self,
        error: KeywordMisuseError,
    ) -> R_co:
        """
        Visit a keyword misuse error.
        """
        ...

    def visit_unexpected_eof_error(
        self,
        error: UnexpectedEofError,
    ) -> R_co:
        """
        Visit an unexpected EOF error.
        """
        ...

    def visit_unexpected_token_error(
        self,
        error: UnexpectedTokenError,
    ) -> R_co:
        """
        Visit an unexpected token error.
        """
        ...

    def visit_unmatched_bracket_error(
        self,
        error: UnmatchedBracketError,
    ) -> R_co:
        """
        Visit an unmatched bracket error.
        """
        ...


class NameAnalysisErrorVisitor[R_co](typing.Protocol):
    """
    Represents a visitor of the name analysis error tree.
    """

    def visit_implicitly_unused_symbol_error(
        self,
        error: ImplicitlyUnusedSymbolError,
    ) -> R_co:
        """
        Visit an implicitly unused symbol error.
        """
        ...

    def visit_out_of_scope_symbol_error(
        self,
        error: OutOfScopeSymbolError,
    ) -> R_co:
        """
        Visit an out of scope symbol error.
        """
        ...

    def visit_undefined_symbol_error(
        self,
        error: UndefinedSymbolError,
    ) -> R_co:
        """
        Visit an undefined symbol error.
        """
        ...

    def visit_use_before_definition_error(
        self,
        error: UseBeforeDefinitionError,
    ) -> R_co:
        """
        Visit a use before definition error.
        """
        ...


class TypeCheckingErrorVisitor[R_co](typing.Protocol):
    """
    Represents a visitor of the type checking error tree.
    """

    def visit_invalid_argument_type_error(
        self,
        error: InvalidArgumentTypeError,
    ) -> R_co:
        """
        Visit an invalid argument type error.
        """
        ...

    def visit_mismatched_types_error(
        self,
        error: MismatchedTypesError,
    ) -> R_co:
        """
        Visit a mismatched types error.
        """
        ...

    def visit_missing_constraints_error(
        self,
        error: MissingConstraintsError,
    ) -> R_co:
        """
        Visit a missing constraints error.
        """
        ...

    def visit_nonhalting_inductive_definition_error(
        self,
        error: NonhaltingInductiveDefinitionError,
    ) -> R_co:
        """
        Visit a nonhalting inductive definition error.
        """
        ...

    def visit_unfixed_inductive_definition_error(
        self,
        error: UnfixedInductiveDefinitionError,
    ) -> R_co:
        """
        Visit an unfixed inductive defintion error.
        """
        ...

    def visit_uninferable_definition_type_error(
        self,
        error: UninferableDefinitionError,
    ) -> R_co:
        """
        Visit an uninferable definition error.
        """
        ...


class CompilationErrorVisitor[R_co](
    TypeCheckingErrorVisitor[R_co],
    NameAnalysisErrorVisitor[R_co],
    GrammarErrorVisitor[R_co],
    SyntaxErrorVisitor[R_co],
):
    """
    Represents a visitor of the compilation error tree.
    """


@attrs.frozen
class AbstractCompilationError(abc.ABC):
    """
    Represents an abstract compilation error.
    """

    span: tuple[int, int]

    @abc.abstractmethod
    def accept[R](self, visitor: CompilationErrorVisitor[R]) -> R:
        """
        Accept a compilation error visitor and return the result.
        """


class AbstractSyntaxError(AbstractCompilationError):
    """
    Represents an abstract syntax error.
    """

    @abc.abstractmethod
    @typing.override
    def accept[R](self, visitor: SyntaxErrorVisitor[R]) -> R:
        pass


@attrs.frozen
class InvalidStringEscapeSequenceError(AbstractSyntaxError):
    """
    Error triggered when an invalid escape sequence is found in a string.
    """

    escape_sequence: str

    @typing.override
    def accept[R](self, visitor: SyntaxErrorVisitor[R]) -> R:
        return visitor.visit_invalid_string_escape_sequence_error(self)


@attrs.frozen
class UnclosedStringError(AbstractSyntaxError):
    """
    Error triggered when the closing quote of a string could not be found.
    """

    @typing.override
    def accept[R](self, visitor: SyntaxErrorVisitor[R]) -> R:
        return visitor.visit_unclosed_string_error(self)


@attrs.frozen
class UnexpectedSpecialCharacterInStringError(AbstractSyntaxError):
    """
    Error triggered when a raw special character is used in a non-raw string.
    """

    special_character: str

    @typing.override
    def accept[R](self, visitor: SyntaxErrorVisitor[R]) -> R:
        return visitor.visit_unexpected_special_character_in_string_error(self)


@attrs.frozen
class UnrecognizedCharacterError(AbstractSyntaxError):
    """
    Error triggered when a character that does not exist in the language is
    found in the program.
    """

    unrecognized_character: str

    @typing.override
    def accept[R](self, visitor: SyntaxErrorVisitor[R]) -> R:
        return visitor.visit_unrecognized_character_error(self)


type SyntaxError = (  # noqa: A001
    InvalidStringEscapeSequenceError
    | UnclosedStringError
    | UnexpectedSpecialCharacterInStringError
    | UnrecognizedCharacterError
)


class AbstractGrammarError(AbstractCompilationError):
    """
    Represents an abstract grammar error.
    """

    @abc.abstractmethod
    @typing.override
    def accept[R](self, visitor: GrammarErrorVisitor[R]) -> R:
        pass
