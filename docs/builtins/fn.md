# Set

## Descripion

Defines a function. Does not run it.

## Usage
```fn FUNCTION_NAME FUNCTION_CONTENTS```

## Preconditions
None.

## Result
When ```fn FUNCTION_NAME FUNCTION_CONTENTS``` is run,
```function::FUNCTION_NAME``` is set to the adress of ```FUNCTION_CONTENTS```.

## Example
```
/**
Test Test:

    Description:
        Demonstrates the "fn" keyword.
    
    Preconditions:
        None.

    Result:
        Ends with 0.

    Postconditions:
        The current thread is ended.
*/

/**
Function Test::Function:
    
    Description:
        Ends with 0.

    Preconditions:
        None.

    Result:
        The code is ended.

    Postconditions:
        The current thread is ended.
*/
fn Test::Function
// Note: The brackets are not required;
// they only help readability.
{
    // Note: Indentation is not required here;
    // it only helps readability.
    end(0);
}

/**
Main Test::Main:

    Description:
        Jumps to function::Test::Function

    Preconditions:
        None.

    Result:
        The code is ended.

    Postconditions:
        The current thead is ended.
*/
mn Test::Main
{
    jmp(function::Test::Function);
}
```