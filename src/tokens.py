from __future__ import annotations

type BASECode = str
type TokenStream = list[Token]


class Token:

    def __init__(
        self,
        type: str,
        contents: BASECode,
        line: int,
        column: int,
    ):

        self.TYPE = type
        self.VALUE = contents
        self.LINE = line
        self.COLUMN = column

    def __eq__(self, other: object):

        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:

        return (
            f"Token of type {self.TYPE}, "
            + f"wtih contents {repr(self.VALUE)}, "
            + f"at {self.LINE},{self.COLUMN}"
        )


class TokenType:

    RAW_SET = "RAW_SET"
    JUMP = "JUMP"
    END = "END"
    OUT = "OUT"
    SET = "SET"
    MAIN = "MAIN"
    FUNCTION = "FUNCTION"
    FUNCTION_TERMINATOR = "FUNCTION_TERMINATOR"
    LINE_TERMINATOR = "LINE_TERMINATOR"
    SHEBANG = "SHEBANG"
    DOCSTRING = "DOCSTRING"
    COMMENT = "COMMENT"
    FLOAT = "FLOAT"
    INTEGER = "INTEGER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    WHITESPACE = "WHITESPACE"
    DUMMY = "DUMMY"
    UNMAPPED = "UNMAPPED"
