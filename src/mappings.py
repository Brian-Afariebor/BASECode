# NOTE - Using a wildcard import here will help with registry;
# we use almost all of the methods in implementations anyway
from implementations import *

from interpreter import Interpreter
from parser import Parser

from regexes import Regex
from regexes import Keyword

from token_types import Type


def register_all():

    # NOTE - These have to go in a specific order to not cause problems
    register_end()
    register_integer()
    register_unmapped()


def register_end():

    Interpreter.register(end, Type.END)
    Parser.register_regex(Type.END, Keyword.END)


def register_unmapped():

    Parser.register_regex(Type.UNMAPPED, Regex.UNMAPPED)


def register_integer():

    Parser.register_regex(Type.INTEGER, Regex.INTEGER)
    Interpreter.register(integer, Type.INTEGER)
