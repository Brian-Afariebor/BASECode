from re import finditer

from tokens import Token
from tokens import TokenStream
from constants import Type
from constants import Keyword

from constants import Regex
from constants import Type
from constants import Regex
from constants import BASECode


class Parser:

    MAPPINGS: dict[Type, Regex | Keyword] = {
        # SECTION: Keywords
        Type.ADD: Keyword.ADD,
        Type.CALL: Keyword.CALL,
        Type.DEBUG: Keyword.DEBUG,
        Type.DELETE: Keyword.DELETE,
        Type.ELSE: Keyword.ELSE,
        Type.END: Keyword.END,
        Type.FUNCTION: Keyword.FUNCTION,
        Type.IF: Keyword.IF,
        # NOTE: 'int' needs to go before 'in'
        # in order for the parser to parse correctly
        Type.INT_CAST: Keyword.INT_CAST,
        Type.INPUT: Keyword.INPUT,
        Type.JUMP: Keyword.JUMP,
        Type.LINE_TERMINATOR: Keyword.LINE_TERMINATOR,
        Type.MAIN: Keyword.MAIN,
        Type.OUT: Keyword.OUT,
        Type.POP: Keyword.POP,
        Type.PUSH: Keyword.PUSH,
        Type.RAW_SET: Keyword.RAW_SET,
        Type.RAW_STACK_SET: Keyword.RAW_STACK_SET,
        Type.REFERENCE: Keyword.REFERENCE,
        Type.REMOVE: Keyword.REMOVE,
        Type.RETURN: Keyword.RETURN,
        Type.SET: Keyword.SET,
        Type.START: Keyword.START,
        Type.STOP: Keyword.STOP,
        # !SECTION
        # SECTION: Regexes
        # NOTE: Comments need to go after
        # docstrings in order to parse correctly
        Type.DOCSTRING: Regex.DOCSTRING,
        Type.COMMENT: Regex.COMMENT,
        Type.DUMMY: Regex.DUMMY,
        Type.FLOAT: Regex.FLOAT,
        Type.FUNCTION_TERMINATOR: Regex.FUNCTION_TERMINATOR,
        Type.INTEGER: Regex.INTEGER,
        Type.IDENTIFIER: Regex.IDENTIFIER,
        Type.SHEBANG: Regex.SHEBANG,
        Type.STRING: Regex.STRING,
        Type.WHITESPACE: Regex.WHITESPACE,
        # !SECTION
        # SECTION: Unmapped
        Type.UNMAPPED: Regex.UNMAPPED,
        # !SECTION
    }

    @staticmethod
    def parse(basecode: BASECode) -> TokenStream:

        buffer: TokenStream = []

        regex_string = "|".join(
            f"(?P<{type}>{regex})" for type, regex in Parser.MAPPINGS.items()
        )

        line = 1
        line_start = 0

        for match in finditer(regex_string, basecode):

            token_string = match.group()
            token_type = str(match.lastgroup)
            column = match.start() - line_start + 1

            if "\n" not in token_string:

                buffer.append(
                    Token(
                        token_type,  # pyright: ignore[reportArgumentType]
                        token_string,
                        line,
                        column,
                    ),
                )
                continue

            line += token_string.count("\n")
            lines = token_string.splitlines()
            line_start = match.end()

            if len(lines) >= 1:

                line_start -= len(lines[-1])

            buffer.append(
                Token(
                    token_type,  # pyright: ignore[reportArgumentType]
                    token_string,
                    line,
                    column,
                ),
            )

        return buffer
