"""
Lexer of Venus.
"""

from __future__ import annotations

import typing

import error
import result
import tokens

from lexer.utils import is_identifier

STRING_TERMINATORS = {'"', "\n"}


class Lexer:
    """
    Represents the lexer.

    Given a Venus source string, produce a list of tokens.
    """

    def __init__(self, source: str) -> None:
        self.source: typing.Final = source

        self.start = self.current = 0

    def reset_start(self) -> None:
        """
        Prepare the lexer to scan a new token.
        """

        self.start = self.current

    def is_at_end(self) -> bool:
        """
        Return whether the lexer head is at the end of the source.

        Returns
        -------
        bool
        """

        return self.current >= len(self.source)

    def peek(self) -> str | typing.Literal["\0"]:  # noqa: PYI051
        """
        Peek the source for the current character.

        Returns
        -------
        A null character if there is no more characters in the source.
        Otherwise, the character at the current position.
        """

        if self.is_at_end():
            return "\0"

        return self.source[self.current]

    def advance(self) -> None:
        """
        Advance the lexer by one step.
        """

        self.current += 1

    def consume(self) -> str | typing.Literal["\0"]:  # noqa: PYI051
        """
        Consume the current character of the source.

        Returns
        -------
        The consumed character or null character if there is no more characters
        in the source.
        """

        char = self.peek()
        self.advance()

        return char

    def get_lexeme(self) -> str:
        """
        Return the lexeme of the token currently being processed.

        Returns
        -------
        str
        """

        return self.source[self.start : self.current]

    def get_span(self) -> tuple[int, int]:
        """
        Return the span of the token currently being processed.

        Returns
        -------
        (int, int)
        """

        return (self.start, self.current)

    def scan_identifier(self) -> tokens.TokenKind:
        """
        Scan an identifier (or alike) and return the corresponding token kind.

        Returns
        -------
        TokenKind
        """

        while is_identifier(self.peek()):
            self.advance()

        return tokens.KEYWORD_MAPPING.get(
            self.get_lexeme(),
            tokens.TokenKind.IDENTIFIER,
        )

    def scan_natural(self) -> tokens.TokenKind:
        """
        Scan a natural integer.

        Returns
        -------
        TokenKind
        """

        while self.peek().isdecimal():
            self.advance()

        return tokens.TokenKind.NATURAL

    def scan_string(self) -> result.Result[tokens.TokenKind, error.SyntaxError]:
        """
        Scan a string.

        Returns
        -------
        Either TokenKind or SyntaxError
        """

        while not self.is_at_end() and self.peek() not in STRING_TERMINATORS:
            self.advance()

        if self.is_at_end() or self.peek() == "\n":
            return result.Err(
                error.UnclosedStringError(
                    self.get_span(),
                ),
            )

        self.advance()  # consume the trailing quote

        return result.Ok(tokens.TokenKind.STRING)

    def scan_token(self) -> result.Result[tokens.TokenKind, error.SyntaxError]:  # noqa: C901, PLR0912, PLR0915
        """
        Scan a token.

        Returns
        -------
        Either TokenKind or SyntaxError
        """

        kind: tokens.TokenKind | None = None

        while kind is None:
            match self.consume():
                case "\0":
                    kind = tokens.TokenKind.EOF
                case " " | "\r" | "\t" | "\n":
                    self.reset_start()
                # *- Atoms -* #
                case char if is_identifier(char, first_char=True):
                    kind = self.scan_identifier()
                # *- Groupers -* #
                case "[":
                    kind = tokens.TokenKind.LEFT_BRACKET
                case "(":
                    if self.peek() == ")":
                        self.advance()
                        kind = tokens.TokenKind.UNIT
                    else:
                        kind = tokens.TokenKind.LEFT_PAREN
                case "]":
                    kind = tokens.TokenKind.RIGHT_BRACKET
                case ")":
                    kind = tokens.TokenKind.RIGHT_PAREN
                # *- Literals -* #
                case char if char.isdecimal():
                    kind = self.scan_natural()
                case '"':
                    scan_result = self.scan_string()

                    if isinstance(scan_result, result.Err):
                        return scan_result

                    kind = scan_result.unwrap()
                # *- Operators -* #
                case "^":
                    kind = tokens.TokenKind.CARET
                case "-":
                    if self.peek() == ">":
                        self.advance()
                        kind = tokens.TokenKind.RIGHT_ARROW
                    else:
                        kind = tokens.TokenKind.MINUS
                case "+":
                    kind = tokens.TokenKind.PLUS
                case "/":
                    kind = tokens.TokenKind.SLASH
                case "*":
                    kind = tokens.TokenKind.STAR
                # *- Punctuation -* #
                case ":":
                    if self.peek() == "=":
                        self.advance()
                        kind = tokens.TokenKind.COLON_EQUAL
                    else:
                        kind = tokens.TokenKind.COLON
                case ",":
                    kind = tokens.TokenKind.COMMA
                case "%":
                    kind = tokens.TokenKind.PERCENT
                case ".":
                    kind = tokens.TokenKind.PERIOD
                case ";":
                    kind = tokens.TokenKind.SEMICOLON
                # *- Relations -* #
                case "=":
                    kind = tokens.TokenKind.EQUAL
                case ">":
                    if self.peek() == "=":
                        self.advance()
                        kind = tokens.TokenKind.GREATER_EQUAL
                    else:
                        kind = tokens.TokenKind.GREATER
                case "<":
                    if self.peek() == "=":
                        self.advance()
                        kind = tokens.TokenKind.LESS_EQUAL
                    else:
                        kind = tokens.TokenKind.LESS
                case char:
                    return result.Err(
                        error.UnrecognizedCharacterError(
                            self.get_span(),
                            char,
                        ),
                    )

        return result.Ok(kind)

    def build_token(self, kind: tokens.TokenKind) -> tokens.Token:
        """
        Build a token from its kind.

        Returns
        -------
        The token.
        """

        return tokens.Token(kind, self.get_lexeme(), self.start)

    def lex(self) -> result.Result[list[tokens.Token], error.SyntaxError]:
        """
        Scan the tokens.

        Returns
        -------
        Either the list of tokens or a syntax error.
        """

        token_list: list[tokens.Token] = []

        while not self.is_at_end():
            self.reset_start()

            scan_result = self.scan_token()

            if isinstance(scan_result, result.Err):
                return scan_result

            token_list.append(self.build_token(scan_result.unwrap()))

        self.reset_start()
        token_list.append(self.build_token(tokens.TokenKind.EOF))

        return result.Ok(token_list)
