from collections.abc import Callable
from re import sub
from typing import Any

from constants import Constants
from tokens import Token
from tokens import TokenStream

type Context = dict[str, Any]
type PositionId = str
type FunctionMap = dict[str, Callable[[Token, PositionId], None]]


class Executable:

    def __init__(
        self,
        name: str,
        tokens: TokenStream,
        *args: str,
    ):

        self.NAME = name

        self.modes = args

        # TODO: Add Null
        self._last_return_value = None

        self._variables: Context = {
            Constants.reference(Constants.Keywords.MAIN_NAME) + "name": self.NAME
        }
        self._positions: dict[PositionId, int] = {Constants.Keywords.MAIN_NAME: 0}

        tokens = list(
            filter(
                lambda token: token.TYPE
                not in [
                    Constants.Types.WHITESPACE,
                    Constants.Types.SHEBANG,
                    Constants.Types.COMMENT,
                    Constants.Types.DUMMY,
                ],
                tokens,
            ),
        )

        if Constants.ExecutionModes.DOCSTRINGS in self.modes:

            tokens = list(
                filter(
                    lambda token: token.TYPE == Constants.Types.DOCSTRING,
                    tokens,
                )
            )

        else:

            tokens = list(
                filter(
                    lambda token: token.TYPE != Constants.Types.DOCSTRING,
                    tokens,
                )
            )

        self.TOKENS = tokens

    def run(self, *args: Any):

        self._variables.clear()

        for pos, arg in enumerate(args):

            self._variables[
                Constants.reference(
                    Constants.reference(
                        Constants.Keywords.MAIN_NAME,
                    )
                    + "args",
                )
                + str(pos)
            ] = arg

        self._run_position_id(Constants.Keywords.MAIN_NAME, 0)
        return self._last_return_value

    def _add(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)
        self._eval_pos(pos_id)
        item1 = self._pop_from_stack()
        if item1 is None:

            raise ValueError("None was given as an addition value at:" + f"\n\t{token}")

        self._step_pos(pos_id)
        self._eval_pos(pos_id)
        item2 = self._pop_from_stack()

        self._append_to_stack(item1 + item2)

    def _append_to_stack(
        self,
        value: Any,
        stack_name: str = Constants.Keywords.MAIN_NAME,
    ):

        first_value = Constants.reference(stack_name) + "0"
        top_pointer = Constants.reference(stack_name) + "tp"

        if first_value not in self._variables:

            self._variables[first_value] = value
            self._variables[top_pointer] = 0

            return

        self._variables[top_pointer] += 1
        self._variables[
            Constants.reference(
                stack_name,
            )
            + str(
                self._variables[top_pointer],
            )
        ] = value

    def _current_token(self, pos_id: PositionId):

        return self.TOKENS[self._positions[pos_id]]

    def _delete(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)

        variable_token = self._token_at_pos_id(pos_id)
        variable_name = variable_token.VALUE

        if variable_name in self._variables:

            del self._variables[variable_name]

        self._step_pos(pos_id)

    def _docstring(self, token: Token, pos_id: PositionId):

        docstring = token.VALUE
        docstring = sub(r"\/\*\*", "", docstring)
        docstring = sub(r"\*\/", "", docstring)
        print(docstring.strip() + "\n" * 2)

    def _end(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)
        self._eval_pos(pos_id)

        del self._positions[pos_id]

        return_value = self._pop_from_stack("main")
        self._last_return_value = return_value

        if pos_id == Constants.Keywords.MAIN_NAME:

            self._positions.clear()
            print(
                "\n" * 5
                + f"Program '{self.NAME}' ended with a "
                + f"return value of {return_value}."
            )

    def _eval_pos(self, pos_id: PositionId) -> None:

        MAPPINGS: FunctionMap = {
            Constants.Types.ADD: self._add,
            Constants.Types.DELETE: self._delete,
            Constants.Types.DOCSTRING: self._docstring,
            Constants.Types.END: self._end,
            Constants.Types.FLOAT: self._float,
            Constants.Types.FUNCTION: self._function,
            Constants.Types.IDENTIFIER: self._identifier,
            Constants.Types.IF: self._if,
            Constants.Types.INPUT: self._input,
            Constants.Types.INT_CAST: self._int_cast,
            Constants.Types.INTEGER: self._int,
            Constants.Types.JUMP: self._jump,
            Constants.Types.LINE_TERMINATOR: self._line_terminator,
            Constants.Types.MAIN: self._main,
            Constants.Types.OUT: self._out,
            Constants.Types.RAW_SET: self._raw_set,
            Constants.Types.REFERENCE: self._reference,
            Constants.Types.SET: self._set,
            Constants.Types.STRING: self._string,
        }

        position = self._positions[pos_id]

        token = self._token_at_pos(position)

        type = token.TYPE

        if type not in MAPPINGS:

            raise SyntaxError(f"Invalid token at:\n{token}")

        function = MAPPINGS[type]

        return function(token, pos_id)

    def _float(self, token: Token, pos_id: PositionId):

        self._append_to_stack(float(token.VALUE))

    def _function(self, token: Token, pos_id: PositionId):

        name_token = self._step_pos(pos_id)

        if name_token is None:

            raise NameError(f"Missing function name at:\t\n{token}")

        self._variables[
            Constants.reference(
                Constants.Keywords.FUNCTION_NAME,
            )
            + name_token.VALUE
        ] = (
            self._positions[pos_id] + 1
        )

        while ((next := self._step_pos(pos_id)) is not None) and (
            next.TYPE not in [Constants.Types.FUNCTION, Constants.Types.MAIN]
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
            ) from None
            # TODO: Implement "Null" type
            self._append_to_stack(None)

    def _if(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)
        self._eval_pos(pos_id)

        item1 = self._pop_from_stack()

        self._step_pos(pos_id)
        self._eval_pos(pos_id)

        item2 = self._pop_from_stack()

        if item1 == item2:

            self._step_pos(pos_id)
            return

        while ((next := self._step_pos(pos_id)) is not None) and (
            next.TYPE != Constants.Types.ELSE
        ):
            pass

    def _input(self, token: Token, pos_id: PositionId):

        self._append_to_stack(input())
        self._step_pos(pos_id)

    def _int(self, token: Token, pos_id: PositionId):

        self._append_to_stack(int(token.VALUE))

    def _int_cast(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)
        self._eval_pos(pos_id)

        value = self._pop_from_stack()

        if value is None:

            raise ValueError("None was given as an int cast value at:" + f"\n\t{token}")

        self._append_to_stack(int(value))
        self._step_pos(pos_id)

    def _jump(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)
        self._eval_pos(pos_id)

        new_position = self._pop_from_stack()

        # TODO: Add Null

        if new_position is None:

            raise ValueError(
                f"None was given as a jump position at:\n\t"
                + repr(self._current_token(pos_id))
            ) from None

        adjusted_position = int(new_position) - 1

        if adjusted_position < 0:

            raise ValueError(
                f"Given jump position {new_position} was too small. "
                + f"Given at:\n\t{self._current_token(pos_id)}"
            ) from None

        if adjusted_position >= len(self.TOKENS):

            raise ValueError(
                f"Given jump position {new_position} was too big at:"
                + f"\n\t{self._current_token(pos_id)}"
            ) from None

        self._positions[pos_id] = int(new_position) - 1

    def _line_terminator(self, token: Token, pos_id: PositionId):

        pass

    def _main(self, token: Token, pos_id: PositionId):

        main_token = self._step_pos(pos_id)

        if main_token is None:

            raise SyntaxError(f"Missing name of main at:\n\t{token}")

        self._variables[
            Constants.reference(
                Constants.Keywords.MAIN_NAME,
            )
            + main_token.VALUE
        ] = self._positions[pos_id]

    def _out(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)
        self._eval_pos(pos_id)
        print(self._pop_from_stack(), end="")
        self._step_pos(pos_id)

    def _pop_from_stack(self, stack_name: str = Constants.Keywords.MAIN_NAME):

        stack_reference = Constants.reference(stack_name)

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

        self._eval_pos(pos_id)

        name = str(self._pop_from_stack())

        self._step_pos(pos_id)
        self._eval_pos(pos_id)

        self._variables[name] = self._pop_from_stack()
        self._step_pos(pos_id)

    def _reference(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)

        self._eval_pos(pos_id)

        name = str(self._pop_from_stack())

        self._append_to_stack(self._variables[name])

        self._step_pos(pos_id)

    def _run_position_id(self, pos_id: PositionId, start: int):

        self._positions[pos_id] = start

        while pos_id in self._positions:

            self._eval_pos(pos_id)
            self._step_pos(pos_id)

    def _set(self, token: Token, pos_id: PositionId):

        next_token = self._step_pos(pos_id)

        if next_token is None:

            raise SyntaxError(f"Name of variable not found at:\n\t{token}.") from None

        variable_name = next_token.VALUE

        self._step_pos(pos_id)

        self._eval_pos(pos_id)

        self._variables[variable_name] = self._pop_from_stack()

        self._step_pos(pos_id)

    def _step_pos(self, pos_id: PositionId) -> None | Token:

        if pos_id not in self._positions:

            return None

        old_position = self._positions[pos_id]

        if old_position + 1 >= len(self.TOKENS):

            if Constants.ExecutionModes.DOCSTRINGS in self.modes:

                del self._positions[pos_id]
                return

            raise EOFError(
                f"End of Code reached by thread {pos_id} "
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
