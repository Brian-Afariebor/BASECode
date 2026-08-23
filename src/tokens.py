from __future__ import annotations
from constants import Type

type BASECode = str
type TokenStream = list[Token]


class Token:

    def __init__(
        self,
        type: Type,
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
