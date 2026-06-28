import unittest

from constants import Constants
from executable import Executable
from linker import Linker
from parser import Parser
from tokens import Token


class LinkerTest(unittest.TestCase):

    def test_no_links(self):

        file_path = "samples/HelloWorld.bc"

        linked_code = Linker.link(file_path)

        with open(file_path) as source_file:

            true_code = source_file.read()

        self.assertEqual(linked_code, true_code)

    def test_link(self):

        unlinked_file_path = "samples/Main.bc"
        linked_file_path = "samples/LinkedMain.bc"

        linked_code = Linker.link(unlinked_file_path)

        with open(linked_file_path) as source_file:

            true_code = source_file.read()

        self.assertEqual(linked_code, true_code)


class ParserTest(unittest.TestCase):

    def test_minimal_hello_world(self):

        hello_world_code = 'out "Hello, World!";'
        parsed_code = Parser.parse(hello_world_code)
        self.assertEqual(
            parsed_code,
            [
                Token(
                    Constants.OUT_TYPE,
                    "out",
                    1,
                    1,
                ),
                Token(
                    Constants.WHITESPACE_TYPE,
                    " ",
                    1,
                    4,
                ),
                Token(
                    Constants.STRING_TYPE,
                    '"Hello, World!"',
                    1,
                    5,
                ),
                Token(
                    Constants.LINE_TERMINATOR_TYPE,
                    ";",
                    1,
                    20,
                ),
            ],
        )

class ExecutableTest(unittest.TestCase):

    def test_end(self):

        for i  in range(-10,11):

            resolved_code = f"end {i/10};"
            parsed_code = Parser.parse(resolved_code)
            code_executable = Executable("EndTest",parsed_code)
            self.assertEqual(code_executable.run(),i/10)



if __name__ == "__main__":

    unittest.main()
