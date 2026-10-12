from interpreter import Interpreter

from states import PositionId
from states import State


def end(
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
):

    new_state = state.step_position(position_id)

    if new_state is None:

        # TODO - Add error message
        raise ValueError()

    state = new_state

    # TODO - Replace with pop from stack
    return_value = interpreter.run_position(position_id, state)

    return state.return_value_from_position(return_value, position_id)


def integer(
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
):

    self = state.get_token_at_position_id(position_id)

    if self is None:

        # NOTE - This should never get reached,
        # but if somehow? happens there's an error

        # TODO - Add error message
        raise RuntimeError()

    try:

        int_value = int(self.value)

    except Exception as e:

        # NOTE - This should never get reached,
        # but if it does there's an error

        # TODO - Improve error message
        raise RuntimeError(f"Error {e} raised")

    return state.append_to_stack(int_value)
