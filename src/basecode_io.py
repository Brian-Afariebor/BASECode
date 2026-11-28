from errors import BASECodeRuntimeError
from errors import MissingTerminatorError

from implementation_uitls import get_args
from interpreter import Interpreter
from intrinsics import String
from states import ThreadId
from states import VariableValue
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

    print(value, end="")

    new_state = state.step_thread(thread_id)

    if new_state is None:

        raise MissingTerminatorError("Missing ending parenthesis ')'")

    new_state = state.step_thread(thread_id)
    
    if new_state is None:

        raise MissingTerminatorError("Missing ending semocolon ';'")


@get_args(0)
def get_input(args: list[VariableValue]):

    return String(input())


FUNCTION_MAPPINGS = [
    (out, Type.OUT),
    (get_input, Type.IN),
]
