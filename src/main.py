from filter import FilteredTokenStream
from interpreter import Interpreter
from mappings import register_all
from tokens import Token
from token_types import Type

if __name__ == "__main__":

    register_all()
    
    Interpreter.run(
        FilteredTokenStream(
            [
                Token("end", Type.END, 0, 0),
                Token(")", Type.UNMAPPED, 0, 0),
            ]
        )
    )
