from execution_modes import Mode
from filter import FilteredTokenStream

from intrinsics import Integer
from intrinsics import Float
from intrinsics import String
from intrinsics import Null
from intrinsics import NULL

from regexes import Keyword
from regexes import reference

from typing import Self

type VariableName = str
type VariableValue = String | Integer | Float | Null
type ThreadPosition = int
type ThreadId = str


# SECTION - Class methods
class State:
    """The state of a BASECode program.

    Attributes:
        TOKENS (Final[FilteredTokenStream]): The tokenized code.
        MODE (Final[ExecutionMode]): THe mode to run the code with.
    """

    def __init__(
        self,
        tokens: FilteredTokenStream,
        mode: Mode = Mode.NORMAL,
    ):
        """The constructor for a State.

        Args:
            tokens (FilteredTokenStream): The tokenized code.
            mode (ExecutionMode, optional):
                The mode to run the code with.
                Defaults to ExecutionMode.NORMAL.
        """

        self.TOKENS = tokens
        self.MODE = mode

        self._thread_positions: dict[ThreadId, ThreadPosition] = {}
        self._variables: dict[VariableName, VariableValue] = {}
        self._return_value: VariableValue = NULL

    # SECTION - Properties
    @property
    def return_value(self):

        return self._return_value

    @property
    def variables(self):

        return self._variables.copy()

    #!SECTION

    # SECTION - Public methods
    def append_to_stack(
        self,
        value: VariableValue,
        stack_name: str = Keyword.MAIN_STACK_NAME.value,
    ):

        first_value = reference(stack_name) + "0"
        top_pointer = reference(stack_name) + "tp"

        if not self.registered_variable_name(first_value):

            return self.set_variable(
                first_value,
                value,
            ).set_variable(
                top_pointer,
                Integer(0),
            )

        top_pointer_value = self.get_variable(top_pointer)

        if not isinstance(top_pointer_value, Integer):

            raise ValueError(
                f"Non-int top pointer found on stack {stack_name};\n"
                + "maybe you changed the value of the top pointer?\n"
                + "Check your code."
            )

        new_top_pointer_value = top_pointer_value + 1

        return self.set_variable(
            top_pointer,
            new_top_pointer_value,
        ).set_variable(
            reference(
                stack_name,
            )
            + str(
                new_top_pointer_value,
            ),
            value,
        )

    def delete_variable(self, variable_name: VariableName):

        if self.registered_variable_name(variable_name):

            del self._variables[variable_name]

        return self

    def get_thread_position(
        self,
        thread_id: ThreadId,
    ) -> ThreadPosition | None:

        if not self.running_thread(thread_id):

            return None

        return self._thread_positions[thread_id]

    def token_at_thread_id(
        self,
        thread_id: ThreadId,
    ):

        position = self.get_thread_position(thread_id)

        if position is None:

            return None

        return self.TOKENS[position]

    def get_variable(
        self,
        variable_name: VariableName,
    ) -> VariableValue:

        if not self.registered_variable_name(variable_name):

            return NULL

        return self._variables[variable_name]

    def pop_from_stack(
        self,
        stack_name: VariableName = Keyword.MAIN_STACK_NAME.value,
    ) -> VariableValue | None:

        stack_reference = reference(stack_name)

        top_pointer_name = stack_reference + "tp"

        top_pointer_value = self.get_variable(top_pointer_name)

        if not isinstance(top_pointer_value, Integer):

            return None

        top_value_pointer_name = stack_reference + str(top_pointer_value)

        top_value = self.get_variable(top_value_pointer_name)

        self.delete_variable(top_value_pointer_name).set_variable(
            top_pointer_name, top_pointer_value - 1
        )

        if top_pointer_value <= 0:

            self.delete_variable(top_pointer_name)

        return top_value

    def running_thread(self, thread_id: ThreadId):

        return thread_id in self._thread_positions

    def registered_variable_name(self, variable_name: VariableName):

        return variable_name in self._variables

    def remove_thread(self, thread_id: ThreadId):

        if self.running_thread(thread_id):

            del self._thread_positions[thread_id]

        return self

    def set_thread_position(
        self,
        thread_id: ThreadId,
        position: ThreadPosition,
    ) -> None | Self:

        if not self.valid_thread_position(position):

            return None

        self._thread_positions[thread_id] = position

        return self

    def step_thread(
        self,
        thread_id: ThreadId,
    ) -> None | Self:

        if not self.running_thread(thread_id):

            return None

        current_adress = self._thread_positions[thread_id]

        new_adress: ThreadPosition = current_adress + 1

        return self.set_thread_position(thread_id, new_adress)

    def set_variable(
        self,
        variable_name: VariableName,
        variable_value: VariableValue,
    ):

        self._variables[variable_name] = variable_value

        return self

    def valid_thread_position(self, adress: ThreadPosition):

        return adress >= 0 and adress < len(self.TOKENS)

    def return_a_value(
        self,
        value: VariableValue,
        thread_id: ThreadId,
    ):

        self._return_value = value

        return self.remove_thread(thread_id)

    # !SECTION


# !SECTION
