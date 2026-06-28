import unittest

import executable
import linker
import parser
import tokens


class TestLinker(unittest.TestCase):

    def test_no_links(self):

        file_path = "samples/HelloWorld.bc"

        linked_code = linker.Linker.resolve(file_path)

        with open(file_path) as source_file:

            true_code = source_file.read()

        self.assertEqual(linked_code, true_code)

    def test_link(self):

        unlinked_file_path = "samples/Main.bc"
        linked_file_path = "samples/LinkedMain.bc"

        linked_code = linker.Linker.resolve(unlinked_file_path)

        with open(linked_file_path) as source_file:

            true_code = source_file.read()

        self.assertEqual(linked_code, true_code)


class TestExecutable(unittest.TestCase):

    def test_minimal_hello_world(self):

        hello_world_code = 'out "Hello, World!";'
        parsed_code = parser.Parser.parse(hello_world_code)
        self.assertEqual(
            parsed_code,
            [
                tokens.Token(
                    parser.TokenType.OUT,
                    "out",
                    1,
                    1,
                ),
                tokens.Token(
                    parser.TokenType.WHITESPACE,
                    " ",
                    1,
                    4,
                ),
                tokens.Token(
                    parser.TokenType.STRING,
                    '"Hello, World!"',
                    1,
                    5,
                ),
                tokens.Token(
                    parser.TokenType.LINE_TERMINATOR,
                    ";",
                    1,
                    20,
                ),
            ],
        )


if __name__ == "_main__":

    unittest.main()
