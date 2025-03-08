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
from Parser import Parser
from CodeWriter import CodeWriter


def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO,
        bootstrap: bool) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
        bootstrap (bool): if this is True, the current file is the 
            first file we are translating.
    """
    input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
    parser = Parser(input_file)
    code_writer = CodeWriter(output_file)
    code_writer.set_file_name(input_filename)
    if (bootstrap):
        code_writer.write_Init()
    current_func = ""
    while (parser.has_more_commands()):
        output_file.write("//"+parser.current_line()+"\n")
        cmd_type = parser.command_type()
        if (cmd_type == "C_ARITHMETIC"):
            cmd = parser.arg1()
            code_writer.write_arithmetic(cmd)
        elif (cmd_type == "C_PUSH" or cmd_type == "C_POP"):
            segment = parser.arg1().upper()
            index = parser.arg2()
            code_writer.write_push_pop(cmd_type,segment,index)
        elif (cmd_type == "C_LABEL" or cmd_type == "C_IF" or cmd_type == "C_GOTO"):
            label = parser.arg1()
            if (cmd_type == "C_LABEL"):
                code_writer.write_label(label)
            elif (cmd_type == "C_IF"):
                code_writer.write_if(label)
            elif (cmd_type == "C_GOTO"):
                code_writer.write_goto(label)
        elif (cmd_type == "C_FUNCTION" or cmd_type == "C_CALL"):
            current_func = parser.arg1()
            nargs = parser.arg2()
            if (cmd_type == "C_FUNCTION"):
                code_writer.set_current_func(current_func)
                code_writer.write_function(current_func,nargs)
            else:
                code_writer.write_call(current_func,nargs)
        elif (cmd_type == "C_RETURN"):
            code_writer.write_return()
        parser.advance()


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    bootstrap = True
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file, bootstrap)
            bootstrap = False
