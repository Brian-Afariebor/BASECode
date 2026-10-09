from enum import Enum


# Yes, we will have to explicitly write out keywords,
# but that doesn't really matter
class Regex(Enum):

    # SECTION - Keywords
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
    # !SECTION

    # SECTION - Regexes
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
    # !SECTION