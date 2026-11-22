# TODO - Remove Test print statements
print("Importing!")

from filter import Filter
from interpreter import Interpreter
from linker import LinkedCode
from mappings import register_all
from parser import Parser

def main():

    # TODO - Remove Test print statements
    print("Registering!")
    
    register_all()

    # TODO - Remove Test print statements
    print("Parsing!")

    # TODO - Add linking
    tokens = Parser.parse(
        LinkedCode(
    """
            set x = add(1.0,2);
            end(x);
            """.strip()
        ),
    )

    # TODO - Remove Test print statements
    print("Filtering!")
    
    filtered_tokens = Filter.filter(tokens)

    if filtered_tokens is None:

        # TODO - Add error
        return

    # TODO - Remove Test print statements
    print("Running!")

    print(Interpreter.run(filtered_tokens))


if __name__ == "__main__":

    # TODO - Remove Test print statements
    print("Running Main!")
    main()
