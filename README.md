# BASECode

An assembly like programming language.

## Origin

When I was younger, I had the idea of making a programming language--a language like assembly, but easier to write---and of course easier to interpret, as I had no idea how a compiler worked. BASECode was the language I chose to make.

## How to Use

BASECode can run code with any extension, but .bc is the prefered extension.

The mini shell environment should help you from there---here are some commands:

add CODE_NAME FILE_PATH: Adds the code at FILE_PATH to the list of code to run. Is saved as CODE_NAME.

add CODE_NAME: Directs the user to get the file CODE_NAME to be turned into code. Code is saved as CODE_NAME.

run CODE_NAME: Runs the code CODE_NAME: Prints any errors it had.

parse CODE_NAME: Returns the tokens the interpeter sees.

format CODE_NAME: Prints the code, but formatted. Does not do indentation.

## Examples
BASECode is a sort of "mashup" of some of my favorite languages.

Here's Hello World:

### Hello World

```
main Main
  out string_start Hello, World string_end
  end NULL
```

### Fibonacci Program

Note: Will run indefinitely.

```
enable IGNORE_EMPTY_LINES
  mn Constants
    set a int 0
    set b int 1
  mn Main
    out a
    out str_s , str_e
    out b
    out str_s \ n str_e
    set a + a b )
    set b a
    jmp main::Main
disable IGNORE_EMPTY_LINES
```