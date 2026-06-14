from collections.abc import Callable

from typing import Any

from parser import Token
from parser import TokenStream

type Context = dict[str, Any]
type PositionId = str
type FunctionMap = dict[str, Callable[[Token, PositionId], None]]


class Executable:

    def __init__(self, name: str, tokens: TokenStream):

        self.NAME = name
        self.TOKENS = list(
            filter(
                lambda token: token.TYPE != "WHITESPACE",
                tokens,
            ),
        )

        self._variables: Context = {}
        self._positions: dict[PositionId, int] = {"main": 0}

    def run(self, *args: Any):

        self._variables.clear()

        for pos, arg in enumerate(args):

            self._variables[f"main::args::{pos}"] = arg

        self._run_position_id("main",0)

    def _append_to_stack(self, value: Any, stack: str = "main"):

        first_value = f"{stack}::0"
        top_pointer = f"{stack}::tp"

        if first_value not in self._variables:

            self._variables[first_value] = value
            self._variables[top_pointer] = 0

            return

        self._variables[top_pointer] += 1
        self._variables[self._variables[top_pointer]] = value

    def _eval_at_position(self, pos_id: PositionId):

        MAPPINGS: FunctionMap = {
            "OUT": self._out,
            "STRING": self._string,
        }

        position = self._positions[pos_id]

        token = self._token_at_pos(position)

        function = MAPPINGS[token.TYPE]

        return function(token, pos_id)

    def _out(self, token: Token, pos_id: PositionId):

        self._step_position(pos_id)
        self._eval_at_position(pos_id)
        print(self._pop_from_stack("main"))
        self._step_position(pos_id)

    def _pop_from_stack(self, stack: str = "main"):

        top_pointer = f"{stack}::tp"
        top_value_pointer = f"{stack}::{self._variables[top_pointer]}"
        top_value = self._variables[top_value_pointer]

        del self._variables[top_value_pointer]

        self._variables[top_pointer] -= 1

        if self._variables[top_pointer] == 0:

            del self._variables[top_pointer]

        return top_value

    def _step_position(self, pos_id: PositionId):

        old_position = self._positions[pos_id]

        if old_position + 1 >= len(self.TOKENS):

            raise EOFError("End of Code reached")

        self._positions[pos_id] += 1


    def _run_position_id(self, pos_id: PositionId, start: int):

        self._positions[pos_id] = start

        while self._positions[pos_id] < len(self.TOKENS):

            self._eval_at_position(pos_id)
            self._step_position(pos_id)

    def _string(self, token: Token, pos_id: PositionId):

        self._append_to_stack(token.VALUE, "main")

    def _token_at_pos(self, pos: int):

        return self.TOKENS[pos]

    def _token_at_pos_id(self, pos_id: PositionId):

        return self._token_at_pos(self._positions[pos_id])
