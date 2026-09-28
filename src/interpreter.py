from errors import PositionError
from execution_modes import ExecutionMode
from filter import FilteredTokenStream
from implementations import Implementation

from states import Position
from states import PositionId
from states import State
from states import VariableValue

from tokens import Token
from token_types import Type


class Interpreter:

    _mappings: dict[tuple[ExecutionMode, Type], Implementation] = {}

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

            raise RuntimeError("Default main position is not valid")

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

    # TODO - Implement this method
    @classmethod
    def run(
        cls,
        tokens: FilteredTokenStream,
        mode: ExecutionMode = ExecutionMode.NORMAL,
    ) -> VariableValue:

        state = cls.generate_state(tokens, mode)

        main_id = cls.MAIN_POSITION_ID

        while state.get_position(main_id) is not None:

            token = state.get_token_at_position_id(main_id)

            if token is None:

                raise PositionError(
                    f"Invalid Main Position {state.get_position(main_id)}",
                )

            implementation = cls.get_implemenation_from_token(token, mode)

            if implementation is None:

                type = token.type

                raise NotImplementedError(
                    f"Function for type {type} and mode {mode} is not defined",
                )

            state = implementation(state, token)

            state.step_position(main_id)
