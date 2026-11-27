from enum import auto
from enum import Enum


class Mode(Enum):
    """A mode of code execution.
    Can be NORMAL,
    NO_TRUST,
    DEBUG,
    or DOCSTRINGS.
    """

    NORMAL = auto()
    """Normal execution of a BASECode program.
    """

    WARNING_ERRORS = auto()
    """Turns all warnings into errors.
    Every action is written to the debug file.
    """

    DEBUG = auto()
    """The debug mode of a BASECode program.
    Warnings are raised,
    and every action is written to the debug file.
    """

    DOCSTRINGS = auto()
    """Prints all of the docstrings.
    """