from collections.abc import Callable
from execution_modes import ExecutionMode
from tokens import TokenStream
from typing import Self

type TokenFilter = Callable[[TokenStream], TokenStream]


class Filter:

    _filters: dict[ExecutionMode, TokenFilter] = {}

    @classmethod
    def register(
        cls,
        mode: ExecutionMode,
        filter: TokenFilter,
    ) -> type[Self]:

        cls._filters[mode] = filter
        return cls

    @classmethod
    def filter(
        cls,
        mode: ExecutionMode,
        tokens: TokenStream,
    ) -> TokenStream | None:

        if mode in cls._filters:

            return cls._filters[mode](tokens)

        return None
