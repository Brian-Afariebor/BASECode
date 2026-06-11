from re import finditer
from re import match
from re import sub

BASECode = str

class DependencyResolver:

    @staticmethod
    def resolve(source: str)->BASECode:

        with open(source, "rt") as source_file:

            text = source_file.read()

        directory_match = match(r"(\/[^\/]+)+(?=\/[^\/]+)", source)

        if directory_match is None:

            raise RuntimeError("Invalid file directory")

        directory = directory_match.string 

        for file_match in finditer(r"(?=imp(\w+))(.+)",text):

            file_name = file_match.string

            with open(directory+file_name+".bc", "rt") as dependency:

                dependency_text = dependency.read()

            text = sub(rf"imp(\w+){file_name}",dependency_text,text)

        return text
        