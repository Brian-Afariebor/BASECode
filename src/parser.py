from re import finditer

type BASECode = str
type Regex = str
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

    def __repr__(self) -> str:

        return (
            f"Token of type {self.TYPE}, "
            + f"wtih contents {repr(self.VALUE)}, "
            + f"at {self.LINE},{self.COLUMN}"
        )


class Parser:

    MAPPINGS: dict[BASECode, Regex] = {
        # Specific Expressions
        "END": "end",
        "OUT": "out",
        "SET": "set",
        "RAW_SET": "rset",
        "MAIN": "mn",
        "FUNCTION": "fn",
        "FUNCTION_TERMINATOR":r"\)",
        "LINE_TERMINATOR":r";",
        # General Expressions
        "SHEBANG": r"#!.*\n",
        "DOCSTRING": r"\/\*\*[\s\S]*?\*\/",
        "COMMENT": r"\/\*[\s\S]*?\*\/",
        "FLOAT": r"-?\d+?\.\d+(e\d+)?",
        "INTEGER": r"-?\d+(e\d+)?",
        "IDENTIFIER": r"\w+",
        "STRING": r"\"(?:[^\"]*)\"",
        "WHITESPACE": r"[\s]+",
        "DUMMY": r"\(|{|}|,|=",
        # No Match
        "UNMAPPED": ".",
    }

    @staticmethod
    def parse(basecode: BASECode) -> TokenStream:

        buffer: TokenStream = []

        regex_string: Regex = "|".join(
            f"(?P<{name}>{regex})" for name, regex in Parser.MAPPINGS.items()
        )

        line = 1
        line_start = 0

        for match in finditer(regex_string, basecode):

            token_string = match.group()
            token_type = str(match.lastgroup)
            column = match.start() - line_start + 1

            buffer.append(
                Token(
                    token_type,
                    token_string,
                    line,
                    column,
                ),
            )

            if "\n" in token_string:

                line += token_string.count("\n")
                line_start = match.end()

        return buffer
