# Assembler
Course project - CSCI30000

A simple assembler for SIC/XE. For this version, it can handle following tasks:
basic, functions, literals, program-block, and macro.

# Structure
* `pass1.py` and `pass2.py` contain main code of this assembler.
* All source programs used to test this assembler should be put under the folder
    `Assembler/test/testFiles`
* `lib` folder contains some helper functions and resources like opcode.

# How To Run
Execute the `run.py` file under the Assembler folder, following by the name of
the source code file.

E.x. In terminal, assume current working directory name is Assembler, execute

        python run.py basic.txt

`basic.txt` can be replaced by `literals.txt`, `functions.txt`,
`prog_blocks.txt`, and `functions.txt`

Results will be put into two files: `object_code.txt` and `object_program.txt`
under the same working directory.

