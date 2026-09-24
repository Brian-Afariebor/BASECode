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


type TokenStream = list[Token]
