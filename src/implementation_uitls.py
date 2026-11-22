from collections.abc import Callable

from errors import BASECodeRuntimeError
from errors import MissingSelfError

from interpreter import Interpreter

from states import ThreadId
from states import VariableValue

from tokens import Token
from typing import NoReturn

type Implementation = Interpreter.Implementation
type SelfImplementation = Callable[
    [
        Token,
        ThreadId,
        Interpreter,
    ],
    None | NoReturn,
]

type SimpleArgumentImplementation = Callable[
    [list[VariableValue]],
    VariableValue | NoReturn,
]


def get_self(
    error_message: str = "",
) -> Callable[[SelfImplementation], Implementation]:

    def get_self_decorator(
        self_implementation: SelfImplementation,
    ) -> Implementation:

        def new_implementation(
            thread_id: ThreadId,
            interpreter: Interpreter,
        ):

            self = interpreter.state.token_at_thread_id(thread_id)

            if self is None:

                # NOTE - This should never get reached,
                # but if it somehow happens there's an error
                raise MissingSelfError(error_message)

            self_implementation(
                self,
                thread_id,
                interpreter,
            )

        return new_implementation

    return get_self_decorator


def get_args(
    count: int,
) -> Callable[
    [SimpleArgumentImplementation],
    Implementation,
]:

    def get_args_decorator(
        simple_argument_implmentation: SimpleArgumentImplementation,
    ) -> Implementation:

        def new_implementation(
            thread_id: ThreadId,
            interpreter: Interpreter,
        ):

            arguments: list[VariableValue] = []

            for i in range(count):

                try:

                    interpreter.step_and_run_thread(thread_id)

                except Exception as e:

                    raise missing_argument_error(i) from e

                argument_value = interpreter.state.pop_from_stack()

                if argument_value is None:

                    raise missing_argument_error(i)

                arguments.append(argument_value)

            return_value = simple_argument_implmentation(arguments)

            interpreter.state.append_to_stack(return_value)

            new_state = interpreter.state.step_thread(thread_id)

            if new_state is None:

                raise BASECodeRuntimeError(
                    """Missing ending parenthesis
                    ')'
                    at end of method call""",
                )

        return new_implementation

    return get_args_decorator


def missing_argument_error(
    i: int,
):
    return BASECodeRuntimeError(
        f"""Missing argument number
        '{i+1}'
        """,
    )