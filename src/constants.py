class Constants:

    class ExecutionModes:

        DOCSTRINGS = "-d"

    class Flags:

        FILE = "-f"
        HELP = "-h"
        NAME = "-n"
        NO_LINK = "-nl"
        NO_PARSE = "-np"
        PRINT_DOCSTRINGS = "-pd"
        SAVE_LINK = "-sl"
        SAVE_PARSE = "-sp"
        SAVE_TRIMMINGS = "-st"

    class Keywords:

        ADD = "add"
        CALL = "call"
        DELETE = "del"
        ELSE = "else"
        END = "end"
        FUNCTION = "fn"
        FUNCTION_NAME = "function"
        IF = "if"
        INPUT = "in"
        INT_CAST = "int"
        JUMP = "jmp"
        LINE_TERMINATOR = ";"
        MAIN = "mn"
        MAIN_NAME = "main"
        OUT = "out"
        RAW_SET = "rset"
        REFERENCE = "ref"
        REFERENCE_OPERATOR = "::"
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

    class Types:

        ADD = "ADD"
        CALL = "CALL"
        COMMENT = "COMMENT"
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
        RAW_SET = "RAW_SET"
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

        return variable + Constants.Keywords.REFERENCE_OPERATOR
