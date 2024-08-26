"""
Venus statement tree
"""

from __future__ import annotations

import abc
import typing

import attrs

if typing.TYPE_CHECKING:
    from .expr import DottedIdentifierExpr
    from .expr import Expr
    from .expr import IdentifierExpr


class StmtVisitor[R_co](typing.Protocol):
    """
    Interface for visiting the statement tree.
    """

    def visit_fix_stmt(self, stmt: FixStmt) -> R_co:
        """
        Visit a fix definition stmt.
        """
        ...

    def visit_let_stmt(self, stmt: LetStmt) -> R_co:
        """
        Visit a let assignment stmt.
        """
        ...

    def visit_use_stmt(self, stmt: UseStmt) -> R_co:
        """
        Visit a use import stmt.
        """
        ...


@attrs.frozen
class AbstractStmt(abc.ABC):
    """
    Represents an abstract statement node.
    """

    span: tuple[int, int]

    @abc.abstractmethod
    def accept[R](self, visitor: StmtVisitor[R]) -> R:
        """
        Accept a statement visitor.
        """


@attrs.frozen
class FixStmt(AbstractStmt):
    """
    Represents a fix definition statement.

    ```
    'fix' target ...parameters :=
        definition
    'where' ...constraints;
    ```
    """

    target: IdentifierExpr
    parameters: list[IdentifierExpr]  # TODO: allow more types
    definition: Expr
    constraints: list[Expr]

    @typing.override
    def accept[R](self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_fix_stmt(self)


@attrs.frozen
class LetStmt(AbstractStmt):
    """
    Represents a let assignment statement.

    ```
    'let' target := definition;
    ```
    """

    target: IdentifierExpr  # TODO: allow more types
    definition: Expr

    @typing.override
    def accept[R](self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_let_stmt(self)


@attrs.frozen
class UseStmt(AbstractStmt):
    """
    Represents a use import statement.

    ```
    'use' source;
    ```
    """

    source: DottedIdentifierExpr

    @typing.override
    def accept[R](self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_use_stmt(self)


type Stmt = FixStmt | LetStmt | UseStmt
