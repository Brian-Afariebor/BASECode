from collections.abc import Callable

from constants import BASECodeValue
from constants import ExecutionMode
from constants import Keyword
from constants import Null
from constants import NULL
from constants import reference
from constants import Type
from constants import Type

from re import sub

from threading import Thread

from tokens import Token
from tokens import TokenStream

from typing import Any

type Context = dict[str, BASECodeValue]
type PositionId = str
type FunctionMap = dict[Type, Callable[[Token, PositionId], None]]


class Executable:

    def __init__(
        self,
        name: str,
        tokens: TokenStream,
        *args: ExecutionMode,
    ):

        self.NAME = name

        self.modes = args

        self._last_return_value = NULL

        name_ref = reference(Keyword.MAIN_NAME) + "name"

        self._variables: Context = {name_ref: self.NAME}

        self._positions: dict[PositionId, int] = {
            Keyword.MAIN_NAME: 0,
        }
        """Positions are zero-indexed
        """

        tokens = list(
            filter(
                lambda token: token.TYPE
                not in [
                    Type.WHITESPACE,
                    Type.SHEBANG,
                    Type.COMMENT,
                    Type.DUMMY,
                ],
                tokens,
            ),
        )

        if ExecutionMode.DOCSTRINGS in self.modes:

            tokens = list(
                filter(
                    lambda token: token.TYPE == Type.DOCSTRING,
                    tokens,
                )
            )

        else:

            tokens = list(
                filter(
                    lambda token: token.TYPE != Type.DOCSTRING,
                    tokens,
                )
            )

        self.TOKENS = tokens

    @property
    def positions(self):

        return self._positions.copy()

    @property
    def variables(self):

        return self._variables.copy()

    def run(self, *args: BASECodeValue):

        self._variables.clear()

        for pos, arg in enumerate(args):

            self._variables[
                reference(
                    reference(
                        Keyword.MAIN_NAME,
                    )
                    + "args",
                )
                + str(pos)
            ] = arg

        self._run_pos_id(Keyword.MAIN_NAME)
        return self._last_return_value

    def _add(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)
        self._eval_pos(pos_id)
        item1 = self._pop_from_stack()

        if isinstance(item1, Null):

            raise ValueError(
                "Null was given as an addition value at:"
                + f"\n\t{self._token_at_pos_id(pos_id)}",
            )

        self._step_pos(pos_id)
        self._eval_pos(pos_id)
        item2 = self._pop_from_stack()

        if isinstance(item2, Null):

            raise ValueError(
                "Null was given as an addition value at:"
                + f"\n\t{self._token_at_pos_id(pos_id)}",
            )

        if isinstance(item1, str):

            item2 = str(item2)

            self._append_to_stack(item1 + item2)
            return

        if isinstance(item2, str):

            item2 = float(item2)

        self._append_to_stack(item1 + item2)

    def _append_to_stack(
        self,
        value: Any,
        stack_name: str = Keyword.MAIN_NAME,
    ):

        first_value = reference(stack_name) + "0"
        top_pointer = reference(stack_name) + "tp"

        if first_value not in self._variables:

            self._variables[first_value] = value
            self._variables[top_pointer] = 0

            return

        if not isinstance(self._variables[top_pointer], int):

            raise ValueError(f"Non-int top pointer found on stack {stack_name}")

        self._variables[top_pointer] += 1  # pyright: ignore[reportOperatorIssue]
        self._variables[
            reference(
                stack_name,
            )
            + str(
                self._variables[top_pointer],
            )
        ] = value

    def _call(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)
        self._eval_pos(pos_id)
        self._step_pos(pos_id)

        # NOTE: We have to account for the parenthesis and semicolon
        return_pos = self._positions[pos_id] + 1
        new_position = self._pop_from_stack()

        if not isinstance(new_position, int):

            raise ValueError(
                f"Non-int '{new_position}' was given as a jump position at:\n\t"
                + repr(self._token_at_pos_id(pos_id))
            ) from None

        adjusted_position = int(new_position) - 1

        if adjusted_position < 0:

            raise ValueError(
                f"Given jump position {new_position} was too small. "
                + f"Given at:\n\t{self._token_at_pos_id(pos_id)}"
            ) from None

        if adjusted_position >= len(self.TOKENS):

            raise ValueError(
                f"Given jump position {new_position} was too big at:"
                + f"\n\t{self._token_at_pos_id(pos_id)}"
            ) from None

        self._positions[pos_id] = adjusted_position
        self._append_to_stack(return_pos)

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

        if pos_id == Keyword.MAIN_NAME:

            self._positions.clear()
            print(
                "\n" * 5
                + f"Program '{self.NAME}' ended with a "
                + f"return value of {return_value}."
            )

    def _eval_pos(self, pos_id: PositionId) -> None:

        position = self._positions[pos_id]

        token = self._token_at_pos(position)

        type = token.TYPE

        # NOTE: Using a match makes it less likely to miss a type
        match type:
            # SECTION: Valid types
            case Type.ADD:
                return self._add(token, pos_id)
            case Type.CALL:
                return self._call(token, pos_id)
            case Type.DELETE:
                return self._delete(token, pos_id)
            case Type.DOCSTRING:
                return self._docstring(token, pos_id)
            case Type.END:
                return self._end(token, pos_id)
            case Type.FLOAT:
                return self._float(token, pos_id)
            case Type.FUNCTION:
                return self._function(token, pos_id)
            case Type.IDENTIFIER:
                return self._identifier(token, pos_id)
            case Type.IF:
                return self._if(token, pos_id)
            case Type.INPUT:
                return self._input(token, pos_id)
            case Type.INT_CAST:
                return self._int_cast(token, pos_id)
            case Type.INTEGER:
                return self._int(token, pos_id)
            case Type.JUMP:
                return self._jump(token, pos_id)
            case Type.LINE_TERMINATOR:
                return self._line_terminator(token, pos_id)
            case Type.MAIN:
                return self._main(token, pos_id)
            case Type.OUT:
                return self._out(token, pos_id)
            case Type.POP:
                return self._pop(token, pos_id)
            case Type.PUSH:
                return self._push(token, pos_id)
            case Type.RAW_SET:
                return self._raw_set(token, pos_id)
            case Type.REFERENCE:
                return self._reference(token, pos_id)
            case Type.RETURN:
                return self._return(token, pos_id)
            case Type.SET:
                return self._set(token, pos_id)
            case Type.START:
                return self._start(token, pos_id)
            case Type.STOP:
                return self._stop(token, pos_id)
            case Type.STRING:
                return self._string(token, pos_id)

            # !SECTION
            # SECTION: Invalid types
            case Type.COMMENT:
                raise SyntaxError(
                    f"Given non-runnable keyword token at:\n\t{token}",
                )

            case Type.DUMMY:
                raise SyntaxError(
                    f"Given non-runnable keyword token at:\n\t{token}",
                )

            case Type.ELSE:
                raise SyntaxError(
                    f"Given non-runnable keyword token at:\n\t{token}",
                )

            case Type.FUNCTION_TERMINATOR:
                raise SyntaxError(
                    f"Given non-runnable keyword token at:\n\t{token}",
                )

            case Type.SHEBANG:
                raise SyntaxError(
                    f"Given non-runnable keyword token at:\n\t{token}",
                )

            case Type.WHITESPACE:
                raise SyntaxError(
                    f"Given non-runnable keyword token at:\n\t{token}",
                )

            case Type.UNMAPPED:
                raise SyntaxError(
                    f"Given non-runnable keyword token at:\n\t{token}",
                )

    def _float(self, token: Token, pos_id: PositionId):

        self._append_to_stack(float(token.VALUE))

    def _function(self, token: Token, pos_id: PositionId):

        name_token = self._step_pos(pos_id)

        if name_token is None:

            raise NameError(f"Missing function name at:\n\t{token}")

        self._variables[
            reference(
                Keyword.FUNCTION_NAME,
            )
            + name_token.VALUE
        ] = (
            self._positions[pos_id] + 1
        )

        while ((next := self._step_pos(pos_id)) is not None) and (
            next.TYPE not in [Type.FUNCTION, Type.MAIN]
        ):
            pass

        self._positions[pos_id] -= 1

    def _identifier(self, token: Token, pos_id: PositionId):

        variable_name = token.VALUE

        if variable_name in self._variables:

            self._append_to_stack(self._variables[variable_name])

        else:

            self._append_to_stack(NULL)

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
            next.TYPE != Type.ELSE
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

        if isinstance(value, Null):

            raise ValueError(
                "Null was given as an int cast value at:" + f"\n\t{token}",
            )

        self._append_to_stack(int(value))
        self._step_pos(pos_id)

    def _jump(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)
        self._eval_pos(pos_id)

        new_position = self._pop_from_stack()

        if not isinstance(new_position, int):

            raise ValueError(
                f"Non-int '{new_position}' was given as a jump position at:\n\t"
                + repr(self._token_at_pos_id(pos_id))
            ) from None

        adjusted_position = int(new_position) - 1

        if adjusted_position < 0:

            raise ValueError(
                f"Given jump position '{new_position}' was too small at:\n\t"
                + repr(self._token_at_pos_id(pos_id))
            ) from None

        if adjusted_position >= len(self.TOKENS):

            raise ValueError(
                f"Given jump position '{new_position}' was too big at:\n\t"
                + repr(self._token_at_pos_id(pos_id))
            ) from None

        self._positions[pos_id] = adjusted_position

    def _line_terminator(self, token: Token, pos_id: PositionId):

        pass

    def _main(self, token: Token, pos_id: PositionId):

        main_token = self._step_pos(pos_id)

        if main_token is None:

            raise SyntaxError(
                f"Missing name of main at:\n\t{self._token_at_pos_id(pos_id)}"
            )

        self._variables[
            reference(
                Keyword.MAIN_NAME,
            )
            + main_token.VALUE
        ] = self._positions[pos_id]

    def _out(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)
        self._eval_pos(pos_id)
        print(self._pop_from_stack(), end="")
        self._step_pos(pos_id)

    def _pop(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)

        stack_name = self._token_at_pos_id(pos_id).VALUE

        self._append_to_stack(self._pop_from_stack(stack_name))

        self._step_pos(pos_id)

    def _pop_from_stack(
        self, stack_name: str = Keyword.MAIN_NAME
    ) -> Null | int | float | str:

        stack_reference = reference(stack_name)

        top_pointer = stack_reference + "tp"

        if top_pointer not in self._variables:

            return NULL

        top_value_pointer = stack_reference + str(self._variables[top_pointer])

        top_value = self._variables[top_value_pointer]

        del self._variables[top_value_pointer]

        if not isinstance(self._variables[top_pointer], int):

            raise ValueError(f"Non-int top pointer found on stack {stack_name}")

        # We know that self._variables[top_pointer] is an int;
        # so this will not fail.

        self._variables[top_pointer] -= 1  # pyright: ignore[reportOperatorIssue]

        if self._variables[top_pointer] <= -1:  # pyright: ignore[reportOperatorIssue]

            del self._variables[top_pointer]

        return top_value

    def _push(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)

        stack_name = self._token_at_pos_id(pos_id).VALUE

        self._step_pos(pos_id)
        self._eval_pos(pos_id)

        self._append_to_stack(self._pop_from_stack(), stack_name)

        self._step_pos(pos_id)

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

    def _return(self, token: Token, pos_id: PositionId):

        return_position = self._pop_from_stack()

        if not isinstance(return_position, int):

            raise ValueError(
                f"Non-int return position '{return_position}'given at:\n\t"
                + f"{self._token_at_pos_id(pos_id)}"
            )

        self._step_pos(pos_id)
        self._eval_pos(pos_id)
        self._positions[pos_id] = return_position

    def _run_pos_id(self, pos_id: PositionId, start: int = 0):

        self._positions[pos_id] = start

        while pos_id in self._positions:

            self._eval_pos(pos_id)
            self._step_pos(pos_id)

    def _set(self, token: Token, pos_id: PositionId):

        next_token = self._step_pos(pos_id)

        if next_token is None:

            raise SyntaxError(
                f"Name of variable not found at:\n\t{token}.",
            ) from None

        variable_name = next_token.VALUE

        self._step_pos(pos_id)

        self._eval_pos(pos_id)

        self._variables[variable_name] = self._pop_from_stack()

        self._step_pos(pos_id)

    def _start(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)

        thread_pos_id = self._token_at_pos_id(pos_id).VALUE

        self._step_pos(pos_id)
        self._eval_pos(pos_id)

        function_location = self._pop_from_stack()

        if isinstance(function_location, Null):

            raise ValueError(f"Null was given as a jump target at:\n\t{token}")

        Thread(
            target=self._run_pos_id,
            args=(thread_pos_id, function_location),
            name=thread_pos_id,
        ).start()

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
                f"End of Code reached by thread {pos_id} "
                + f"at:\n\t{self._token_at_pos(old_position)}"
            ) from None

        self._positions[pos_id] += 1

        return self._token_at_pos_id(pos_id)

    def _stop(self, token: Token, pos_id: PositionId):

        self._step_pos(pos_id)

        thread_pos_id = self._token_at_pos_id(pos_id).VALUE

        if thread_pos_id in self._positions:
            del self._positions[thread_pos_id]

        self._step_pos(pos_id)

    def _string(self, token: Token, pos_id: PositionId):

        string = token.VALUE[1:-1]

        string = sub(r"\\t", r"\t", string)
        string = sub(r"\\n", r"\n", string)
        string = sub(r"\\q", '"', string)

        self._append_to_stack(string, "main")

    def _token_at_pos(self, pos: int):

        if pos >= len(self.TOKENS):

            raise EOFError(f"No tokens at position {pos+1}") from None

        return self.TOKENS[pos]

    def _token_at_pos_id(self, pos_id: PositionId):

        return self._token_at_pos(self._positions[pos_id])
