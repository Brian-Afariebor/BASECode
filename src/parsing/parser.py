from re import finditer


class Token:

    def __init__(self, type: str, contents: str, line: int, column: int):

        self.TYPE = type
        self.CONTENTS = contents
        self.LINE = line
        self.COLUMN = column

    def __repr__(self) -> str:

        return (
            f"Token of type {self.TYPE}, "
            + f"wtih contents {repr(self.CONTENTS)}, "
            + f"at {self.LINE},{self.COLUMN}"
        )


class BASECodeParser:

    MAPPINGS = {
        "OUT": "out",
        "STRING": r"\"(?:[^\"]*)\"",
        "WHITESPACE": r"\s+",
        "UNMAPPED": ".+",
    }

    @staticmethod
    def parse(basecode: str):

        buffer: list[Token] = []

        regex_string = "|".join(
            f"(?P<{name}>{regex})" for name, regex in BASECodeParser.MAPPINGS.items()
        )

        line = 1
        line_start = 0
        for match in finditer(regex_string, basecode):

            token_string = match.group()
            token_type = str(match.lastgroup)
            column = match.start() - line_start

            buffer.append(Token(token_type, token_string, line, column))

            if "\n" in token_string:

                line += token_string.count("\n")
                line_start = match.end()

        return buffer
