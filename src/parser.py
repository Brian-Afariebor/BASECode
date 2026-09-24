from tokens import Token
from tokens import TokenStream
from token_types import Type
from regexes import Regex

type BASECodeCode = str


class Parser:

    _mappings: dict[Type, Regex] = {}

    @classmethod
    def register_regex(cls, type: Type, regex: Regex):

        cls._mappings[type] = regex
        return cls

    # TODO -  Implement this method
    @classmethod
    def parse(cls, code: BASECodeCode) -> TokenStream: ...
