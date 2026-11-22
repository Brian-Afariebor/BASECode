from basecode_math import FUNCTIONS as MATH_FUNCTIONS
from collections.abc import Callable

from errors import InvalidEndError
from errors import InvalidSetError

from implementation_uitls import get_self
from interpreter import Interpreter
from intrinsics import Integer

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

    Interpreter.register(end, Type.END)
    
    for implementation, function_type in MATH_FUNCTIONS:
        
        Interpreter.register(implementation, function_type)
    
    Interpreter.register(identifier, Type.IDENTIFIER)
    Interpreter.register(set_variable, Type.SET)

@get_self()
def end(
    self: Token,
    thread_id: ThreadId,
    interpreter: Interpreter,
) -> None | NoReturn:

    try:
        interpreter.step_and_run_thread(
            thread_id,
        )

    except Exception as interpreter_error:

        raise InvalidEndError(f"""Missing end value at:
            
            {self}""".strip()) from interpreter_error

    state = interpreter.state

    return_value = state.pop_from_stack()

    if return_value is None:

        state.return_a_value(Integer(0), thread_id)
        return

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


@get_self()
def set_variable(
    self: Token,
    thread_id: ThreadId,
    interpreter: Interpreter,
) -> None | NoReturn:

    def invalid_set_error():

        return InvalidSetError(f"""Invalid set statement at token:
                '{self}'
            """.strip())

    state = interpreter.state

    new_state = state.step_thread(thread_id)

    if new_state is None:

        raise invalid_set_error()

    variable_token = state.token_at_thread_id(thread_id)

    if variable_token is None:

        raise invalid_set_error()

    variable_name = variable_token.value

    try:

        interpreter.step_and_run_thread(
            thread_id,
        )

    except Exception as interpreter_error:

        raise invalid_set_error() from interpreter_error

    variable_value = state.pop_from_stack()

    if variable_value is None:

        raise invalid_set_error()

    state.set_variable(variable_name, variable_value)

    new_state = state.step_thread(thread_id)

    if new_state is None:

        raise invalid_set_error()
