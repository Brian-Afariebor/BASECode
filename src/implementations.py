from interpreter import Interpreter

from states import PositionId
from states import State


def end(
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
):

    print("End called!")

    state.remove_position(position_id)

    return state
