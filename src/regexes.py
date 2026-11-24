from enum import Enum
from enum import unique


@unique
class Keyword(Enum):

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
    MUL = "mul"
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


@unique
class Regex(Enum):

    COMMENT = r"\/\*[\s\S]*\*\/"
    DOCSTRING = r"\/\*\*[\s\S]*?\*\/"
    DUMMY = r"\(|{|}|,|="
    FLOAT = r"-?\d+?\.\d+(e\d+)?"
    FUNCTION_TERMINATOR = r"\)"
    IDENTIFIER = rf"[\w_{repr(Keyword.REFERENCE_OPERATOR.value)[1:-1]}]+"
    INTEGER = r"-?\d[\d_]*(e\d+)?"
    SHEBANG = r"#!.*\n"
    STRING = r"\"(?:[^\"]*)\""
    UNMAPPED = "."
    WHITESPACE = r"[\s]+"


IMPORT_ORDER: list[Keyword | Regex] = [
    Keyword.ADD,
    Keyword.CALL,
    Keyword.DEBUG,
    Keyword.ELSE,
    Keyword.END,
    Keyword.FUNCTION,
    Keyword.IF,
    Keyword.INT_CAST,
    Keyword.INPUT,
    Keyword.JUMP,
    Keyword.LINE_TERMINATOR,
    Keyword.MAIN,
    Keyword.MUL,
    Keyword.OUT,
    Keyword.POP,
    Keyword.PUSH,
    Keyword.RAW_SET,
    Keyword.RAW_STACK_SET,
    Keyword.REFERENCE,
    Keyword.REMOVE,
    Keyword.RETURN,
    Keyword.SET,
    Keyword.START,
    Keyword.STOP,
    Regex.DOCSTRING,
    Regex.COMMENT,
    Regex.DUMMY,
    Regex.FLOAT,
    Regex.FUNCTION_TERMINATOR,
    Regex.INTEGER,
    Regex.IDENTIFIER,
    Regex.SHEBANG,
    Regex.STRING,
    Regex.WHITESPACE,
    Regex.UNMAPPED,
]
