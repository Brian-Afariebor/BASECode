from errors import BASECodeRuntimeError
from errors import MissingTerminatorError

from interpreter import Interpreter
from states import ThreadId
from token_types import Type

def out(
    thread_id: ThreadId,
    interpreter: Interpreter,
) -> None:

    interpreter.step_and_run_thread(thread_id)

    state = interpreter.state

    value = state.pop_from_stack()

    if value is None:

        raise BASECodeRuntimeError("Could not get value to print")

    print(value, end = "")

    new_state = state.step_thread(thread_id)

    if new_state is None:

        raise MissingTerminatorError("Missing ending parenthesis ')'")

FUNCTION_MAPPINGS = [(out, Type.OUT)]