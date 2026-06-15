from collections.abc import Callable

from enum import StrEnum

from typing import Any

from parser import Token
from parser import TokenStream

from re import sub

type Context = dict[str, Any]
type PositionId = str
type FunctionMap = dict[str, Callable[[Token, PositionId], None]]


class ExecutionMode(StrEnum):

    DOCSTRINGS = "-d"


class Executable:

    def __init__(
        self,
        name: str,
        tokens: TokenStream,
        *args: ExecutionMode,
    ):

        self.NAME = name

        self.modes = args

        self._variables: Context = {}
        self._positions: dict[PositionId, int] = {"main": 0}

        tokens = list(
            filter(
                lambda token: token.TYPE
                not in [
                    "WHITESPACE",
                    "SHEBANG",
                    "COMMENT",
                ],
                tokens,
            ),
        )

        if ExecutionMode.DOCSTRINGS in self.modes:

            tokens = list(
                filter(
                    lambda token: token.TYPE == "DOCSTRING",
                    tokens,
                )
            )

        else:

            tokens = list(
                filter(
                    lambda token: token.TYPE != "DOCSTRING",
                    tokens,
                )
            )

        self.TOKENS = tokens

    def run(self, *args: Any):

        self._variables.clear()

        for pos, arg in enumerate(args):

            self._variables[f"main::args::{pos}"] = arg

        self._run_position_id("main", 0)

    def _append_to_stack(self, value: Any, stack: str = "main"):

        first_value = f"{stack}::0"
        top_pointer = f"{stack}::tp"

        if first_value not in self._variables:

            self._variables[first_value] = value
            self._variables[top_pointer] = 0

            return

        self._variables[top_pointer] += 1
        self._variables[self._variables[top_pointer]] = value

    def _docstring(self, token: Token, pos_id: PositionId):

        docstring = token.VALUE
        docstring = sub(r"\/\*\*","",docstring)
        docstring = sub(r"\*\/","",docstring)
        print(docstring.strip()+"\n"*2)

    def _end(self, token: Token, pos_id: PositionId):

        self._step_position(pos_id)
        self._eval_at_position(pos_id)

        del self._positions[pos_id]

        if pos_id == "main":

            self._positions.clear()
            print(
                "\n" * 5
                + f"Program '{self.NAME}' ended with a "
                + f"return value of {self._pop_from_stack('main')}."
            )

    def _eval_at_position(self, pos_id: PositionId):

        MAPPINGS: FunctionMap = {
            "OUT": self._out,
            "STRING": self._string,
            "END": self._end,
            "INTEGER": self._int,
            "DOCSTRING": self._docstring,
        }

        position = self._positions[pos_id]

        token = self._token_at_pos(position)

        type = token.TYPE

        function = MAPPINGS[type]

        return function(token, pos_id)

    def _int(self, token: Token, pos_id: PositionId):

        self._append_to_stack(int(token.VALUE))

    def _out(self, token: Token, pos_id: PositionId):

        self._step_position(pos_id)
        self._eval_at_position(pos_id)
        print(self._pop_from_stack("main"), end="")
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

    def _run_position_id(self, pos_id: PositionId, start: int):

        self._positions[pos_id] = start

        while pos_id in self._positions:

            self._eval_at_position(pos_id)
            self._step_position(pos_id)

    def _step_position(self, pos_id: PositionId) -> None | Token:

        if pos_id not in self._positions:

            return None

        old_position = self._positions[pos_id]

        if old_position + 1 >= len(self.TOKENS):

            if ExecutionMode.DOCSTRINGS in self.modes:

                del self._positions[pos_id]
                return
            
            raise EOFError(
                f"End of Code reached by thread {pos_id}, "
                + f"at:\n\t{self._token_at_pos(old_position)}"
            ) from None

        self._positions[pos_id] += 1

        return self._token_at_pos_id(pos_id)

    def _string(self, token: Token, pos_id: PositionId):

        string = token.VALUE[1:-1]

        string = sub(r"\\t", r"\t", string)
        string = sub(r"\\n", r"\n", string)
        string = sub(r"\\q", r"\"", string)

        self._append_to_stack(string, "main")

    def _token_at_pos(self, pos: int):

        if pos >= len(self.TOKENS):

            raise EOFError(f"No tokens at position {pos+1}") from None

        return self.TOKENS[pos]

    def _token_at_pos_id(self, pos_id: PositionId):

        return self._token_at_pos(self._positions[pos_id])
