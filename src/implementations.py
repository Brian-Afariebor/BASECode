from basecode_math import FUNCTIONS as MATH_FUNCTIONS
from collections.abc import Callable

from errors import BASECodeRuntimeError
from errors import EndOfCodeError
from errors import MissingTerminatorError

from implementation_uitls import get_self
from interpreter import Interpreter

from states import ThreadId
from states import VariableValue

from tokens import Token
from token_types import Type
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


def register_all() -> None:

    for implementation, function_type in MATH_FUNCTIONS:

        Interpreter.register(implementation, function_type)


    Interpreter.register(end, Type.END)
    Interpreter.register(identifier, Type.IDENTIFIER)
    Interpreter.register(set_variable, Type.SET)


def end(
    thread_id: ThreadId,
    interpreter: Interpreter,
) -> None | NoReturn:

    state = interpreter.state

    try:

        interpreter.step_and_run_thread(
            thread_id,
        )

    except Exception as interpreter_error:

        raise BASECodeRuntimeError(f"Missing end value") from interpreter_error

    return_value = state.pop_from_stack()

    if return_value is None:

        raise BASECodeRuntimeError("Missing end value")

    state.return_a_value(return_value, thread_id)


@get_self()
def identifier(
    self: Token,
    thread_id: ThreadId,
    interpreter: Interpreter,
) -> None:

    self_name = self.value

    state = interpreter.state

    self_value = state.get_variable(self_name)

    state.append_to_stack(self_value)


def set_variable(
    thread_id: ThreadId,
    interpreter: Interpreter,
) -> None | NoReturn:

    state = interpreter.state

    new_state = state.step_thread(thread_id)

    if new_state is None:

        raise EndOfCodeError("Missing variable assignment token")

    variable_token = state.token_at_thread_id(thread_id)

    # NOTE - This should never happen
    if variable_token is None:

        raise BASECodeRuntimeError("Missing variable assignment token")

    variable_name = variable_token.value

    interpreter.step_and_run_thread(
        thread_id,
    )

    variable_value = state.pop_from_stack()

    if variable_value is None:

        raise BASECodeRuntimeError("Missing assignment value")

    state.set_variable(variable_name, variable_value)

    new_state = state.step_thread(thread_id)

    if new_state is None:

        raise MissingTerminatorError("Missing ending semicolon ';'")
