from execution_modes import ExecutionMode
from filter import FilteredTokenStream

from intrinsics import Integer
from intrinsics import Float
from intrinsics import String
from intrinsics import Null
from intrinsics import NULL

from regexes import Keyword

from typing import Final
from typing import Self

type VariableName = str

type VariableValue = String | Integer | Float | Null
type Position = int
type PositionId = str


class State:
    """The state of a BASECode program.

    Attributes:
        tokens (Final[FilteredTokenStream]): The tokenized code.
        mode(Final[ExecutionMode]): THe mode to run the code with.
    """

    tokens: Final[FilteredTokenStream]
    mode: Final[ExecutionMode]

    _variables: dict[VariableName, VariableValue]
    _positions: dict[PositionId, Position]
    _return_value: VariableValue

    def __init__(
        self,
        tokens: FilteredTokenStream,
        mode: ExecutionMode = ExecutionMode.NORMAL,
    ):
        """The constructor for a State.

        Args:
            tokens (FilteredTokenStream): The tokenized code.
            mode (ExecutionMode, optional):
                The mode to run the code with.
                Defaults to ExecutionMode.NORMAL.
        """

        self.tokens = tokens
        self.mode = mode

        self._positions = {}
        self._variables = {}
        self._return_value = NULL

    # SECTION - Properties
    @property
    def return_value(self):

        return self._return_value

    #!SECTION

    # SECTION - Public methods
    def append_to_stack(
        self,
        value: VariableValue,
        stack_name: str = Keyword.MAIN_NAME.value,
    ):

        first_value = reference(stack_name) + "0"
        top_pointer = reference(stack_name) + "tp"

        if first_value not in self._variables:

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

        new_top_pointer_value = Integer(top_pointer_value + 1)

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

    def get_position(
        self,
        position_id: PositionId,
    ) -> Position | None:
        """Gets the position of a position id.

        Args:
            position_id (PositionId): The position id to get the value of.

        Returns:
            Position | None:
                The value of the position id.
                Is None if the position id is not registered.
        """

        if not self.registered_position_id(position_id):

            return None

        return self._positions[position_id]

    def get_token_at_position_id(self, position_id: PositionId):

        position = self.get_position(position_id)

        if position is None:

            return None

        return self.tokens[position]

    def get_variable(
        self,
        variable_name: VariableName,
    ) -> VariableValue | None:
        """Gets the value of a variable.

        Args:
            variable_name (VariableName): The variable to get the value of.

        Returns:
            VariableValue | None:
                The value of the variable.
                Returns none if the variable has not been defined.
        """

        if not self.registered_variable_name(variable_name):

            return None

        return self._variables[variable_name]

    def pop_from_stack(
            self,
            stack_name: VariableName = Keyword.MAIN_NAME.value,
        ) -> VariableValue | None:

        stack_reference = reference(stack_name)

        top_pointer_name = stack_reference + "tp"

        top_pointer_value = self.get_variable(top_pointer_name)

        if not isinstance(top_pointer_value, Integer):

            return None

        top_value_pointer_name = stack_reference + str(top_pointer_value)

        top_value = self.get_variable(top_value_pointer_name)

        self.delete_variable(top_value_pointer_name).set_variable(
            top_pointer_name,
              Integer(top_pointer_value -1),
            )

        if top_pointer_value <= 0:

            self.delete_variable(top_pointer_name)

        return top_value

    def registered_position_id(self, position_id: PositionId):

        return position_id in self._positions

    def registered_variable_name(self, variable_name: VariableName):

        return variable_name in self._variables

    def remove_position(self, position_id: PositionId):

        if self.registered_position_id(position_id):

            del self._positions[position_id]

        return self

    def return_value_from_position(
        self,
        value: VariableValue,
        position_id: PositionId,
    ):

        self._return_value = value

        return self.remove_position(position_id)

    def set_position(
        self,
        position_id: PositionId,
        position: Position,
    ) -> None | Self:
        """Sets the position of a position id.

        Args:
            position_id (PositionId) The position id to set the position of.
            position (Position): The position to set the position id to.

        Returns:
            None | Self:
                Sets the value of the position.
                Returns None if the position is not valid.
        """

        if not self.valid_position(position):

            return None

        self._positions[position_id] = position

        return self

    def step_position(
        self,
        position_id: PositionId,
    ) -> None | Self:

        if not self.registered_position_id(position_id):

            return None

        current_adress = self._positions[position_id]

        new_adress: Position = current_adress + 1

        return self.set_position(position_id, new_adress)

    def set_variable(
        self,
        variable_name: VariableName,
        variable_value: VariableValue,
    ):

        self._variables[variable_name] = variable_value

        return self

    def valid_position(self, adress: Position):

        return adress >= 0 and adress < len(self.tokens)

    #!SECTION


def reference(variable: VariableName)->str:

    return variable + Keyword.REFERENCE_OPERATOR.value
