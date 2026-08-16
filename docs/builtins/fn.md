# Set

## Descripion

Defines a function. Does not run it.

## Usage
```fn FUNCTION_NAME FUNCTION_CONTENTS```

## Requirements
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
    
    Requirements:
        None.

    Result:
        The current thread ends with 0.
*/

/**
Function Test::Function:
    
    Description:
        Ends with 0.

    Requirements:
        None.

    Result:
        The current thread ends with 0.
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
        Jumps to function::Test::Function.

    Requirements:
        function::Test::Function is not null.

    Result:
        function::Test::Function is jumped to.
*/
mn Test::Main
{
    jmp(function::Test::Function);
}
```