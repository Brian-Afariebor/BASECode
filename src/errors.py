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
        """


class StackError(BASECodeError):

    NOTE = """
    Stacks have the following layout:
        
        (bottom)
        StackName::0
        StackName::1
        ...
        StackName::n # let n be the greatest index
        (top)

    In addition, this is true:

        StackName::tp = n

    You can use stacks like this:

        set VariableName = pop(StackName);
        /* Do note that if the stack has no elements, NULL is returned. */

        push(StackName, Value);
        /* This will create a stack if it does not exist. */

        rsks("StackName",Index,Value);
        /* This also creates a stack if it does not exist. */
    
        set VariableName = rskg("StackName",Index);
        /* Note that here too, the index can be a non-int. */

        clr(StackName);
        rclr("StackName");

    """


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
        """


class BASECodeRuntimeError(BASECodeError):

    NOTE = "Check the documentation of implementations for their usage."


class MissingSelfError(BASECodeError):

    NOTE = "Implementations must be called from a valid state."


class MissingArgumentError(BASECodeError):

    NOTE = "Check the standard library for standard library function usage."


class EndOfCodeError(BASECodeRuntimeError):

    NOTE = """All programs must end.
    You can do that using the end() method.
    It is used like this:

        end(VALUE):
        /**Ends the current thread with the current value.*/
    """

class InvalidTokenError(BASECodeRuntimeError):

    NOTE = """Check the library for all valid BASECode functions and types."""

class MissingTerminatorError(InvalidTokenError):

    NOTE = """All functions need to be terminated.
    You can do that using ')' and ';'."""

class SuspiciousError(BASECodeRuntimeError):

    NOTE = """Make sure your code is not overwritting
    built-in lanugage variables,
    features,
    or constants"""