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

        directory = "/".join(directory_parts[:-1]) + "/"

        buffer = text

        for match in finditer(r"imp\s+(?P<name>\w+)", text):

            replacement_name = match.group("name")

            replacement_text = Linker.link(directory + replacement_name + ".bc")

            replacement_text: BASECode = sub(
                r"(?P<function>mn|fn)\s+(?P<name>\w+)",
                rf"\g<function> {replacement_name}::\g<name>",
                replacement_text,
            )

            buffer: BASECode = sub(
                f"imp\\s+{replacement_name}",
                replacement_text,
                buffer,
            )

        return buffer
