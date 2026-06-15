from linker import Linker
from parser import Parser
from executable import Executable
from executable import ExecutionMode

file_path = "tests/hello_world.bc"

linked_code = Linker.resolve(file_path)

parsed_code = Parser.parse(linked_code)

code_executable = Executable(
    "Hello World",
    parsed_code,
    ExecutionMode.DOCSTRINGS,
)

code_executable.run()
