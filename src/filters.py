from execution_modes import ExecutionMode

from filter import Filter
from filter import FilteredTokenStream
from filter import UnfilteredTokenSream

from token_types import Type

NORMAL_FIlTER_TYPES = [
    Type.DUMMY,
    Type.WHITESPACE,
]


def register_all():

    Filter.register(ExecutionMode.NORMAL, normal_filter)


def normal_filter(
    token_stream: UnfilteredTokenSream,
) -> FilteredTokenStream:

    filtered_list = [
        token for token in token_stream if token.type not in NORMAL_FIlTER_TYPES
    ]

    return FilteredTokenStream(filtered_list)
