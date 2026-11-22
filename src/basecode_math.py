from errors import BASECodeRuntimeError
from errors import BASECodeTypeError

from implementation_uitls import get_self
from implementation_uitls import get_args

from interpreter import Interpreter

from intrinsics import Float
from intrinsics import Integer
from intrinsics import Null
from intrinsics import String

from states import ThreadId
from states import VariableValue

from tokens import Token
from token_types import Type
from typing import NoReturn


@get_args(2)
def add(arguments: list[VariableValue]):

    first_argument = arguments[0]
    second_argument = arguments[1]

    if isinstance(first_argument, Null):

        raise BASECodeTypeError("Null first-argument to add")

    if isinstance(second_argument, Null):

        raise BASECodeTypeError("Null second-argument to add")

    if isinstance(first_argument, String):

        return first_argument + second_argument

    if isinstance(second_argument, String):

        return String(first_argument) + second_argument
    
    return first_argument + second_argument

@get_self()
def integer(
    self: Token,
    thread_id: ThreadId,
    interpreter: Interpreter,
) -> None | NoReturn:

    string_representation = self.value.replace("_", "")

    try:

        int_value = Integer(string_representation)

    except Exception as casting_error:

        raise BASECodeRuntimeError(
            f"""The integer
            
            '{string_representation}'
            
            could not be created.""",
        ) from casting_error

    interpreter.state.append_to_stack(int_value)


@get_self()
def raw_float(
    self: Token,
    thread_id: ThreadId,
    interpreter: Interpreter,
) -> None | NoReturn:

    string_representation = self.value

    try:

        float_value = Float(string_representation)

    except Exception as creation_error:

        raise BASECodeRuntimeError(
            f"""The integer
            
            '{string_representation}'
            
            could not be created.""",
        ) from creation_error

    interpreter.state.append_to_stack(float_value)


FUNCTIONS = [
    (integer, Type.INTEGER),
    (raw_float, Type.FLOAT),
    (add, Type.ADD),
]
