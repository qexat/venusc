"""
Entry point for the lexer interactive loop.
"""

from __future__ import annotations

import contextlib
import sys

import result

from lexer import Lexer


def main() -> None:
    """
    Small interactive loop for the lexer.
    """

    with contextlib.suppress(ModuleNotFoundError):
        import readline  # noqa: F401, PLC0415 # pyright: ignore[reportUnusedImport]

    try:
        while True:
            line = input("\x1b[34m>\x1b[39m ")

            lexing_result = Lexer(line).lex()

            match lexing_result:
                case result.Ok(token_list):
                    for token in token_list:
                        # TODO: use tokens.renderer
                        print(token)  # noqa: T201
                case result.Err(error):
                    # TODO: use error.renderer
                    print(error, file=sys.stderr)  # noqa: T201
    except (KeyboardInterrupt, EOFError):
        return


if __name__ == "__main__":
    main()
