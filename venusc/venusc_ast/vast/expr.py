"""
Venus expression tree
"""

from __future__ import annotations

import abc
import typing

import attrs
import type  # noqa: A004

if typing.TYPE_CHECKING:
    import tokens


class ExprVisitor[R_co](typing.Protocol):
    """
    Interface for visiting the expression tree.
    """

    def visit_annotated_expr(self, expr: AnnotatedExpr) -> R_co:
        """
        Visit an annotated expression.
        """
        ...

    def visit_application_expr(self, expr: ApplicationExpr) -> R_co:
        """
        Visit an application expression.
        """
        ...

    def visit_case_expr(self, expr: CaseExpr) -> R_co:
        """
        Visit a case expression.
        """
        ...

    def visit_dotted_identifier_expr(self, expr: DottedIdentifierExpr) -> R_co:
        """
        Visit a dotted identifier expression.
        """
        ...

    def visit_grouping_expr(self, expr: GroupingExpr) -> R_co:
        """
        Visit a grouping expression.
        """
        ...

    def visit_identifier_expr(self, expr: IdentifierExpr) -> R_co:
        """
        Visit an identifier expression.
        """
        ...

    def visit_if_expr(self, expr: IfExpr) -> R_co:
        """
        Visit an if-then-else expression.
        """
        ...

    def visit_list_expr(self, expr: ListExpr) -> R_co:
        """
        Visit an list literal expression.
        """
        ...

    def visit_literal_expr(self, expr: LiteralExpr) -> R_co:
        """
        Visit an atomic literal expression.
        """
        ...

    def visit_match_expr(self, expr: MatchExpr) -> R_co:
        """
        Visit a match-case-end expression.
        """
        ...

    def visit_tuple_expr(self, expr: TupleExpr) -> R_co:
        """
        Visit a tuple literal expression.
        """
        ...


@attrs.frozen
class AbstractExpr(abc.ABC):
    """
    Represents an abstract expression node.
    """

    span: tuple[int, int]
    type: type.Type = attrs.field(
        kw_only=True,
        factory=lambda: type.TypeVariable(-1),
    )

    @abc.abstractmethod
    def accept[R](self, visitor: ExprVisitor[R]) -> R:
        """
        Accept an expression visitor.
        """


@attrs.frozen
class AnnotatedExpr(AbstractExpr):
    """
    Represents a type-annotated expression.

    ```
    expr: annotation
    ```
    """

    expr: Expr
    annotation: Expr

    @typing.override
    def accept[R](self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_annotated_expr(self)


@attrs.frozen
class ApplicationExpr(AbstractExpr):
    """
    Represents an application (function call) expression.

    ```
    application ...arguments
    ```
    """

    application: Expr
    arguments: list[Expr]

    @typing.override
    def accept[R](self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_application_expr(self)


@attrs.frozen
class CaseExpr(AbstractExpr):
    """
    Represents a case in a match expression.

    ```
    'case' pattern -> branch
    ```
    """

    pattern: Expr
    branch: Expr

    @typing.override
    def accept[R](self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_case_expr(self)


@attrs.frozen
class DottedIdentifierExpr(AbstractExpr):
    """
    Represents a dotted identifier expression.

    ```
    parent.(...attributes)
    ```
    """

    parent: Expr
    attributes: list[IdentifierExpr]

    @typing.override
    def accept[R](self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_dotted_identifier_expr(self)


@attrs.frozen
class GroupingExpr(AbstractExpr):
    """
    Represents a parenthesized expression.

    ```
    (grouped)
    ```
    """

    grouped: Expr

    @typing.override
    def accept[R](self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_grouping_expr(self)


@attrs.frozen
class IdentifierExpr(AbstractExpr):
    """
    Represents an identifier expression.
    """

    token: tokens.Token

    @typing.override
    def accept[R](self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_identifier_expr(self)


@attrs.frozen
class IfExpr(AbstractExpr):
    """
    Represents an if-then-else expression.

    ```
    'if' condition
    'then' then_branch
    'else' else_branch
    ```
    """

    condition: Expr
    then_branch: Expr
    else_branch: Expr

    @typing.override
    def accept[R](self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_if_expr(self)


@attrs.frozen
class ListExpr(AbstractExpr):
    """
    Represents an expression consisting of a list literal.

    ```
    [...items]
    ```
    """

    items: list[Expr]

    @typing.override
    def accept[R](self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_list_expr(self)


@attrs.frozen
class LiteralExpr(AbstractExpr):
    """
    Represents an atomic literal expression.
    """

    token: tokens.Token

    @typing.override
    def accept[R](self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_literal_expr(self)


@attrs.frozen
class MatchExpr(AbstractExpr):
    """
    Represents a match-case-end expression.

    ```
    'match' matched
        ...cases
    'end'
    ```
    """

    matched: Expr
    cases: list[CaseExpr]

    @typing.override
    def accept[R](self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_match_expr(self)


@attrs.frozen
class TupleExpr(AbstractExpr):
    """
    Represents an expression consisting of a tuple literal.

    ```
    (...items)
    ```
    """

    items: list[Expr]

    @typing.override
    def accept[R](self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_tuple_expr(self)


type Expr = (
    AnnotatedExpr
    | ApplicationExpr
    | CaseExpr
    | DottedIdentifierExpr
    | GroupingExpr
    | IdentifierExpr
    | IfExpr
    | ListExpr
    | LiteralExpr
    | MatchExpr
    | TupleExpr
)
