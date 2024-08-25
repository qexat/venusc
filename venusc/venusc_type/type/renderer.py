# pyright: reportUnusedCallResult = false, reportImportCycles = false

"""
Renderer for types.
"""

from __future__ import annotations

import io
import typing

from .lib import ApplicationType
from .lib import PrimitiveType
from .lib import ProductType
from .lib import TypeVisitor
from .utils import is_atomic


class TypeRenderer(TypeVisitor[str]):
    """
    Renderer for types.
    """

    # TODO: move this method to a dedicated colorer class
    def render_type_name(self, name: str) -> str:  # noqa: PLR6301
        """
        Render a type name.

        Returns
        -------
        str
        """

        return f"\x1b[38;2;183;137;46m{name}\x1b[39m"

    # TODO: move this method to a dedicated colorer class
    def render_type_variable_name(self, name: str) -> str:  # noqa: PLR6301
        """
        Render a type variable name.

        Returns
        -------
        str
        """

        return f"\x1b[38;2;204;76;51m{name}\x1b[39m"

    @typing.override
    def visit_application_type(self, typ: ApplicationType) -> str:
        buffer = io.StringIO()

        parameter = typ.parameter.accept(self)
        applied = typ.applied.accept(self)

        is_parameter_atomic = is_atomic(typ.parameter)

        if not is_parameter_atomic:
            buffer.write("(")

        buffer.write(parameter)

        if not is_parameter_atomic:
            buffer.write(")")

        buffer.write(" -> ")
        buffer.write(applied)

        return buffer.getvalue()

    @typing.override
    def visit_primitive_type(self, typ: PrimitiveType) -> str:
        return self.render_type_name(typ.kind.real_name)

    @typing.override
    def visit_product_type(self, typ: ProductType) -> str:
        buffer = io.StringIO()

        left = typ.left.accept(self)
        right = typ.right.accept(self)

        left_parenthesized = not (
            is_atomic(typ.left) or isinstance(typ.left, ProductType)
        )
        right_parenthesized = not (
            is_atomic(typ.right) or isinstance(typ.right, ProductType)
        )

        if left_parenthesized:
            buffer.write("(")

        buffer.write(left)

        if left_parenthesized:
            buffer.write(")")

        buffer.write(", ")

        if right_parenthesized:
            buffer.write("(")

        buffer.write(right)

        if right_parenthesized:
            buffer.write(")")

        return buffer.getvalue()
