from re import finditer

from tokens import Token
from tokens import TokenStream
from constants import Constants

type BASECode = str
type Regex = str


class Parser:

    MAPPINGS: dict[BASECode, Regex] = {

        # Keywords
        Constants.Types.START: Constants.Keywords.START,
        Constants.Types.STOP: Constants.Keywords.STOP,
        Constants.Types.RAW_SET: Constants.Keywords.RAW_SET,
        Constants.Types.JUMP: Constants.Keywords.JUMP,
        Constants.Types.DELETE: Constants.Keywords.DELETE,
        Constants.Types.END: Constants.Keywords.END,
        Constants.Types.OUT: Constants.Keywords.OUT,
        Constants.Types.SET: Constants.Keywords.SET,
        Constants.Types.MAIN: Constants.Keywords.MAIN,
        Constants.Types.FUNCTION: Constants.Keywords.FUNCTION,
        Constants.Types.FUNCTION_TERMINATOR: Constants.Regexes.FUNCTION_TERMINATOR,
        Constants.Types.LINE_TERMINATOR: Constants.Keywords.LINE_TERMINATOR,

        # General Expressions
        Constants.Types.SHEBANG: Constants.Regexes.SHEBANG,
        Constants.Types.DOCSTRING: Constants.Regexes.DOCSTRING,
        Constants.Types.COMMENT: Constants.Regexes.COMMENT,
        Constants.Types.FLOAT: Constants.Regexes.FLOAT,
        Constants.Types.INTEGER: Constants.Regexes.INTEGER,
        Constants.Types.IDENTIFIER: Constants.Regexes.IDENTIFIER,
        Constants.Types.STRING: Constants.Regexes.STRING,
        Constants.Types.WHITESPACE: Constants.Regexes.WHITESPACE,
        Constants.Types.DUMMY: Constants.Regexes.DUMMY,

        # No Match
        Constants.Types.UNMAPPED: Constants.Regexes.UNMAPPED,
    }

    @staticmethod
    def parse(basecode: BASECode) -> TokenStream:

        buffer: TokenStream = []

        regex_string: Regex = "|".join(
            f"(?P<{name}>{regex})" for name, regex in Parser.MAPPINGS.items()
        )

        line = 1
        line_START = 0

        for match in finditer(regex_string, basecode):

            token_string = match.group()
            token_type = str(match.lastgroup)
            column = match.start() - line_START + 1

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
                line_START = match.end()

        return buffer