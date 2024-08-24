"""
Utils for the type tree.
"""

from __future__ import annotations

import typing

from .kind import PrimitiveKind
from .lib import ApplicationType
from .lib import PrimitiveType
from .lib import ProductType
from .lib import SumType
from .lib import Type
from .lib import TypeVariable

# *- Predicates -* #


def is_atomic(typ: Type) -> bool:
    """
    Return whether the type `typ` is atomic or not.

    Returns
    -------
    bool
    """

    match typ:
        case ApplicationType() | ProductType() | SumType():
            return False
        case PrimitiveType() | TypeVariable():
            return True


def is_never(typ: Type) -> typing.TypeGuard[PrimitiveType]:
    """
    Return whether the type `typ` is the empty type or not.

    Returns
    -------
    bool
    """

    return isinstance(typ, PrimitiveType) and typ.kind is PrimitiveKind.NEVER


def is_unit(typ: Type) -> typing.TypeGuard[PrimitiveType]:
    """
    Return whether the type `typ` is the unit type or not.

    Returns
    -------
    bool
    """

    return isinstance(typ, PrimitiveType) and typ.kind is PrimitiveKind.UNIT


# *- Constructors -* #


def make_application_from_signature(
    *parameters: *tuple[Type, *tuple[Type, ...]],
    return_type: Type,
) -> ApplicationType:
    """
    Construct an application type given its parameter and return types.

    Returns
    -------
    The application type.
    """

    ##########################################################################
    # Process                                                                #
    # -------                                                                #
    # 1. We start by creating `first -> return_type`.                        #
    # 2. In reverse order (as `->` is right-associative), we insert the      #
    #    last parameter as the first of the returned application.            #
    #      `first -> (last -> return_type)`                                  #
    # 3. We continue to do that for each parameter:                          #
    #      `first -> (second_last -> (last -> return_type))`                 #
    # And so on.                                                             #
    ##########################################################################

    first, *rest = parameters
    result = ApplicationType(first, return_type)

    for parameter in reversed(rest):
        result = ApplicationType(
            first,
            ApplicationType(parameter, result.applied),
        )

    return result


def make_factorial_type(*types: Type) -> Type:
    """
    Recursively create a new factorial type.

    Formally, a factorial type is the result of a product fold over a list of
    types.

    Returns
    -------
    Unit
        If no type is provided.
    Type
        If one type is provided.
    Product Type (simplified)
        If several types are provided.
    """

    match types:
        case ():
            return PrimitiveType(PrimitiveKind.UNIT)
        case (first,):
            return first
        case _:
            first, *rest = types

            return simplify(ProductType(first, make_factorial_type(*rest)))


# *- Solving utils -* #


def simplify(typ: Type) -> Type:
    """
    Simplify the type `typ` by removing identities and redundant terms.

    Returns
    -------
    Type
        The simplied version of the type.
    """

    match typ:
        case ApplicationType(parameter, applied):
            return ApplicationType(simplify(parameter), simplify(applied))
        case ProductType(left, right):
            sleft = simplify(left)
            sright = simplify(right)

            # If any of the terms is the empty type, then the product type can
            # be simplified to the empty type
            if is_never(sleft) or is_never(sright):
                simplified = PrimitiveType(PrimitiveKind.NEVER)
            # If the right term is the identity (unit type), then the product
            # can be simplified to the left term
            elif is_unit(sright):
                simplified = sleft
            # If the left term is the identity (unit type), then the product can
            # be simplified to the right term
            elif is_unit(sleft):
                simplified = sright
            else:
                simplified = ProductType(sleft, sright)

            return simplified

        case SumType(left, right):
            sleft = simplify(left)
            sright = simplify(right)

            # If the right term is the identity (empty type), then the sum can
            # be simplified to the left term
            if is_never(sright):
                simplified = sleft
            # If the left term is the identity (empty type), then the sum can
            # be simplified to the right term
            elif is_never(sleft):
                simplified = sright
            else:
                simplified = SumType(sleft, sright)

            return simplified
        case PrimitiveType() | TypeVariable():
            return typ
