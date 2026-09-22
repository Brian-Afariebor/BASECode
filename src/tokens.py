from dataclasses import dataclass
from token_types import Type

@dataclass
class Token:

    value: str
    type: Type
    row: int
    column: int


type TokenStream = list[Token]
