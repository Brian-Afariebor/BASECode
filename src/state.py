from execution_modes import ExecutionMode
from filter import FilteredTokenStream
from typing import Final, Self

type VariableName = str

# TODO - Add null class
type VariableValue = str | int | float
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

        if not self._registered_position_id(position_id):

            return None

        return self._positions[position_id]

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

        if not self._registered_variable_name(variable_name):

            return None

        return self._variables[variable_name]

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

        if not self._valid_position(position):

            return None

        self._positions[position_id] = position

        return self

    def step_position(
        self,
        position_id: PositionId,
    ) -> bool:

        if not self._registered_position_id(position_id):

            return False

        current_adress = self._positions[position_id]

        new_adress: Position = current_adress + 1

        return self.set_position(position_id, new_adress) is None

    def set_variable(
        self,
        variable_name: VariableName,
        variable_value: VariableValue,
    ):

        self._variables[variable_name] = variable_value

        return self

    def _registered_position_id(self, position_id: PositionId):

        return position_id in self._positions

    def _registered_variable_name(self, variable_name: VariableName):

        return variable_name in self._variables

    def _valid_position(self, adress: Position):

        return adress in range(0,len(self.tokens))