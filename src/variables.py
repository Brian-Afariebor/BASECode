from errors import BASECodeRuntimeError
from errors import EndOfCodeError
from errors import MissingTerminatorError

from implementation_uitls import get_self
from interpreter import Interpreter

from states import ThreadId
from states import VariableName

from tokens import Token
from token_types import Type


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


def set_variable(
    thread_id: ThreadId,
    interpreter: Interpreter,
) -> None:

    state = interpreter.state

    new_state = state.step_thread(thread_id)

    if new_state is None:

        raise EndOfCodeError("Missing variable assignment token")

    variable_token = state.token_at_thread_id(thread_id)

    # NOTE - This should never happen
    if variable_token is None:

        raise BASECodeRuntimeError("Missing variable assignment token")

    if variable_token.type != Type.IDENTIFIER:

        raise BASECodeRuntimeError(
            f"Tried to assign value to non-variable '{variable_token}'",
        )

    variable_name = variable_token.value

    existing_variables = list(state.variables.keys())

    if is_constant(variable_name, existing_variables):

        interpreter.warn(
            f"""Tried to reasign a potential constant
            
            '{variable_name}'
            
            at token
            
            '{variable_token}';
            
            if this is not intended, try changing the name to

            '{get_new_variable_name(variable_name, existing_variables)}'
            """,
        )

    first_character = variable_name[0]

    if first_character.islower():

        interpreter.warn(
            f"""Tried to assign a value to potential language variable
            
            '{variable_name}'
            
            at token
            
            '{variable_token}';
            
            if this is not intended, try changing the name to

            '{get_new_variable_name(variable_name, existing_variables)}'
            """,
        )

    interpreter.step_and_run_thread(
        thread_id,
    )

    variable_value = state.pop_from_stack()

    if variable_value is None:

        raise BASECodeRuntimeError("Missing assignment value")

    state.set_variable(variable_name, variable_value)

    new_state = state.step_thread(thread_id)

    if new_state is None:

        raise MissingTerminatorError("Missing ending semicolon ';'")


def is_constant(
    variable_name: VariableName,
    existing_variables: list[VariableName],
) -> bool:

    return variable_name.isupper() and variable_name in existing_variables


def get_snake_case_name(variable_name: VariableName) -> VariableName:

    if variable_name.isupper():

        space_fixed = variable_name.replace("__", "_")
        ending_fixed = space_fixed.removesuffix("_")
        return ending_fixed

    is_private = variable_name.startswith("_")

    variable_parts = variable_name.split("_")

    capital_fixed = "".join([part.capitalize() for part in variable_parts])

    return f"_{capital_fixed}" if is_private else capital_fixed


def get_new_variable_name(
    variable_name: VariableName,
    existing_variables: list[VariableName],
) -> VariableName:

    first_try = get_snake_case_name(variable_name)

    attempt = (
        first_try
        if len(first_try) > 2
        else get_snake_case_name(f"{first_try}Variable")
        if first_try.islower()
        else get_snake_case_name(f"{first_try}_CONSTANT")
    )

    attempts = 1

    while attempt in existing_variables:

        
        attempt = (
            get_snake_case_name(f"{first_try}Variable{attempts}")
            if first_try.islower()
            else get_snake_case_name(f"{first_try}_CONSTANT_{attempts}")
        )
        attempts += 1

    return attempt


FUNCTION_MAPPINGS = [
    (identifier, Type.IDENTIFIER),
    (set_variable, Type.SET),
]
