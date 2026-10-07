from abc import ABC

from collections.abc import Callable

from errors import PositionError  # pyright: ignore[reportUnusedImport]
from execution_modes import ExecutionMode
from filter import FilteredTokenStream

from states import Position
from states import PositionId
from states import State
from states import VariableValue  # pyright: ignore[reportUnusedImport]

from tokens import Token
from token_types import Type


class Interpreter(ABC):

    type Implementation = Callable[[PositionId, State, Interpreter], State]

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

    @classmethod
    def run(
        cls,
        tokens: FilteredTokenStream,
        mode: ExecutionMode = ExecutionMode.NORMAL,
    ):

        state = cls.generate_state(tokens, mode)

        interpreter = Interpreter()

        interpreter.run_position(cls.MAIN_POSITION_ID, state)

    def run_position(
        self,
        position_id: PositionId,
        state: State,
    ):

        while state.registered_position_id(position_id):

            token = state.get_token_at_position_id(position_id)

            token = self.raise_null_token_error(position_id, token)

            implementation = self.get_implemenation_from_token(
                token,
                state.mode,
            )

            implementation = self.raise_unimplemented_error(token, implementation)

            state = implementation(position_id, state, self)

            new_state = state.step_position(position_id)

            if new_state is not None:

                state = new_state
                continue

            if state.registered_position_id(position_id):

                raise RuntimeError(
                    f"End of code reached for position_id {position_id}",
                )

        return state.return_value

    def raise_unimplemented_error(
        self,
        token: Token,
        implementation: Implementation | None,
    ):
        if implementation is None:
            raise SyntaxError(
                f"Token '{token}' has an unregistered type;\n"
                + "check your installation of BASECode and your code.",  # pyright: ignore[reportOptionalMemberAccess]
            )

        return implementation

    def raise_null_token_error(
        self,
        position_id: PositionId,
        token: Token | None,
    ):
        if token is None:
            raise RuntimeError(
                f"Position {position_id} did not sync with tokens.",
            )

        return token
