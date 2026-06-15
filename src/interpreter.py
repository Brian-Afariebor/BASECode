from executable import Executable
from linker import Linker
from parser import Parser

from sys import argv

def main():

    file_path = argv[1]
    args = argv[2:]

    linked_code = Linker.resolve(file_path)

    parsed_code = Parser.parse(linked_code)

    code_executable = Executable("Hello World",parsed_code)

    code_executable.run(*args)

if __name__ == "__main__":

    main()