from collections.abc import Callable

from errors import BASECodeRuntimeError
from errors import InvalidEndError
from errors import InvalidSetError
from errors import MissingSelfError
from errors import MissingTerminatorError

from interpreter import Interpreter

from intrinsics import Integer
from intrinsics import Float

from states import PositionId
from states import State

from tokens import Token
from token_types import Type

type Implementation = Interpreter.Implementation
type SelfImplementation = Callable[
    [
        Token,
        PositionId,
        State,
        Interpreter,
    ],
    State,
]



def register_all():

    Interpreter.register(end, Type.END)
    Interpreter.register(raw_float, Type.FLOAT)
    Interpreter.register(integer, Type.INTEGER)
    Interpreter.register(identifier, Type.IDENTIFIER)
    Interpreter.register(set_variable, Type.SET)


def get_self(error_message: str = ""):

    def get_self_decorator(self_implementation: SelfImplementation):

        def new_implementation(
            position_id: PositionId,
            state: State,
            interpreter: Interpreter,
        ) -> State:

            self = state.get_token_at_position_id(position_id)

            if self is None:

                # NOTE - This should never get reached,
                # but if it somehow happens there's an error
                raise MissingSelfError(error_message)

            return self_implementation(self, position_id, state, interpreter)

        return new_implementation

    return get_self_decorator


@get_self()
def end(
    self: Token,
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
) -> State:

    new_state = interpreter.step_and_run_position(
        state,
        position_id,
    )

    if new_state is None:

        raise InvalidEndError(f"""Missing end value at:
            
            {self}""".strip())

    state = new_state

    return_value = state.pop_from_stack()

    if return_value is None:

        return state.return_value_from_position(Integer(0), position_id)

    return state.return_value_from_position(return_value, position_id)


@get_self()
def raw_float(
    self: Token,
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
) -> State:

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


@get_self()
def identifier(
    self: Token,
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
) -> State:

    self_name = self.value

    self_value = state.get_variable(self_name)

    return state.append_to_stack(self_value)


@get_self()
def integer(
    self: Token,
    position_id: PositionId,
    state: State,
    interpreter: Interpreter,
) -> State:

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

    def missing_variable_value_error():

        return InvalidSetError(f"""Missing a variable value at token:

            {state.get_token_at_position_id(position_id)}
            """.strip())

    new_state = state.step_position(position_id)

    if new_state is None:

        raise InvalidSetError(f"""Missing a variable name at token:
                    {state.get_token_at_position_id(position_id)}
                    """.strip())

    state = new_state

    variable_token = state.get_token_at_position_id(position_id)

    if variable_token is None:

        raise InvalidSetError(f"""
            Variable name token was not found at position:
            
            '{position_id}'
            
            """.strip())

    variable_name = variable_token.value

    new_state = interpreter.step_and_run_position(
        state,
        position_id,
    )

    if new_state is None:

        raise missing_variable_value_error()

    state = new_state

    variable_value = state.pop_from_stack()

    if variable_value is None:

        raise missing_variable_value_error()

    state = state.set_variable(variable_name, variable_value)

    new_state = state.step_position(position_id)

    if new_state is None:

        raise MissingTerminatorError(f"""
            Missing terminator at position '{position_id}';
            set statements are, in fact, statements.""".strip())

    return new_state
