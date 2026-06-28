from executable import Executable
from linker import Linker
from parser import Parser
from sys import argv


def main():

    if len(argv) < 2:

        raise NameError(
            "Missing source code file; intended use is "
            + "'python interpreter.py FILE_PATH FILE_ARGS'.\n"
            + "Run python 'interpreter.py -h' for details."
        )

    file_path = argv[1]

    if file_path == "-h":

        print("Usage:\n\t"+"python intrepreter.py FILE_PATH FILE_ARGS")
        return

    linked_code = Linker.link(file_path)

    parsed_code = Parser.parse(linked_code)

    code_executable = Executable(file_path, parsed_code)

    code_executable.run(argv[2:])


if __name__ == "__main__":
    main()
