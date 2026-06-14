from re import finditer
from re import sub

type BASECode = str


class DependencyResolver:

    @staticmethod
    def resolve(source_directory: str) -> BASECode:

        with open(source_directory, "rt") as source_file:

            text = source_file.read()

        directory_parts = source_directory.split("/")

        directory = "/" + "/".join(directory_parts[:-1]) + "/"

        buffer = text

        for match in finditer(r"imp\s+(?P<name>\w+)", text):

            replacement_name = match.group("name")

            with open(directory + replacement_name + ".bc") as replacement_file:

                replacement_text = replacement_file.read()

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
