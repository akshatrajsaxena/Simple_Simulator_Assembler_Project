A simple Python assembler
This is a simple Python assembler that can be used to assemble simple assembly instructions into binary machine code.

Usage
To use the assembler, simply pass the assembly code as a string to the assemble() function. The function will return a list of binary machine code instructions.

## Supported instructions

The following instructions are currently supported:

* add
* sub
* mul
* xor
* or
* and
* mov
* rs
* ls
* div
* not
* cmp
* ld
* st
* jmp
* jlt
* jgt
* je
* hlt

The input assembly code should follow a specific format:

Each instruction should be on a new line.
Instructions can include operations like add, sub, mul, xor, or, and, mov, rs, ls, div, not, cmp, ld, st, jmp, jlt, jgt, je, or hlt.
Variables should be declared using the var keyword followed by a variable name.
Labels should end with a colon (:) and must not conflict with variable names.
Registers should be represented as R0, R1, R2, R3, R4, R5, R6, or FLAGS.
Immediate values should be represented as $ followed by the decimal value.
Comments can be added using the # symbol.

##Error Handling
The program performs basic error checking to ensure the correctness of the input code. If any errors are encountered during the conversion process, an error message will be displayed on the console, indicating the type of error.

## Limitations

The following limitations apply to the current version of the assembler:

* Only simple assembly instructions are supported.
* Only 8-bit registers are supported.
* Only immediate values of up to 127 are supported.
* Only labels at the beginning of a line are supported.

## Future plans

The following features are planned for future versions of the assembler:

* Support for more complex assembly instructions.
* Support for 16-bit registers.
* Support for immediate values of up to 255.
* Support for labels anywhere in a line.
