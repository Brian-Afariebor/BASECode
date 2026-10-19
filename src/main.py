from filter import Filter
from interpreter import Interpreter
from linker import LinkedCode
from mappings import register_all 
from parser import Parser

def main():

    register_all()

    # TODO - Add linking
    tokens = Parser.parse(LinkedCode("end(-3.141);"))

    filtered_tokens = Filter.filter(tokens)

    if filtered_tokens is None:

        # TODO - Add error
        return

    print(Interpreter.run(filtered_tokens))

if __name__ == "__main__":

    main()
