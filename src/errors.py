type ErrorText = str
type HelpText = str

class BASECodeError(RuntimeError):

    NOTE: HelpText

    def __post__init__(self):

        self.add_note(f"Note:\n\n{self.NOTE}")
    
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