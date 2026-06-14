from parser import BASECode
from parser import BASECodeParser

def main():

    code: BASECode = 'set x 1.; out "Hello, World!";'

    parsed_code = BASECodeParser.parse(code)

    for token in parsed_code:

        print(token)


if __name__ == "__main__":

    main()