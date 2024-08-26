"""
Venus abstract syntax tree
"""

from __future__ import annotations

from vast.expr import Expr
from vast.expr import ExprVisitor
from vast.stmt import Stmt
from vast.stmt import StmtVisitor


class AstVisitor[R_co](StmtVisitor[R_co], ExprVisitor[R_co]):
    """
    Represents an AST visitor.
    """


type AstNode = Expr | Stmt
