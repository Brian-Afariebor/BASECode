# BASECode

An assembly like programming language.

## Origin

When I was younger, I had the idea of making a programming language--a language like assembly, but easier to write, and a bit higher-level. 

## Examples

Here are some examples of BASECode:

### Hello World
```
mn Main

  out "Hello, World!";

  end 0;
```

### 99 Bottles of Beer
```
mn Constants

  set Start 99;

fn Loop

  if Start 0

    jmp function::End;

  else

    out Start;
    out " bottles of beer on the wall,\n";
    out Start;
    out " bottles of beer.\n";
    out "Take one down, and pass it around,\n";
    set Start - Start 1);
    out Start;
    out " bottles of beer.";

fn End
  
  out "No more bottles of beer on the wall,\n";
  out "No more bottles of beer.\n";
  out "Go to the store, and buy some more,\n";
  out "99 bottles of beer...";

  ret 0;

mn Main

  call function::Loop;

  end 0;

```