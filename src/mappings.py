from filters import register_all as register_all_filters
from implementations import register_all as register_all_implementations
from parser import Parser
from regexes import IMPORT_ORDER as REGEX_IMPORT_ORDER
from token_types import Type


def register_all():

    register_all_filters()
    register_all_implementations()
    register_all_regexes()


def register_all_regexes():

    for regex in REGEX_IMPORT_ORDER:

        name = regex.name

        type: Type = Type._member_map_[name] # pyright: ignore[reportAssignmentType]
        
        Parser.register_regex(type, regex)