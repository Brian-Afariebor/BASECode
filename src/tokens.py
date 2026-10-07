from dataclasses import dataclass
from token_types import Type

type TokenValue = str
type Column = int
type Row = int


@dataclass
class Token:

    value: TokenValue
    type: Type
    row: Row
    column: Column

    def __repr__(self):

        return (
            f"Token '{self.value}' of type {self.type.name}"
            + f" at {self.row},{self.column}"
        )


class TokenStream(list[Token]): ...
