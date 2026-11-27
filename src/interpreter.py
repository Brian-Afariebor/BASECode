from __future__ import annotations

from abc import ABC
from collections.abc import Callable

from errors import BASECodeRuntimeError
from errors import EndOfCodeError
from errors import InvalidTokenError
from errors import SuspiciousError

from execution_modes import Mode
from filter import FilteredTokenStream

from states import State
from states import ThreadPosition
from states import ThreadId
from states import VariableValue

from tokens import Token
from token_types import Type

from typing import NoReturn
from typing import Self


class Interpreter(ABC):

    type Implementation = Callable[
        [ThreadId, Interpreter],
        None | NoReturn,
    ]

    type WarningMessage = str

    MAIN_THREAD_ID: ThreadId = "main"
    MAIN_THREAD: ThreadPosition = 0

    _mappings: dict[tuple[Mode, Type], Implementation] = {}
    _state: State

    # SECTION - Class methods

    @classmethod
    def generate_state(
        cls,
        tokens: FilteredTokenStream,
        mode: Mode = Mode.NORMAL,
    ) -> State:

        state = State(tokens, mode).set_thread_position(
            cls.MAIN_THREAD_ID,
            cls.MAIN_THREAD,
        )

        if state is None:

            raise BASECodeRuntimeError("Default main position is not valid")

        return state

    @classmethod
    def get_implemenation_from_token(
        cls,
        token: Token,
        mode: Mode = Mode.NORMAL,
    ) -> Implementation | None:
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

        key = (Mode.NORMAL, type)

        if key not in cls._mappings:

            return None

        return cls._mappings[key]

    @classmethod
    def register(
        cls,
        implementation: Implementation,
        type: Type,
        mode: Mode = Mode.NORMAL,
    ) -> type[Self]:
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
        mode: Mode = Mode.NORMAL,
    ) -> VariableValue | NoReturn:

        interpreter = Interpreter(tokens, mode)

        return interpreter.run_thread(cls.MAIN_THREAD_ID)

    # !SECTION

    # SECTION - Constructor
    def __init__(
        self,
        tokens: FilteredTokenStream,
        mode: Mode = Mode.NORMAL,
    ) -> None:

        self._state = Interpreter.generate_state(tokens, mode)

    # !SECTION

    # SECTION - Instance Methods
    @property
    def state(self) -> State:

        return self._state

    def run_thread(
        self,
        thread_id: ThreadId,
    ) -> VariableValue:

        _ = self.run_token_at_thread(thread_id)

        while self._state.running_thread(thread_id):

            self.step_and_run_thread(thread_id)

        return self._state.return_value

    def run_token_at_thread(
        self,
        thread_id: ThreadId,
    ) -> Self | NoReturn:

        token = self._state.token_at_thread_id(thread_id)

        if token is None:

            raise EndOfCodeError("Missing token at end of code")

        implementation = Interpreter.get_implemenation_from_token(
            token,
            self._state.MODE,
        )

        if implementation is None:

            raise InvalidTokenError(
                f"No implementation found for token '{token}'",
            )

        try:

            implementation(thread_id, self)

        except Exception as e:

            raise BASECodeRuntimeError(
                f"""An error was raised at:
                
                '{token}'
                """,
            ) from e

        return self

    def step_and_run_thread(
        self,
        thread_id: ThreadId,
    ) -> Interpreter | NoReturn:

        stepped_state = self._state.step_thread(thread_id)

        if stepped_state is None:

            raise EndOfCodeError("Reached end of file without ending")

        self._state = stepped_state

        return self.run_token_at_thread(thread_id)

    def warn(self, message: WarningMessage):

        match self._state.MODE:

            case Mode.WARNING_ERRORS:

                raise SuspiciousError(message)

            case Mode.DEBUG:

                # TODO - Add debug warning system
                pass

            case _:

                pass

    # !SECTION
