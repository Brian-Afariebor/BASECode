from re import finditer

from regexes import Regex

from tokens import Token
from tokens import TokenStream

from token_types import Type

type BASECodeCode = str


class Parser:

    _mappings: dict[Type, Regex] = {}

    @classmethod
    def get_regex_string(cls):

        regex = ""

        for type, regex in cls._mappings.items():

            regex += f"(?P<{type._name_}>{regex})"
            regex += "|"

        alligned_regex = regex[:-1]

        return alligned_regex

    @classmethod
    def parse(cls, code: BASECodeCode) -> TokenStream:

        buffer: TokenStream = []

        regex_string = cls.get_regex_string()

        line = 1
        line_start = 0

        for match in finditer(regex_string, code):

            token_string = match.group()
            token_type = Type[str(match.lastgroup)]
            column = match.start() - line_start + 1

            if "\n" not in token_string:

                buffer.append(
                    Token(
                        token_string,
                        token_type,
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
                    token_string,
                    token_type,
                    line,
                    column,
                ),
            )

        return buffer

    @classmethod
    def register_regex(cls, type: Type, regex: Regex):

        cls._mappings[type] = regex
        return cls
