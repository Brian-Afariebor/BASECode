from execution_modes import ExecutionMode
from filter import FilteredTokenStream
from typing import Final

type VariableName = str
type VariableValue = str | int | float
type Position = int
type PositionId = str


class State:

    tokens: Final[FilteredTokenStream]
    mode: Final[ExecutionMode]

    _variables: dict[VariableName, VariableValue]
    _positions: dict[PositionId, Position]

    def __init__(
        self,
        tokens: FilteredTokenStream,
        mode: ExecutionMode = ExecutionMode.NORMAL,
    ):

        self.tokens = tokens
        self.mode = mode

        self._positions = {}
        self._variables = {}

    def get_position(
        self,
        position_id: PositionId,
    ) -> Position | None:

        if position_id not in self._positions:

            return None

        return self._positions[position_id]

    def get_variable(
        self,
        variable_name: VariableName,
    ) -> VariableValue | None:

        if variable_name not in self._variables:

            return None

        return self._variables[variable_name]

    def set_position(
        self,
        position_id: PositionId,
        position: Position,
    ):

        self._positions[position_id] = position

        return self

    def set_variable(
        self,
        variable_name: VariableName,
        variable_value: VariableValue,
    ):

        self._variables[variable_name] = variable_value

        return self
