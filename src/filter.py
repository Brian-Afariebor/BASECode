from collections.abc import Callable
from execution_modes import Mode
from tokens import TokenStream
from typing import Self


type UnfilteredTokenSream = TokenStream

class FilteredTokenStream(TokenStream): ...


type TokenFilter = Callable[[UnfilteredTokenSream], FilteredTokenStream]


class Filter:

    _filters: dict[Mode, TokenFilter] = {}

    @classmethod
    def register(
        cls,
        mode: Mode,
        filter: TokenFilter,
    ) -> type[Self]:

        cls._filters[mode] = filter
        return cls

    @classmethod
    def filter(
        cls,
        tokens: UnfilteredTokenSream,
        mode: Mode = Mode.NORMAL,
    ) -> FilteredTokenStream | None:

        if mode not in cls._filters:

            return None

        return cls._filters[mode](tokens)
