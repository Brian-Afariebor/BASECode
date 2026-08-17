from constants import Keywords
from constants import Files

from re import finditer
from re import sub

type BASECode = str


class Linker:

    @staticmethod
    def link(source_path: str) -> BASECode:

        try:

            with open(source_path, "rt") as source_file:

                text = source_file.read()

        except FileNotFoundError:

            raise FileNotFoundError(f"Missing file {source_path}") from None

        directory_parts = source_path.split("/")

        current_directory = "/".join(directory_parts[:-1]) + "/"

        buffer = text

        for match in finditer(
            rf"{Keywords.IMPORT}\s+\"(?P<name>[^\"]+)\"", text
        ):

            replacement_path = match.group("name")

            replacement_text = Linker.link(
                current_directory + replacement_path,
            )

            buffer: BASECode = sub(
                f'imp\\s+"{replacement_path}"',
                replacement_text,
                buffer,
            )

        for match in finditer(
            rf"{Keywords.IMPORT}\s+<(?P<name>[^>]+)>", text
        ):

            library_file_name = match.group("name")

            BASECode_directory = "/".join(__file__.split("/")[:-2]) + "/"

            replacement_text = Linker.link(
                BASECode_directory
                + Files.STANDARD_LIBRARY_PATH
                + library_file_name
                + ".bc"
            )

            buffer: BASECode = sub(
                f"imp\\s+<{library_file_name}>",
                replacement_text,
                buffer,
            )

        return buffer
