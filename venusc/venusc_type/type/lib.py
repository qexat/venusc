"""
Definition of the type tree.
"""

from __future__ import annotations

import abc
import typing

import attrs

if typing.TYPE_CHECKING:
    from type.kind import PrimitiveKind


class TypeVisitor[R_co](typing.Protocol):
    """
    Interface for visiting a type tree.
    """

    def visit_application_type(self, typ: ApplicationType) -> R_co:
        """
        Visit an application type.
        """
        ...

    def visit_primitive_type(self, typ: PrimitiveType) -> R_co:
        """
        Visit a primitive type.
        """
        ...

    def visit_product_type(self, typ: ProductType) -> R_co:
        """
        Visit a product type.
        """
        ...

    def visit_sum_type(self, typ: SumType) -> R_co:
        """
        Visit a sum type.
        """
        ...

    def visit_type_variable(self, typ: TypeVariable) -> R_co:
        """
        Visit a type variable.
        """
        ...


@attrs.frozen
class AbstractType(abc.ABC):
    """
    Represents an abstract tree. Top node of the type tree.
    """

    @abc.abstractmethod
    def accept[R](self, visitor: TypeVisitor[R]) -> R:
        """
        Accept a type visitor.
        """


@attrs.frozen
@typing.final
class ApplicationType(AbstractType):
    """
    Represents the type of an application (also called "function").

    An application having more than parameter is a function that takes one
    argument and returns an application taking the rest, like in lambda
    calculus.
    """

    parameter: Type
    applied: Type

    @typing.override
    def accept[R](self, visitor: TypeVisitor[R]) -> R:
        return visitor.visit_application_type(self)


@attrs.frozen
@typing.final
class PrimitiveType(AbstractType):
    """
    Represents a primitive type such as `Integer`, `Boolean`, `String`...
    """

    kind: PrimitiveKind

    @typing.override
    def accept[R](self, visitor: TypeVisitor[R]) -> R:
        return visitor.visit_primitive_type(self)


@attrs.frozen
@typing.final
class ProductType(AbstractType):
    """
    Represents the monoidal product of two types.
    """

    left: Type
    right: Type

    @typing.override
    def accept[R](self, visitor: TypeVisitor[R]) -> R:
        return visitor.visit_product_type(self)


@attrs.frozen
@typing.final
class SumType(AbstractType):
    """
    Represents the commutative monoidal sum of two types.
    """

    left: Type
    right: Type

    @typing.override
    def accept[R](self, visitor: TypeVisitor[R]) -> R:
        return visitor.visit_sum_type(self)


@attrs.frozen
@typing.final
class TypeVariable(AbstractType):
    """
    Represents a type variable.

    It is uniquely defined by a number: if two type variables have the same
    number, then they are identical. However, two type variables with different
    numbers might still be equivalent.
    """

    identifier: int

    @typing.override
    def accept[R](self, visitor: TypeVisitor[R]) -> R:
        return visitor.visit_type_variable(self)


type Type = (
    ApplicationType | PrimitiveType | ProductType | SumType | TypeVariable
)
