from basecode_math import FUNCTION_MAPPINGS as MATH_FUNCTIONS
from errors import BASECodeRuntimeError
from interpreter import Interpreter
from states import ThreadId
from token_types import Type
from variables import FUNCTION_MAPPINGS as VARIABLE_FUNCTIONS


def register_all() -> None:

    for implementation, function_type in MATH_FUNCTIONS:

        Interpreter.register(implementation, function_type)

    for implementation, function_type in VARIABLE_FUNCTIONS:

        Interpreter.register(implementation, function_type)

    Interpreter.register(end, Type.END)


def end(
    thread_id: ThreadId,
    interpreter: Interpreter,
) -> None:

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
