from re import finditer

from tokens import Token
from tokens import TokenStream
from constants import Constants

type BASECode = str
type Regex = str


class Parser:

    MAPPINGS: dict[BASECode, Regex] = {

        # Keywords
        Constants.START_TYPE: Constants.START_KEYWORD,
        Constants.STOP_TYPE: Constants.STOP_KEYWORD,
        Constants.RAW_SET_TYPE: Constants.RAW_SET_KEYWORD,
        Constants.JUMP_TYPE: Constants.JUMP_KEYWORD,
        Constants.END_TYPE: Constants.END_KEYWORD,
        Constants.OUT_TYPE: Constants.OUT_KEYWORD,
        Constants.SET_TYPE: Constants.SET_KEYWORD,
        Constants.MAIN_TYPE: Constants.MAIN_KEYWORD,
        Constants.FUNCTION_TYPE: Constants.FUNCTION_KEYWORD,
        Constants.FUNCTION_TERMINATOR_TYPE: Constants.FUNCTION_TERMINATOR_REGEX,
        Constants.LINE_TERMINATOR_TYPE: Constants.LINE_TERMINATOR,

        # General Expressions
        Constants.SHEBANG_TYPE: Constants.SHEBANG_REGEX,
        Constants.DOCSTRING_TYPE: Constants.DOCSTRING_REGEX,
        Constants.COMMENT_TYPE: Constants.COMMENT_REGEX,
        Constants.FLOAT_TYPE: Constants.FLOAT_REGEX,
        Constants.INTEGER_TYPE: Constants.INTEGER_REGEX,
        Constants.IDENTIFIER_TYPE: Constants.IDENTIFIER_REGEX,
        Constants.STRING_TYPE: Constants.STRING_REGEX,
        Constants.WHITESPACE_TYPE: Constants.WHITESPACE_REGEX,
        Constants.DUMMY_TYPE: Constants.DUMMY_REGEX,
        
        # No Match
        Constants.UNMAPPED_TYPE: Constants.UNMAPPED_REGEX,
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
