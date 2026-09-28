from collections.abc import Callable

from states import State

from tokens import Token

type Implementation = Callable[[State, Token],State]