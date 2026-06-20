from parser import BASECode
from parser import Parser

def main():

    code: BASECode = 'out main::x;'

    parsed_code = Parser.parse(code)

    for token in parsed_code:

        print(token)


if __name__ == "__main__":

    main()