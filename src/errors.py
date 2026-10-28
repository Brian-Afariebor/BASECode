from typing import Any

type ErrorText = str
type HelpText = str


class BASECodeError(RuntimeError):

    NOTE: HelpText

    def __init__(self, *args: Any, **kwargs: Any):

        super().__init__(*args, **kwargs)

        self.add_note(f"\nNote:\n\n{self.NOTE}")


class PositionError(BASECodeError):

    NOTE = """
        Positions must be
            integers
            greater than 0
            and less than the amount of tokens.

        Since there is no safe way to get the amount of tokens at runtime,
            you should only jump and call functions and mains.

        You can create those like this:

            fn FunctionName
            {
                STUFF;
            }

            mn MainName
            {
                STUFF;
            }

        They can be used like this:

            jmp(function::FunctionName);
            jmp(main::MainName)

            call(function::FunctionName);
            call(main::MainName)


        Note that the functions and mains must be defined before usage.

        For example, this code:

            <Main.blc>

            mn Main
            {
                jmp(function::EndCode);
            }

            fn EndCode
            {
                end(0);
            }

        will cause an error; 
            as function::EndCode has not yet been defined by the interrpeter.
        """.strip()


class StackError(BASECodeError):

    NOTE = """
    Stacks have the following layout:
        
        (bottom)
        StackName::0
        StackName::1
        ...
        StackName::n # let n be the greatest index
        (top)

    In addition, this, assuming safe code, is true:

        StackName::tp = n

    You can safely use stacks like this:

        set VariableName = pop(StackName);
        /* Do note that if the stack has no elements, NULL is returned. */

        push(StackName, Value);
        /* This will create a stack if it does not exist. */

        rsks("StackName",Index,Value);
        /* Note that you can make the index a non-int,
            as it is cast to a string by the interpreter.
            However, it is not recommeded unless you know what you are doing. */
    
        set VariableName = rskg("StackName",Index);
        /* Note that here too, the index can be a non-int. */

        clr(StackName);
        rclr("StackName");

    """.strip()


class BASECodeTypeError(BASECodeError):

    NOTE = """
        There are 4 standard BASECode types:
        
            int // An integer; 1,-2,3
            str // A string; "Hello, World!", "\\q"
            float // A decimal number; 3.14, -2.45, 20.23 
            null 
            /* The type for the null object. 
                Commonly used to represent failure of some kind. */
        
        Most functions do specific things when given certain types;
            check the docs for information!

        As for user defined functions, the docstring convention is this:

            /**
            TypeOfFunction FunctionName:

                Description:
                    A description of the function.

                Requirements:
                    Everything required for the function to do its job.
                    All preconditions go here.

                Result:
                    What happens after the function runs.
                    All side effects and postconditions go here.
            */

        You can use the option '-pd' to print all the docstrings.

        You can check the type of an object like this:

            if(sametype(Variable, "") == true)
            {
                STUFF;
            }
            else
            {
                STUFF;
            }
        """


class BASECodeRuntimeError(BASECodeError):

    NOTE = "Check the documentation of implementations for their usage."


class MissingSelfError(BASECodeError):

    NOTE = "Implementations must be called from a valid state."


class MissingArgumentError(BASECodeError):

    NOTE = "Check the standard library for standard library function usage."


class InvalidSetError(MissingArgumentError):

    NOTE = """set is used like this:

        set VARIABLE_NAME = VALUE;
        /*At the filtering stage this becomes set VARIABLE_NAME VALUE;
            so the = is not needed; just good practice.*/
        """.strip()
class InvalidEndError(MissingArgumentError):

    NOTE = """end is used like this:

        end(VALUE);
        /*Due to the filtering process, this can be simplified to 'end VALUE',
        but it's clearer when done this way*/
    """

class MissingTerminatorError(BASECodeError):

    NOTE = "All statements must end in a terminator; the semicolon ';'."
