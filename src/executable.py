from collections.abc import Callable

from constants import Constants

from enum import StrEnum

from typing import Any

from tokens import Token
from tokens import TokenStream
from tokens import TokenType

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

        self._variables: Context = {
            Constants.MAIN_NAME + Constants.REFERENCE_OPERATOR + "name": self.NAME
        }
        self._positions: dict[PositionId, int] = {Constants.MAIN_NAME: 0}

        tokens = list(
            filter(
                lambda token: token.TYPE
                not in [
                    TokenType.WHITESPACE,
                    TokenType.SHEBANG,
                    TokenType.COMMENT,
                    TokenType.DUMMY,
                ],
                tokens,
            ),
        )

        if ExecutionMode.DOCSTRINGS in self.modes:

            tokens = list(
                filter(
                    lambda token: token.TYPE == TokenType.DOCSTRING,
                    tokens,
                )
            )

        else:

            tokens = list(
                filter(
                    lambda token: token.TYPE != TokenType.DOCSTRING,
                    tokens,
                )
            )

        self.TOKENS = tokens

    def run(self, *args: Any):

        self._variables.clear()

        for pos, arg in enumerate(args):

            self._variables[
                Constants.MAIN_NAME
                + Constants.REFERENCE_OPERATOR
                + "args"
                + Constants.REFERENCE_OPERATOR
                + str(pos)
            ] = arg

        self._run_position_id(Constants.MAIN_NAME, 0)

    def _append_to_stack(self, value: Any, stack_name: str = Constants.MAIN_NAME):

        first_value = stack_name + Constants.REFERENCE_OPERATOR + "0"
        top_pointer = stack_name + Constants.REFERENCE_OPERATOR + "tp"

        if first_value not in self._variables:

            self._variables[first_value] = value
            self._variables[top_pointer] = 0

            return

        self._variables[top_pointer] += 1
        self._variables[
            stack_name
            + Constants.REFERENCE_OPERATOR
            + str(self._variables[top_pointer])
        ] = value

    def _docstring(self, token: Token, pos_id: PositionId):

        docstring = token.VALUE
        docstring = sub(r"\/\*\*", "", docstring)
        docstring = sub(r"\*\/", "", docstring)
        print(docstring.strip() + "\n" * 2)

    def _end(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)
        self._eval_position(pos_id)

        del self._positions[pos_id]

        if pos_id == Constants.MAIN_NAME:

            self._positions.clear()
            print(
                "\n" * 5
                + f"Program '{self.NAME}' ended with a "
                + f"return value of {self._pop_from_stack('main')}."
            )

    def _eval_position(self, pos_id: PositionId) -> None:

        MAPPINGS: FunctionMap = {
            TokenType.OUT: self._out,
            TokenType.STRING: self._string,
            TokenType.END: self._end,
            TokenType.INTEGER: self._int,
            TokenType.DOCSTRING: self._docstring,
            TokenType.IDENTIFIER: self._identifier,
            TokenType.SET: self._set,
            TokenType.MAIN: self._main,
            TokenType.LINE_TERMINATOR: self._line_terminator,
            TokenType.RAW_SET: self._raw_set,
            TokenType.FUNCTION: self._function,
        }

        position = self._positions[pos_id]

        token = self._token_at_pos(position)

        type = token.TYPE

        if type not in MAPPINGS:

            raise NameError(f"Invalid token at:\n{token}")

        function = MAPPINGS[type]

        return function(token, pos_id)

    def _function(self, token: Token, pos_id: PositionId):

        name_token = self._step_pos(pos_id)

        if name_token is None:

            raise NameError(f"Missing function name at:\t\n{token}")

        function_reference = Constants.FUNCTION_NAME + Constants.REFERENCE_OPERATOR

        self._variables[function_reference + name_token.VALUE] = (
            self._positions[pos_id] + 1
        )

        while ((next := self._step_pos(pos_id)) is not None) and (
            next.VALUE not in [TokenType.FUNCTION, TokenType.MAIN]
        ):
            pass

        self._positions[pos_id] -= 1

    def _identifier(self, token: Token, pos_id: PositionId):

        variable_name = token.VALUE

        if variable_name in self._variables:

            self._append_to_stack(self._variables[variable_name])

        else:

            raise NameError(
                f"Variable '{variable_name}' not defined at:" + f"\n\t{token}."
            )
            # TODO: Implement "Null" type
            self._append_to_stack(None)

    def _int(self, token: Token, pos_id: PositionId):

        self._append_to_stack(int(token.VALUE))

    def _line_terminator(self, token: Token, pos_id: PositionId):

        pass

    def _main(self, token: Token, pos_id: PositionId):

        main_token = self._step_pos(pos_id)

        if main_token is None:

            raise NameError(f"Missing name of main at:\n\t{token}")

        main_reference = Constants.MAIN_NAME + Constants.REFERENCE_OPERATOR

        self._variables[main_reference + main_token.VALUE] = self._positions[pos_id]

    def _out(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)
        self._eval_position(pos_id)
        print(self._pop_from_stack(), end="")
        self._step_pos(pos_id)

    def _pop_from_stack(self, stack_name: str = Constants.MAIN_NAME):

        stack_reference = stack_name + Constants.REFERENCE_OPERATOR

        top_pointer = stack_reference + "tp"

        if top_pointer not in self._variables:

            # TOO: Add NULL
            return None

        top_value_pointer = stack_reference + str(self._variables[top_pointer])

        top_value = self._variables[top_value_pointer]

        del self._variables[top_value_pointer]

        self._variables[top_pointer] -= 1

        if self._variables[top_pointer] <= -1:

            del self._variables[top_pointer]

        return top_value

    def _raw_set(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)

        self._eval_position(pos_id)

        name = str(self._pop_from_stack())

        self._step_pos(pos_id)
        self._eval_position(pos_id)

        self._variables[name] = self._pop_from_stack()
        self._step_pos(pos_id)

    def _run_position_id(self, pos_id: PositionId, start: int):

        self._positions[pos_id] = start

        while pos_id in self._positions:

            self._eval_position(pos_id)
            self._step_pos(pos_id)

    def _set(self, token: Token, pos_id: PositionId):

        next_token = self._step_pos(pos_id)

        if next_token is None:

            raise NameError(
                f"Name of assignment operator not found at:\n\t{token}."
            ) from None

        variable_name = next_token.VALUE

        self._step_pos(pos_id)

        self._eval_position(pos_id)

        self._variables[variable_name] = self._pop_from_stack()

        self._step_pos(pos_id)

    def _step_pos(self, pos_id: PositionId) -> None | Token:

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
