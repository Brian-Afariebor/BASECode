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

            raise FileNotFoundError(f"Missing file '{source_path}'.") from None

        directory_parts = source_path.split("/")

        current_directory = "/".join(directory_parts[:-1]) + "/"

        buffer = text

        for match in finditer(r"imp\s+\"(?P<name>[\w\W]+)\"", text):

            replacement_path = match.group("name")

            replacement_text = Linker.link(current_directory + replacement_path)

            buffer: BASECode = sub(
                f'imp\\s+"{replacement_path}"',
                replacement_text,
                buffer,
            )

        return buffer
