from collections.abc import Callable

from executable import Executable
from executable import ExecutionMode
from linker import Linker
from parser import Parser
from sys import argv


class Main:

    def __init__(self, args: list[str]):

        self.ARGS = args
        self._current_flag = 0
        self._file_path = ""
        self._code_name = ""
        self._execution_modes: list[ExecutionMode] = []
        self._code_args: list[str] = []

    def run(self):

        while self._current_flag < len(self.ARGS):

            self._eval()
            self._current_flag += 1

        linked_code = Linker.link(self._file_path)
        parsed_code = Parser.parse(linked_code)
        code_executable = Executable(
            self._code_name if self._code_name != "" else self._file_path,
            parsed_code,
            *self._execution_modes,
        )
        code_executable.run(*self._code_args)

    def _eval(self):

        MAPPINGS: dict[str, Callable[[], None]] = {"-f": self._file}

        current_flag = self.ARGS[self._current_flag]

        if current_flag not in MAPPINGS:

            raise NameError(f"Unknown flag {current_flag}; see -h for flags.")

        function = MAPPINGS[current_flag]

        return function()

    def _file(self):

        self._current_flag += 1

        if self._current_flag >= len(self.ARGS):

            raise FileNotFoundError("File missing; see -h for details.")

        self._file_path = self.ARGS[self._current_flag]


MAIN = Main(argv[1:])

if __name__ == "__main__":

    MAIN.run()
