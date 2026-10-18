from filters import register_all as register_all_filters
from implementations import register_all as register_all_implementations

from parser import Parser

from regexes import Regex
from regexes import Keyword

from token_types import Type


def register_all():

    register_all_filters()
    register_all_implementations()
    register_all_regexes()

def register_all_regexes():

    register_keywords()
    register_non_unmapped_regexes()
    register_unmapped_regex()

def register_unmapped_regex():
    Parser.register_regex(Type.UNMAPPED, Regex.UNMAPPED)

def register_non_unmapped_regexes():
    Parser.register_regex(Type.INTEGER, Regex.INTEGER)

def register_keywords():
    Parser.register_regex(Type.END, Keyword.END)
