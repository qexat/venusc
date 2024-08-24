"""
Various utils for lexing.
"""

from __future__ import annotations


def is_identifier(char: str, *, first_char: bool = False) -> bool:
    """
    Return whether `char` is a valid character of an identifier.

    Parameters
    ----------
    char : str
        The character to check.
    first_char : bool = False
        Whether the character is the first one of the identifier.

    Returns
    -------
    bool
    """

    return (
        char == "_"
        or "A" <= char <= "Z"
        or "a" <= char <= "z"
        or ("0" <= char <= "9" and not first_char)
    )
