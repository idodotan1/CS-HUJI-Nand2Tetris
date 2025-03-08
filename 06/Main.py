"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    parser = Parser(input_file)
    sym_table = SymbolTable()
    i = 0
    while(parser.has_more_commands()):
        cmd_type = parser.command_type()
        if (cmd_type=="L_COMMAND"):
            sym = parser.symbol()
            sym_table.add_entry(sym,i)
        else:
            i += 1
        parser.advance()
    parser.reset()
    n = 16
    while(parser.has_more_commands()):
        cmd_type = parser.command_type()
        if cmd_type == "C_COMMAND":
            des = parser.dest()
            com = parser.comp()
            jmp = parser.jump()
            line = Code.comp(com) + Code.dest(des) + Code.jump(jmp) +'\n'
            output_file.write(line)
        elif cmd_type == "A_COMMAND":
            sym = parser.symbol()
            if (not sym.isdigit()):
                if (not sym_table.contains(sym)):
                    sym_table.add_entry(sym,n)
                    n += 1
                add = sym_table.get_address(sym)
            else:
                add = int(parser.symbol())
            line = format(add,'016b') + '\n'
            output_file.write(line)
        parser.advance()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
