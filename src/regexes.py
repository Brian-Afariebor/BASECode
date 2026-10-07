from enum import Enum


# Yes, we will have to explicitly write out keywords,
# but that doesn't really matter
class Regex(Enum):

    END = "end"
    UNMAPPED = "."