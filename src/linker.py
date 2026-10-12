from re import finditer
from re import sub

from regexes import Keyword

STANDARD_LIBRARY_PATH = "lib"
UNLINKED_BASECODE_ENDING = ".bc"
LINKED_BASECODE_ENDING = ".blc"


# TODO - Add windows version
BASECODE_DIRECTORY = "/".join(__file__.split("/")[:-2])

type FilePath = str


class BASECodeCode(str): ...


class LinkedCode(BASECodeCode): ...


def link(source_path: FilePath) -> LinkedCode:

    text = get_code_from_file(source_path)

    # TODO - Add windows version
    directory_parts = source_path.split("/")

    # TODO - Add windows version
    current_directory = "/".join(directory_parts[:-1])

    buffer = text

    for match in finditer(
        rf"{Keyword.IMPORT}\s+\"(?P<name>[^\"]+)\"",
        text,
    ):

        replacement_path = match.group("name")

        replacement_text = link(
            sub_directory(current_directory, replacement_path),
        )

        buffer = remove_file_imports(buffer, replacement_path, replacement_text)

    for match in finditer(rf"{Keyword.IMPORT}\s+<(?P<name>[^>]+)>", text):

        library_file_name = match.group("name")

        replacement_text = link(get_library_path(library_file_name))

        buffer = replace_library_imports(
            buffer,
            replacement_text,
            library_file_name,
        )

    return LinkedCode(buffer)


def remove_file_imports(
    buffer: BASECodeCode,
    replacement_path: FilePath,
    replacement_text: LinkedCode,
):
    
    return BASECodeCode(
        sub(
            f"imp\\s+<{replacement_path}>",
            replacement_text,
            buffer,
        )
    )


def replace_library_imports(
    buffer: BASECodeCode,
    replacement_text: LinkedCode,
    library_file_name: str,
):

    return BASECodeCode(
        sub(
            f"imp\\s+<{library_file_name}>",
            replacement_text,
            buffer,
        )
    )


def get_library_path(library_file_name: str):
    return (
        sub_directory(
            sub_directory(
                BASECODE_DIRECTORY,
                STANDARD_LIBRARY_PATH,
            ),
            library_file_name,
        )
        + ".bc"
    )


def get_code_from_file(source_path: FilePath):

    try:

        with open(source_path, "rt") as source_file:

            text = BASECodeCode(source_file.read())

    except FileNotFoundError:

        raise FileNotFoundError(f"Missing file {source_path}")

    return text


def sub_directory(directory: FilePath, sub_directory: FilePath):

    # TODO: Add Windows version
    return directory + "/" + sub_directory
