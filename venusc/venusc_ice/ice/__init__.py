"""
Definition of the Internal Compiler Error (ICE) system.
"""

from __future__ import annotations


# FIXME: for now, internal errors are just a class of Python exceptions.
# FIXME: in the future, they will be their own data type.
class InternalError(RuntimeError):
    """
    Represents an internal compiler error.
    """
