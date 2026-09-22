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

    _vars: dict[VariableName, VariableValue]
    _positions: dict[PositionId, Position]

    def __init__(
        self,
        tokens: FilteredTokenStream,
        mode: ExecutionMode = ExecutionMode.NORMAL,
    ):

        self.tokens = tokens
        self.mode = mode

        self._positions = {}
        self._vars = {}

    def set_position(
        self,
        position_id: PositionId,
        position: Position,
    ):

        self._positions[position_id] = position

    def get_position(self, position_id: PositionId) -> Position | None:

        if position_id not in self._positions:

            return None

        return self._positions[position_id]
