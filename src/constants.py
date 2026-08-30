from enum import auto
from enum import Enum
from enum import StrEnum

type BASECode = str


class ExecutionMode(StrEnum):

    DEBUG = "DEBUG"
    DOCSTRINGS = "DOCSTRINGS"


class File(StrEnum):

    STANDARD_LIBRARY_PATH = "lib"
    TEST_FILE_PATH = "testfiles"
    UNLINKED_BASECODE_ENDING = ".bc"
    LINKED_BASECODE_ENDING = ".blc"
    BASECODE_DIRECTORY = "/".join(__file__.split("/")[:-2])


class Flag(StrEnum):

    DEBUG = "-db"
    FILE = "-f"
    HELP = "-h"
    NAME = "-n"
    NO_LINK = "-nl"
    NO_RUN = "-nr"
    PRINT_DOCSTRINGS = "-pd"
    SAVE_LINK = "-sl"
    SAVE_PARSE = "-sp"
    SAVE_TRIMMINGS = "-st"


class Keyword(StrEnum):

    ADD = "add"
    CALL = "call"
    DEBUG = "dbg"
    DELETE = "del"
    ELSE = "else"
    END = "end"
    FUNCTION = "fn"
    FUNCTION_NAME = "function"
    IF = "if"
    IMPORT = "imp"
    INPUT = "in"
    INT_CAST = "int"
    JUMP = "jmp"
    LINE_TERMINATOR = ";"
    MAIN = "mn"
    MAIN_NAME = "main"
    OUT = "out"
    POP = "pop"
    PUSH = "push"
    RAW_SET = "rset"
    RAW_STACK_SET = "rsks"
    REFERENCE = "ref"
    REFERENCE_OPERATOR = "::"
    REMOVE = "rem"
    RETURN = "ret"
    SET = "set"
    START = "start"
    STOP = "stop"


class Regex(StrEnum):

    COMMENT = r"\/\*[\s\S]*?\*\/|\/\/.*"
    DOCSTRING = r"\/\*\*[\s\S]*?\*\/|\/\/\/"
    DUMMY = r"\(|{|}|,|="
    FLOAT = r"-?\d+?\.\d+(e\d+)?"
    FUNCTION_TERMINATOR = r"\)"
    IDENTIFIER = r"[\w:]+"
    INTEGER = r"-?\d+(e\d+)?"
    SHEBANG = r"#!.*\n"
    STRING = r"\"(?:[^\"]*)\""
    UNMAPPED = "."
    WHITESPACE = r"[\s]+"


class Null:

    def __repr__(self):

        return "NULL"


NULL = Null()

type BASECodeValue = int | float | str | Null


class Type(Enum):

    ADD = auto()
    CALL = auto()
    COMMENT = auto()
    DEBUG = auto()
    DELETE = auto()
    DOCSTRING = auto()
    DUMMY = auto()
    ELSE = auto()
    END = auto()
    FLOAT = auto()
    FUNCTION_TERMINATOR = auto()
    FUNCTION = auto()
    IDENTIFIER = auto()
    IF = auto()
    INPUT = auto()
    INT_CAST = auto()
    INTEGER = auto()
    JUMP = auto()
    LINE_TERMINATOR = auto()
    MAIN = auto()
    OUT = auto()
    POP = auto()
    PUSH = auto()
    RAW_SET = auto()
    RAW_STACK_SET = auto()
    REFERENCE = auto()
    REMOVE = auto()
    RETURN = auto()
    SET = auto()
    SHEBANG = auto()
    START = auto()
    STOP = auto()
    STRING = auto()
    UNMAPPED = auto()
    WHITESPACE = auto()


def reference(variable: str):

    return variable + Keyword.REFERENCE_OPERATOR


def sub_directory(directory: str, sub_directory: str):

    # TODO: Add Windows version
    return directory + "/" + sub_directory
