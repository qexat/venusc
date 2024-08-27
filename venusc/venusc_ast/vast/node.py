"""
Venus abstract syntax tree
"""

from __future__ import annotations

import attrs

from vast.expr import Expr
from vast.expr import ExprVisitor
from vast.stmt import Stmt
from vast.stmt import StmtVisitor


class AstVisitor[R_co](StmtVisitor[R_co], ExprVisitor[R_co]):
    """
    Represents an AST visitor.
    """


@attrs.frozen
class Topnode:
    """
    Represents the top node of an AST.
    """

    statements: list[Stmt]


type AstNode = Expr | Stmt
