# BASECode
A low level programming language intending to make low-level programming easier.

## Index

1. [Introduction](#Introduction)
2. [Notes](#Notes)
3. [Installation](#Installation)
4. [Usage](#Usage)
5. [Examples](#Examples)

## Introduction

BASECode is a buffer language; it makes transitioning to a lower-level language easier.

To demonstrate this, take pointers. While pointers are the address of a variable, in BASECode they are represented as the name of the variable itself. Here's an example:
```
set Constants::A = 1;
// In BASECode, ref() is the reference function.
// As a result, Constants::B is set to 1.
set Constants::B = ref("Constants::A");
```
BASECode makes low-level concepts easier to understand while also providing the tools to abstract further if needed.

## Installation

## Usage
The interpreter can be found in [src/interpreter.py](https://github.com/Brian-Afariebor/BASECode/main/src/interpreter.py) and can be run like so:
```
python interpreter.py FILE_ARGS
```
Command line arguments can be found in [docs/terminal.md](https://github.com/Brian-Afariebor/BASECode/main/docs/terminal.md)

## Examples

Examples can be found in [samples](https://github.com/Brian-Afariebor/BASECode/main/samples).
