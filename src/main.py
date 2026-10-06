from filter import FilteredTokenStream

from implementations import end
from interpreter import Interpreter
from tokens import Token
from token_types import Type

if __name__ == "__main__":

    Interpreter.register(end, Type.END)
    Interpreter.run(
        FilteredTokenStream(
            [
                Token("end", Type.END, 0, 0),
                Token(")", Type.UNMAPPED, 0, 0),
            ]
        )
    )
