from re import finditer

from tokens import Token
from tokens import TokenStream
from constants import Types
from constants import Keywords

from constants import Regexes
from constants import Type
from constants import Regex
from constants import BASECode

class Parser:

    MAPPINGS: dict[Type, Regex] = {
        # SECTION: Keywords
        Types.ADD: Keywords.ADD,
        Types.CALL: Keywords.CALL,
        Types.DEBUG: Keywords.DEBUG,
        Types.DELETE: Keywords.DELETE,
        Types.ELSE: Keywords.ELSE,
        Types.END: Keywords.END,
        Types.FUNCTION: Keywords.FUNCTION,
        Types.IF: Keywords.IF,
        # NOTE: 'int' needs to go before 'in'
        # in order for the parser to parse correctly
        Types.INT_CAST: Keywords.INT_CAST,
        Types.INPUT: Keywords.INPUT,
        Types.JUMP: Keywords.JUMP,
        Types.LINE_TERMINATOR: Keywords.LINE_TERMINATOR,
        Types.MAIN: Keywords.MAIN,
        Types.OUT: Keywords.OUT,
        Types.POP: Keywords.POP,
        Types.PUSH: Keywords.PUSH,
        Types.RAW_SET: Keywords.RAW_SET,
        Types.RAW_STACK_SET: Keywords.RAW_STACK_SET,
        Types.REFERENCE: Keywords.REFERENCE,
        Types.SET: Keywords.SET,
        Types.START: Keywords.START,
        Types.STOP: Keywords.STOP,
        # !SECTION
        # SECTION: Regexes
        # NOTE: Comments need to go after
        # docstrings in order to parse correctly
        Types.DOCSTRING: Regexes.DOCSTRING,
        Types.COMMENT: Regexes.COMMENT,
        Types.DUMMY: Regexes.DUMMY,
        Types.FLOAT: Regexes.FLOAT,
        Types.FUNCTION_TERMINATOR: Regexes.FUNCTION_TERMINATOR,
        Types.INTEGER: Regexes.INTEGER,
        Types.IDENTIFIER: Regexes.IDENTIFIER,
        Types.SHEBANG: Regexes.SHEBANG,
        Types.STRING: Regexes.STRING,
        Types.WHITESPACE: Regexes.WHITESPACE,
        # !SECTION
        # SECTION: Unmapped
        Types.UNMAPPED: Regexes.UNMAPPED,
        # !SECTION
    }

    @staticmethod
    def parse(basecode: BASECode) -> TokenStream:

        buffer: TokenStream = []

        regex_string: Regex = "|".join(
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
                        token_type,
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
                    token_type,
                    token_string,
                    line,
                    column,
                ),
            )

        return buffer
