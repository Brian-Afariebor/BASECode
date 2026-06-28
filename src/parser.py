from re import finditer

from tokens import Token
from tokens import TokenStream
from tokens import TokenType

type BASECode = str
type Regex = str


class Parser:

    MAPPINGS: dict[BASECode, Regex] = {
        # Specific Expressions
        TokenType.RAW_SET: "rset",
        TokenType.JUMP: "jmp",
        TokenType.END: "end",
        TokenType.OUT: "out",
        TokenType.SET: "set",
        TokenType.MAIN: "mn",
        TokenType.FUNCTION: "fn",
        TokenType.FUNCTION_TERMINATOR: r"\)",
        TokenType.LINE_TERMINATOR: r";",
        # General Expressions
        TokenType.SHEBANG: r"#!.*\n",
        TokenType.DOCSTRING: r"\/\*\*[\s\S]*?\*\/",
        TokenType.COMMENT: r"\/\*[\s\S]*?\*\/",
        TokenType.FLOAT: r"-?\d+?\.\d+(e\d+)?",
        TokenType.INTEGER: r"-?\d+(e\d+)?",
        TokenType.IDENTIFIER: r"[\w:]+",
        TokenType.STRING: r"\"(?:[^\"]*)\"",
        TokenType.WHITESPACE: r"[\s]+",
        TokenType.DUMMY: r"\(|{|}|,|=",
        # No Match
        TokenType.UNMAPPED: ".",
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
