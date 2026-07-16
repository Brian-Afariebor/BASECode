from collections.abc import Callable
from constants import Constants
from executable import Executable
from linker import Linker
from parser import Parser
from parser import TokenStream
from sys import argv


class Main:

    def __init__(self, args: list[str]):

        self.ARGS = args

        self._current_flag = 0

        # * Linking
        self._link_code_flag = True
        self._save_linked_code_flag = False
        self._linked_code_file = ""

        # * Parsing
        self._parse_code_flag = True
        self._save_parsed_code_flag = False
        self._parsed_code_file = ""

        # * Execution

        # * Dependencies
        self._run_code_flag = True
        self._file_path = ""
        self._code_name = ""
        self._execution_modes: list[str] = []
        self._code_args: list[str] = []

        # * Pre-execution
        self._save_trimmed_code_flag = False
        self._trimmed_code_file = ""

        # * Post-execution

    def run(self):

        self._run_flags()

        linked_code = self._link_code()

        if not self._parse_code_flag:

            return

        parsed_code = Parser.parse(linked_code)

        self._run_code(parsed_code)

    def _docstring(self):

        self._execution_modes.append(Constants.ExecutionModes.DOCSTRINGS)
        
    def _enable_no_link(self):

        self._link_code_flag = False

    def _enable_save_link(self):

        self._current_flag += 1

        if self._current_flag >= len(self.ARGS):

            raise FileNotFoundError(
                f"File missing; see {Constants.Flags.HELP} for details."
            ) from None

        self._save_linked_code_flag = True
        self._linked_code_file = self.ARGS[self._current_flag]


    def _enable_save_trimmings(self):

        self._current_flag += 1

        if self._current_flag >= len(self.ARGS):

            raise FileNotFoundError(
                f"File missing; see {Constants.Flags.HELP} for details."
            ) from None

        self._save_trimmed_code_flag = True
        self._trimmed_code_file = self.ARGS[self._current_flag]

    def _eval(self):

        MAPPINGS: dict[str, Callable[[], None]] = {
            Constants.Flags.FILE: self._file,
            Constants.Flags.HELP: self._help,
            Constants.Flags.NAME: self._name,
            Constants.Flags.NO_LINK: self._enable_no_link,
            Constants.Flags.PRINT_DOCSTRINGS: self._docstring,
            Constants.Flags.SAVE_LINK: self._enable_save_link,
            Constants.Flags.SAVE_TRIMMINGS: self._enable_save_trimmings
        }

        current_flag = self.ARGS[self._current_flag]

        if current_flag not in MAPPINGS:

            raise SyntaxError(
                f"Unknown flag '{current_flag}'; "
                + f"see {Constants.Flags.HELP} for details."
            ) from None

        function = MAPPINGS[current_flag]

        return function()

    def _file(self):

        self._current_flag += 1

        if self._current_flag >= len(self.ARGS):

            raise FileNotFoundError(
                f"File missing; see {Constants.Flags.HELP} for details."
            ) from None

        self._file_path = self.ARGS[self._current_flag]

    def _help(self):

        raise SyntaxError("") from None

    def _link_code(self):

        if self._link_code_flag:

            linked_code = Linker.link(self._file_path)

        else:

            with open(self._file_path) as code_file:

                linked_code = code_file.read()

        if self._save_linked_code_flag:
            
            self._save_linked_code(linked_code)

        return linked_code

    def _name(self):

        self._current_flag += 1

        if self._current_flag >= len(self.ARGS):

            raise SyntaxError(
                f"Name missing; see {Constants.Flags.HELP} for details."
            ) from None

        self._code_name = self.ARGS[self._current_flag]

    def _run_code(self, parsed_code: TokenStream):

        code_executable = Executable(
            self._code_name if self._code_name != "" else self._file_path,
            parsed_code,
            *self._execution_modes,
        )

        if self._save_trimmed_code_flag:
            
            self._save_trimmed_code(code_executable)

        if self._run_code_flag:
            
            code_executable.run(*self._code_args)

    def _run_flags(self):

        self._current_flag = 0

        while self._current_flag < len(self.ARGS):
            
            self._eval()
            
            self._current_flag += 1

    def _save_linked_code(self, linked_code: str):

        with open(self._linked_code_file, "w") as linked_code_file:

            linked_code_file.write(linked_code)         

    def _save_trimmed_code(self, code_executable: Executable):

        with open(self._trimmed_code_file, "w") as trimmed_code_file:

            for token in code_executable.TOKENS:

                token_content = token.VALUE

                trimmed_code_file.write(token_content)

                if "\"" in token_content:
                    continue

                if token_content not in [")",";"]:

                    trimmed_code_file.write(" ")


MAIN = Main(argv[1:])

if __name__ == "__main__":

    MAIN.run()
