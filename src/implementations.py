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

        raise ValueError()

    state = new_state

    return_value = interpreter.run_position(position_id, state)

    _ = state.return_value_from_position(return_value, position_id)

    return state
