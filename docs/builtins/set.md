# Set

## Descripion

Sets a variable to a value.

## Usage
```set VARIABLE_NAME VALUE;```

## Requirements
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
    
    Requirements:
        None.

    Result:
        The current thread ends with 0.
*/

/**
Main Test::Main:

    Description:
        Sets x to 0.

    Requirements:
        None.

    Result:
        X is 0.
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