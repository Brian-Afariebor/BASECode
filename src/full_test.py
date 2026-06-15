from linker import Linker
from parser import Parser
from executable import Executable
from executable import ExecutionMode # pyright: ignore[reportUnusedImport]

file_path = "tests/HelloWorld.bc"

linked_code = Linker.resolve(file_path)

parsed_code = Parser.parse(linked_code)

code_executable = Executable(
    "Hello World",
    parsed_code,
)

code_executable.run()
