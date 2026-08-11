from re import finditer

from tokens import Token
from tokens import TokenStream
from constants import Constants

type BASECode = str
type Regex = str


class Parser:

    MAPPINGS: dict[BASECode, Regex] = {
        # Keywords
        Constants.Types.ADD: Constants.Keywords.ADD,
        Constants.Types.CALL: Constants.Keywords.CALL,
        Constants.Types.DELETE: Constants.Keywords.DELETE,
        Constants.Types.ELSE: Constants.Keywords.ELSE,
        Constants.Types.END: Constants.Keywords.END,
        Constants.Types.FUNCTION: Constants.Keywords.FUNCTION,
        Constants.Types.IF: Constants.Keywords.IF,
        # int needs to go before in in order for the parser to parse correctly
        Constants.Types.INT_CAST: Constants.Keywords.INT_CAST,
        Constants.Types.INPUT: Constants.Keywords.INPUT,
        Constants.Types.JUMP: Constants.Keywords.JUMP,
        Constants.Types.LINE_TERMINATOR: Constants.Keywords.LINE_TERMINATOR,
        Constants.Types.MAIN: Constants.Keywords.MAIN,
        Constants.Types.OUT: Constants.Keywords.OUT,
        Constants.Types.RAW_SET: Constants.Keywords.RAW_SET,
        Constants.Types.REFERENCE: Constants.Keywords.REFERENCE,
        Constants.Types.SET: Constants.Keywords.SET,
        Constants.Types.START: Constants.Keywords.START,
        Constants.Types.STOP: Constants.Keywords.STOP,
        Constants.Types.DELETE: Constants.Keywords.DELETE,
        # Regexes
        Constants.Types.DOCSTRING: Constants.Regexes.DOCSTRING,
        Constants.Types.COMMENT: Constants.Regexes.COMMENT,
        Constants.Types.DUMMY: Constants.Regexes.DUMMY,
        Constants.Types.FLOAT: Constants.Regexes.FLOAT,
        Constants.Types.FUNCTION_TERMINATOR: Constants.Regexes.FUNCTION_TERMINATOR,
        # * Fixes bugs with integer parsing
        Constants.Types.INTEGER: Constants.Regexes.INTEGER,
        Constants.Types.IDENTIFIER: Constants.Regexes.IDENTIFIER,
        Constants.Types.SHEBANG: Constants.Regexes.SHEBANG,
        Constants.Types.STRING: Constants.Regexes.STRING,
        Constants.Types.WHITESPACE: Constants.Regexes.WHITESPACE,
        # Unmapped
        Constants.Types.UNMAPPED: Constants.Regexes.UNMAPPED,
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

            if "\n" in token_string:

                line += token_string.count("\n")
                lines = token_string.split("\n")
                line_start = match.end()

                if len(lines) >= 1:

                    line_start -= len(lines[-1])

                column = 0

            buffer.append(
                Token(
                    token_type,
                    token_string,
                    line,
                    column,
                ),
            )

        return buffer
