type BASECode = str
type Type = str
type Regex = str
type Keyword = str

class ExecutionModes:

    DEBUG = "DEBUG"
    DOCSTRINGS = "DOCSTRINGS"

class Files:

    STANDARD_LIBRARY_PATH = "lib/"
    UNLINKED_BASECODE_ENDING = ".bc"
    LINKED_BASECODE_ENDING = ".blc"

class Flags:

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

class Keywords:

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
    RETURN = "ret"
    SET = "set"
    START = "start"
    STOP = "stop"

class Regexes:

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

class Types:

    ADD = "ADD"
    CALL = "CALL"
    COMMENT = "COMMENT"
    DEBUG = "DEBUG"
    DELETE = "DELETE"
    DOCSTRING = "DOCSTRING"
    DUMMY = "DUMMY"
    ELSE = "ELSE"
    END = "END"
    FLOAT = "FLOAT"
    FUNCTION_TERMINATOR = "FUNCTION_TERMINATOR"
    FUNCTION = "FUNCTION"
    IDENTIFIER = "IDENTIFIER"
    IF = "IF"
    INPUT = "INPUT"
    INT_CAST = "INT_CAST"
    INTEGER = "INTEGER"
    JUMP = "JUMP"
    LINE_TERMINATOR = "LINE_TERMINATOR"
    MAIN = "MAIN"
    OUT = "OUT"
    POP = "POP"
    PUSH = "PUSH"
    RAW_SET = "RAW_SET"
    RAW_STACK_SET = "RAW_STACK_SET"
    REFERENCE = "REFERENCE"
    SET = "SET"
    SHEBANG = "SHEBANG"
    START = "START"
    STOP = "STOP"
    STRING = "STRING"
    UNMAPPED = "UNMAPPED"
    WHITESPACE = "WHITESPACE"

@staticmethod
def reference(variable: str):

    return variable + Keywords.REFERENCE_OPERATOR
