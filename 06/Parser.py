"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    line-by-line, parses the current command, and provides convenient access
    to the commands components (fields and symbols). Also removes white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it."""
        self.__input_lines = []
        for line in input_file:
            clean_line = line.split("//")[0].strip()
            if clean_line:
                self.__input_lines.append(clean_line)
        self.__lines = len(self.__input_lines)
        self.__current_line = 0

    def has_more_commands(self) -> bool:
        """Checks if there are more commands in the input."""
        return self.__current_line < self.__lines

    def advance(self) -> None:
        """Reads the next command from the input."""
        self.__current_line += 1

    def command_type(self) -> str:
        """Returns the type of the current command."""
        current_line = self.__input_lines[self.__current_line].strip()
        if current_line.startswith("@"):
            return "A_COMMAND"
        elif current_line.startswith("("):
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self) -> str:
        """Returns the symbol or decimal Xxx for A or L commands."""
        current_line = self.__input_lines[self.__current_line].strip()
        if current_line.startswith("@"):
            return current_line[1:] 
        if current_line.startswith("(") and current_line.endswith(")"):
            return current_line[1:-1]
        
    def dest(self) -> typing.Optional[str]:
        """Returns the dest mnemonic for C_COMMAND."""
        current_line = self.__input_lines[self.__current_line].strip()
        if "=" in current_line:
            return current_line.split("=")[0].strip()
        return None

    def comp(self) -> str:
        """Returns the comp mnemonic for C_COMMAND."""
        current_line = self.__input_lines[self.__current_line].strip()
        if "=" in current_line:
            comp_part = current_line.split("=")[1]  # After '='
        else:
            comp_part = current_line
        if ";" in comp_part:
            comp_part = comp_part.split(";")[0]  # Before ';'
        return comp_part.strip()

    def jump(self) -> typing.Optional[str]:
        """Returns the jump mnemonic for C_COMMAND."""
        current_line = self.__input_lines[self.__current_line].strip()
        if ";" in current_line:
            return current_line.split(";")[1].strip()  # After ';'
        return None
    def reset(self) -> None:
        """Resets the parser back to begining"""
        self.__current_line = 0
    def switch_symbol_to_num(self,num:int) -> None:
        """Switches a symbol of A command to a number"""
        current_line = self.__lines[self.__current_line]
        self.__lines[self.__current_line] = "@" + str(num)
