from filter import FilteredTokenStream
from interpreter import Interpreter
from linker import LinkedCode
from mappings import register_all
from parser import Parser

if __name__ == "__main__":

    register_all()

    # TODO - Add linking
    tokens = Parser.parse(LinkedCode("end-1"))

    # TODO - Add filtering
    filtered_tokens = FilteredTokenStream(tokens)

    print(Interpreter.run(filtered_tokens))
