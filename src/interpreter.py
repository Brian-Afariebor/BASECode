from abc import ABC
from collections.abc import Callable
from errors import BASECodeRuntimeError
from errors import EndOfCodeError
from errors import InvalidTokenError
from execution_modes import ExecutionMode
from filter import FilteredTokenStream

from states import Position
from states import PositionId
from states import State

from tokens import Token
from token_types import Type


class Interpreter(ABC):

    type Implementation = Callable[[PositionId, State, Interpreter], State]

    _mappings: dict[tuple[ExecutionMode, Type], Implementation] = {}
    _state: State

    MAIN_POSITION_ID: PositionId = "main"
    MAIN_POSITION_START: Position = 0

    @classmethod
    def generate_state(
        cls,
        tokens: FilteredTokenStream,
        mode: ExecutionMode = ExecutionMode.NORMAL,
    ):

        state = State(tokens, mode).set_position(
            cls.MAIN_POSITION_ID,
            cls.MAIN_POSITION_START,
        )

        if state is None:

            raise BASECodeRuntimeError("Default main position is not valid")

        return state

    @classmethod
    def get_implemenation_from_token(
        cls,
        token: Token,
        mode: ExecutionMode = ExecutionMode.NORMAL,
    ):
        """Gets the implentation of a token.

        Args:
            token (Token): The token to get the implementation of.
            mode (ExecutionMode, optional):
                The execution mode us the interpreter.
                Defaults to ExecutionMode.NORMAL.

        Returns:
            Implementation | None:
                The implementation from the token.
                The mode shifts to ExecutionMode.NORMAL
                    if the given mode is not registered
                    but the normal one is.

                Retuns None if both of these fail.
        """

        type = token.type

        key = (mode, type)

        if key in cls._mappings:

            return cls._mappings[key]

        # NOTE - The default mode for a non-found extra mode is NORMAL

        key = (ExecutionMode.NORMAL, type)

        if key not in cls._mappings:

            return None

        return cls._mappings[key]

    @classmethod
    def register(
        cls,
        implementation: Implementation,
        type: Type,
        mode: ExecutionMode = ExecutionMode.NORMAL,
    ):
        """Registers a new implementation.

        Args:
            implementation (Implementation): The type implementation.
            type (Type): The type that is being implemented.
            mode (ExecutionMode, optional):
                The intended execution mode.
                Defaults to ExecutionMode.NORMAL.

        Returns:
            type[Self]: The class; for chaining.
        """

        cls._mappings[(mode, type)] = implementation

        return cls

    @classmethod
    def run(
        cls,
        tokens: FilteredTokenStream,
        mode: ExecutionMode = ExecutionMode.NORMAL,
    ):

        interpreter = Interpreter(tokens, mode)

        return interpreter.run_position(cls.MAIN_POSITION_ID)

    def __init__(
        self,
        tokens: FilteredTokenStream,
        mode: ExecutionMode = ExecutionMode.NORMAL,
    ):

        self._state = Interpreter.generate_state(tokens, mode)

    def run_position(
        self,
        position_id: PositionId,
    ):

        while self._state.registered_position_id(position_id):

            token = self._state.get_token_at_position_id(position_id)

            if token is None:

                raise BASECodeRuntimeError(
                    f"Position {position_id} did not sync with tokens.",
                )

            implementation = self.get_implemenation_from_token(
                token,
                self._state.mode,
            )

            if implementation is None:

                raise InvalidTokenError(
                    f"Token '{token}' has an unregistered type;\n",
                )

            call_state = implementation(position_id, self._state, self)

            potential_new_state = call_state.step_position(position_id)

            if potential_new_state is not None:

                self._state = potential_new_state
                continue

            if call_state.registered_position_id(position_id):

                raise EndOfCodeError(
                    f"End of code reached for position_id {position_id}",
                )

        return self._state.return_value

    def step_and_run_position(
        self,
        position_id: PositionId,
    ) -> State | None:
        
        stepped_state = self._state.step_position(position_id)

        if stepped_state is None:

            return None

        self._state = stepped_state

        token = self._state.get_token_at_position_id(position_id)

        if token is None:

            return None

        implementation = Interpreter.get_implemenation_from_token(
            token,
            self._state.mode,
        )

        if implementation is None:

            return None

        self._state = implementation(position_id, self._state, self)

        return self._state