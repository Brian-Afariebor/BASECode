class Constants:

    class ExecutionModes:

        DOCSTRINGS = "-d"

    class Flags:

        DOCSTRING = "-d"
        FILE = "-f"
        HELP = "-h" 
        NAME = "-n"

    class Keywords:

        ADD = "add"
        DELETE = "del"
        ELSE = "else"
        END = "end"
        FUNCTION = "fn"
        FUNCTION_NAME = "function"
        IF = "if"
        JUMP = "jmp"
        LINE_TERMINATOR = ";"
        MAIN = "mn"
        MAIN_NAME = "main"
        OUT = "out"
        RAW_SET = "rset"
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


    class Types:

        ADD = "add"
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
        INTEGER = "INTEGER"
        JUMP = "JUMP"
        LINE_TERMINATOR = "LINE_TERMINATOR"
        MAIN = "MAIN"
        OUT = "OUT"
        RAW_SET = "RAW_SET"
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
