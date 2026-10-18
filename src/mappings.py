from filters import register_all as register_all_filters
from implementations import register_all as register_all_implementations

from parser import Parser

from regexes import Regex
from regexes import Keyword

from token_types import Type


def register_all():

    register_all_filters()
    register_all_implementations()

def register_regexes():

    Parser.register_regex(Type.END, Keyword.END)
    Parser.register_regex(Type.UNMAPPED, Regex.UNMAPPED)
    Parser.register_regex(Type.INTEGER, Regex.INTEGER)
