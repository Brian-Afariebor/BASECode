from interpreter import Interpreter

from intrinsics import Integer
from intrinsics import Float

from states import PositionId
from states import State

from token_types import Type

def register_all():

    Interpreter.register(end, Type.END)
    Interpreter.register(raw_float, Type.FLOAT)
    Interpreter.register(integer, Type.INTEGER)

def end(
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
):

    new_state = interpreter.step_and_run_position(
        state,
        position_id,
    )

    if new_state is None:

        # TODO - Add error message
        raise ValueError()

    state = new_state

    return_value = state.pop_from_stack()

    if return_value is None:

        return state.return_value_from_position(Integer(0), position_id)

    return state.return_value_from_position(return_value, position_id)

def raw_float(
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
):

    self = state.get_token_at_position_id(position_id)

    if self is None:

        # NOTE - This should never get reached,
        # but if it somehow happens there's an error

        # TODO - Add error message
        raise RuntimeError()

    try:

        float_value = Float(self.value)

    except Exception as e:

        # NOTE - This should never get reached,
        # but if it does there's an error

        # TODO - Improve error message
        raise RuntimeError(f"Error '{e}' raised")

    return state.append_to_stack(float_value)


def integer(
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
):

    self = state.get_token_at_position_id(position_id)

    if self is None:

        # NOTE - This should never get reached,
        # but if it somehow happens there's an error

        # TODO - Add error message
        raise RuntimeError()

    try:

        int_value = Integer(self.value)

    except Exception as e:

        # NOTE - This should never get reached,
        # but if it does there's an error

        # TODO - Improve error message
        raise RuntimeError(f"Error '{e}' raised")

    return state.append_to_stack(int_value)
