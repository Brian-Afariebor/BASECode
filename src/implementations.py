from errors import BASECodeRuntimeError
from errors import MissingArgumentError
from errors import MissingSelfError
from errors import MissingTerminatorError
from errors import PositionError

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
    Interpreter.register(identifier, Type.IDENTIFIER)
    Interpreter.register(set_variable, Type.SET)


def end(
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
) -> State:

    self = state.get_token_at_position_id(position_id)

    if self is None:

        # NOTE - This should never get reached,
        # but if it somehow happens there's an error
        raise MissingSelfError()

    new_state = interpreter.step_and_run_position(
        state,
        position_id,
    )

    if new_state is None:

        # TODO - Add error message
        raise MissingArgumentError(f"""Missing end value at:
            
            {self}""".strip())

    state = new_state

    return_value = state.pop_from_stack()

    if return_value is None:

        return state.return_value_from_position(Integer(0), position_id)

    return state.return_value_from_position(return_value, position_id)


def raw_float(
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
) -> State:

    self = state.get_token_at_position_id(position_id)

    if self is None:

        # NOTE - This should never get reached,
        # but if it somehow happens there's an error
        raise MissingSelfError()

    try:

        float_value = Float(self.value)

    except Exception as e:

        # NOTE - This should never get reached,
        # but if it does there's an error
        raise BASECodeRuntimeError(f"""Error '''
            {e}
            '''
            
            raised while trying to create a float with the value
            
            '{self.value}'
            
            at:

            {self}""".strip())

    return state.append_to_stack(float_value)


def identifier(
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
) -> State:

    self = state.get_token_at_position_id(position_id)

    if self is None:

        # NOTE - This should never get reached,
        # but if it somehow happens there's an error
        raise MissingSelfError()

    self_name = self.value

    self_value = state.get_variable(self_name)

    return state.append_to_stack(self_value)


def integer(
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
) -> State:

    self = state.get_token_at_position_id(position_id)

    if self is None:

        # NOTE - This should never get reached,
        # but if it somehow happens there's an error
        raise MissingSelfError()

    try:

        string_representation = self.value.replace("_", "")
        int_value = Integer(string_representation)

    except Exception as e:

        # NOTE - This should never get reached,
        # but if it does there's an error
        raise BASECodeRuntimeError(f"""Error '''
            {e}
            '''
            
            raised while trying to create an int with the value
            
            '{self.value}'

            at:

            {self}""".strip())

    return state.append_to_stack(int_value)


def set_variable(
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
) -> State:

    new_state = state.step_position(position_id)

    if new_state is None:

        raise MissingArgumentError(f"""Missing a variable name at token:
        
            {state.get_token_at_position_id(position_id)}
            
            set is used like this:

            set VARIABLE_NAME = VALUE;
            /*At the filtering stage this becomes set VARIABLE_NAME VALUE;
                so the = is not needed; just good practice.*/
            """.strip())

    state = new_state

    variable_token = state.get_token_at_position_id(position_id)

    if variable_token is None:

        raise PositionError(f"""
            Variable name token was not found at position
            
            '{position_id}'
            
            """.strip())

    variable_name = variable_token.value

    new_state = Interpreter.step_and_run_position(
        interpreter,
        state,
        position_id,
    )

    if new_state is None:

        raise MissingArgumentError(f"""Missing a variable value at token:
        
            {state.get_token_at_position_id(position_id)}
            
            set is used like this:

            set VARIABLE_NAME = VALUE;
            /*At the filtering stage this becomes set VARIABLE_NAME VALUE;
                so the = is not needed; just good practice.*/
            """.strip())

    state = new_state

    variable_value = state.pop_from_stack()

    if variable_value is None:

        raise MissingArgumentError(f"""Missing a variable value at token:
        
            {state.get_token_at_position_id(position_id)}
            
            set is used like this:

            set VARIABLE_NAME = VALUE;
            /*At the filtering stage this becomes set VARIABLE_NAME VALUE;
                so the = is not needed; just good practice.*/
            """.strip())

    state = state.set_variable(variable_name, variable_value)

    new_state = state.step_position(position_id)

    if new_state is None:

        raise MissingTerminatorError(f"""
            Missing terminator at position '{position_id}';
            set statements are, in fact, statements.""".strip())

    return new_state
