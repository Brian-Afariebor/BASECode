from collections.abc import Callable

from errors import BASECodeRuntimeError
from errors import InvalidEndError
from errors import InvalidSetError
from errors import MissingSelfError

from interpreter import Interpreter

from intrinsics import Integer
from intrinsics import Float

from states import ThreadId
from states import VariableValue

from tokens import Token
from token_types import Type

type Implementation = Interpreter.Implementation
type SelfImplementation = Callable[
    [
        Token,
        ThreadId,
        Interpreter,
    ],
    None,
]

type SimpleArgumentImplementation = Callable[
    [list[VariableValue]],
    VariableValue,
]


def register_all():

    Interpreter.register(end, Type.END)
    Interpreter.register(raw_float, Type.FLOAT)
    Interpreter.register(integer, Type.INTEGER)
    Interpreter.register(identifier, Type.IDENTIFIER)
    Interpreter.register(set_variable, Type.SET)


def get_self(
    error_message: str = "",
) -> Callable[[SelfImplementation], Implementation]:

    def get_self_decorator(
        self_implementation: SelfImplementation,
    ) -> Implementation:

        def new_implementation(
            thread_id: ThreadId,
            interpreter: Interpreter,
        ):

            self = interpreter.state.token_at_thread_id(thread_id)

            if self is None:

                # NOTE - This should never get reached,
                # but if it somehow happens there's an error
                raise MissingSelfError(error_message)

            return self_implementation(
                self,
                thread_id,
                interpreter,
            )

        return new_implementation

    return get_self_decorator


def get_args(
    count: int,
) -> Callable[
    [SimpleArgumentImplementation],
    Implementation,
]:

    def get_args_decorator(
        simple_argument_implmentation: SimpleArgumentImplementation,
    ) -> Implementation:

        @get_self()
        def new_implementation(
            self: Token,
            thread_id: ThreadId,
            interpreter: Interpreter,
        ):

            def missing_argument_error(
                self: Token,
                i: int,
            ):
                return BASECodeRuntimeError(
                    f"""Missing argument number 
                    '{i+1}'
                    while calling the function at:
                    {self}
                    """,
                )

            arguments: list[VariableValue] = []

            for i in range(count):

                try:

                    interpreter.step_and_run_thread(thread_id)

                except Exception as e:

                    raise missing_argument_error(self, i) from e

                argument_value = interpreter.state.pop_from_stack()

                if argument_value is None:

                    raise missing_argument_error(self, i)

                arguments.append(argument_value)

            simple_argument_implmentation(arguments)

        return new_implementation

    return get_args_decorator


@get_self()
def end(
    self: Token,
    thread_id: ThreadId,
    interpreter: Interpreter,
):

    try:
        interpreter.step_and_run_thread(
            thread_id,
        )

    except Exception as interpreter_error:

        raise InvalidEndError(f"""Missing end value at:
            
            {self}""".strip()) from interpreter_error

    state = interpreter.state

    return_value = state.pop_from_stack()

    if return_value is None:

        state.return_a_value(Integer(0), thread_id)
        return

    state.return_a_value(return_value, thread_id)


@get_self()
def integer(
    self: Token,
    thread_id: ThreadId,
    interpreter: Interpreter,
):

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
):

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


@get_self()
def identifier(
    self: Token,
    thread_id: ThreadId,
    interpreter: Interpreter,
):

    self_name = self.value

    state = interpreter.state

    self_value = state.get_variable(self_name)

    state.append_to_stack(self_value)


@get_self()
def set_variable(
    self: Token,
    thread_id: ThreadId,
    interpreter: Interpreter,
):

    def invalid_set_error():

        return InvalidSetError(f"""Invalid set statement at token:
                '{self}'
            """.strip())

    state = interpreter.state

    new_state = state.step_thread(thread_id)

    if new_state is None:

        raise invalid_set_error()

    state = new_state

    variable_token = state.token_at_thread_id(thread_id)

    if variable_token is None:

        raise invalid_set_error()

    variable_name = variable_token.value

    try:

        interpreter.step_and_run_thread(
            thread_id,
        )

    except Exception as interpreter_error:

        raise invalid_set_error() from interpreter_error

    variable_value = state.pop_from_stack()

    if variable_value is None:

        raise invalid_set_error()

    state = state.set_variable(variable_name, variable_value)

    new_state = state.step_thread(thread_id)

    if new_state is None:

        raise invalid_set_error()
