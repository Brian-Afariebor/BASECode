from implementations import end
from interpreter import Interpreter
from parser import Parser
from regexes import Regex
from token_types import Type


def register_all():

    register_end()
    register_unmapped()

def register_end():

    Interpreter.register(end, Type.END)
    Parser.register_regex(Type.END, Regex.END)

def register_unmapped():

    Parser.register_regex(Type.UNMAPPED, Regex.UNMAPPED)