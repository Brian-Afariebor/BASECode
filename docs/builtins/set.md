# Set

## Descripion

Sets a variable to a value.

## Usage
```set VARIABLE_NAME VALUE;```

## Preconditions
None.

## Result
When ```set VARIABLE_NAME VALUE;``` is run,
```VARIABLE_NAME``` is set to ```VALUE```.

## Example
```
/**
Test Test:

    Description:
        Demonstrates the "set" keyword.
    
    Preconditions:
        None.

    Result:
        Ends with 0.

    Postconditions:
        The current thread is ended.
*/

/**
Main Test::Main:

    Description:
        Sets x to 0.

    Preconditions:
        None.

    Result:
        X is 0.

    Postconditions:
        The code is ended.
*/
mn Test::Main
{
    // Note: The equals sign (=) is not required;
    // it's just there for readability.
    // It gets removed before code execution.
    set x = 0;
    end(x);
}
```