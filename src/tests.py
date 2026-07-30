from collections.abc import Callable
from constants import Constants
from executable import Executable
from linker import Linker
from main import Main
from parser import Parser

from time import perf_counter
from time import sleep

from tokens import Token
from tokens import TokenStream

import unittest

hello_world_file_path = "samples/HelloWorld.bc"
unlinked_code_file_path = "samples/Main.bc"
linked_code_file_path = "samples/LinkedMain.blc"
loop_file_path = "samples/Loop.bc"

with open(linked_code_file_path) as source_file:

    linked_code_code = source_file.read()

with open(hello_world_file_path) as source_file:

    # HelloWorld.bc is unlinked, so this is fine.
    hello_world_code = source_file.read()


def get_time(function: Callable[[], None]):

    start_time = perf_counter()

    function()

    delta = perf_counter() - start_time

    return delta


class TimerTest(unittest.TestCase):

    def test_timer(self):

        self.assertAlmostEqual(1, get_time(self.sleep_one_second), 2)

    def sleep_one_second(self):

        sleep(1)


class LinkerTest(unittest.TestCase):

    def test_no_links(self):

        linked_code = Linker.link(hello_world_file_path)

        self.assertEqual(linked_code, hello_world_code)

    def test_link(self):

        linked_code = Linker.link(unlinked_code_file_path)

        self.assertEqual(linked_code, linked_code_code)


class ParserTest(unittest.TestCase):

    def test_minimal_hello_world(self):

        hello_world_code = 'out "Hello, World!";'
        parsed_code = Parser.parse(hello_world_code)
        self.assertEqual(
            parsed_code,
            [
                Token(
                    Constants.Types.OUT,
                    "out",
                    1,
                    1,
                ),
                Token(
                    Constants.Types.WHITESPACE,
                    " ",
                    1,
                    4,
                ),
                Token(
                    Constants.Types.STRING,
                    '"Hello, World!"',
                    1,
                    5,
                ),
                Token(
                    Constants.Types.LINE_TERMINATOR,
                    ";",
                    1,
                    20,
                ),
            ],
        )

    def parse_big_code(self):

        with open(loop_file_path) as code_file:

            code = code_file.read()

        Parser.parse(code)

    def parse_small_code(self):

        hello_world_code = 'out "Hello, World!"; end 0;'
        Parser.parse(hello_world_code)

    def test_small_code_parsing_speed(self):

        speed_requirement = 0.01
        reps = 1000

        for _ in range(reps):
            self.assertLessEqual(
                get_time(self.parse_small_code),
                speed_requirement,
                f"Small Code Parsing did not meet speed requirement "
                + str(speed_requirement)
                + "seconds.",
            )

    def test_big_code_parsing_speed(self):

        speed_requirement = 0.01
        reps = 100

        for _ in range(reps):

            self.assertLessEqual(
                get_time(self.parse_big_code),
                speed_requirement,
                f"Big Code Parsing did not meet speed requirement of "
                + str(speed_requirement)
                + " seconds.",
            )


class ExecutableTest(unittest.TestCase):

    def execute_parsed_code(self, name: str, parsed_code: TokenStream):

        Executable(name, parsed_code).run()

    def test_end(self):

        for i in range(-10, 11):

            resolved_code = f"end {i/10};"
            parsed_code = Parser.parse(resolved_code)
            code_executable = Executable("EndTest", parsed_code)
            self.assertEqual(code_executable.run(), i / 10)

    def test_small_code_execution_speed(self):

        hello_world_code = "end 0;"
        parsed_code = Parser.parse(hello_world_code)
        speed_requirement = 0.02
        reps = 1000

        def run_code():

            self.execute_parsed_code("HelloWorld", parsed_code)

        for _ in range(reps):
            self.assertLessEqual(
                get_time(run_code),
                speed_requirement,
                f"Small Code Executable did not meet speed requirement of "
                + str(speed_requirement)
                + " seconds.",
            )


class MainTest(unittest.TestCase):

    def run_code(self, file_path: str):

        main = Main(["-f", file_path])
        main.run()

    def test_small_code_execution_speed(self):

        file_path = "samples/Comments.bc"
        speed_requirement = 0.01
        reps = 100

        def run_code():

            self.run_code(file_path)

        for _ in range(reps):

            self.assertLessEqual(
                get_time(run_code),
                speed_requirement,
                f"Small Main Test did not meet speed requirement of "
                + str(speed_requirement)
                + " seconds.",
            )

    def test_large_code_execution_speed(self):

        file_path = loop_file_path
        speed_requirement = 0.05
        reps = 100

        def run_code():

            self.run_code(file_path)

        for _ in range(reps):

            self.assertLessEqual(
                get_time(run_code),
                speed_requirement,
                f"Large Main Test did not meet speed requirement of "
                + str(speed_requirement)
                + " seconds.",
            )


if __name__ == "__main__":

    unittest.main()
