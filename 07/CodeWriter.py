"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import os


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.__output_stream = output_stream 
        self.__file_name = None
        self.__label_counter = 0

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        outpt_command = "@SP \n A=M-1 \n D=M \n"
        if (command == "add"):
            outpt_command += "A=A-1 \n M = D+M \n @SP \n M=M-1 \n"
        elif (command == "sub"):
            outpt_command += "A=A-1 \n M = M-D \n @SP \n M=M-1 \n"
        elif (command == "neg"):
            outpt_command += "M = -M \n"
        elif (command == "eq"):
            outpt_command += ("A=A-1 \n D=M-D \n M=0 \n @SP \n M=M-1 \n "
            "@EQUAL{} \n D;JEQ \n @END{} \n 0;JMP \n "
            "(EQUAL{}) \n @SP \n A=M-1 \n M=-1 \n (END{}) \n").format(self.__label_counter, self.__label_counter, self.__label_counter, self.__label_counter)
            #fomatting the comparison labels with a counter to make differences
            self.__label_counter += 1
        elif (command == "lt"):
            outpt_command += ("@YNEGATIVE{} \n D;JLT \n @SP \n A=M-1 \n A=A-1 \n D=M \n @XNEGATIVE{} \n D;JLT \n @SAMESIGN{} \n 0;JMP \n"
                               "(YNEGATIVE{}) \n @SP \n A=M-1 \n A=A-1 \n D=M \n @SAMESIGN{} \n D;JLT \n @SP \n AM=M-1 \n A=A-1 \n M=0 \n @END{} \n 0;JMP \n" 
                              "(XNEGATIVE{})\n @SP \n M=M-1 \n @LT{} \n 0;JMP \n"
                              "(SAMESIGN{}) \n @SP \n A=M-1 \n D=M \n A=A-1 \n D=M-D \n M=0 \n @SP \n M=M-1 \n "
            "@LT{} \n D;JLT \n @END{} \n 0;JMP \n "
            "(LT{}) \n @SP \n A=M-1 \n M=-1 \n (END{}) \n").format(self.__label_counter, self.__label_counter, self.__label_counter, self.__label_counter, self.__label_counter,
                                                                   self.__label_counter, self.__label_counter, self.__label_counter, self.__label_counter, self.__label_counter,
                                                                   self.__label_counter, self.__label_counter, self.__label_counter)
            #fomatting the comparison labels with a counter to make differences
            self.__label_counter += 1
        elif (command == "gt"):
            outpt_command += ("@YPOSITIVE{} \n D;JGT \n @SP \n A=M-1 \n A=A-1 \n D=M \n @XPOSITIVE{} \n D;JGT \n @SAMESIGN{} \n 0;JMP \n"
                               "(YPOSITIVE{}) \n @SP \n A=M-1 \n A=A-1 \n D=M \n @SAMESIGN{} \n D;JGT \n @SP\n AM=M-1 \n A=A-1 \n M=0 \n @END{} \n 0;JMP \n" 
                              "(XPOSITIVE{})\n @SP \n M=M-1 \n @GT{} \n 0;JMP \n"
                              "(SAMESIGN{}) \n @SP \n A=M-1 \n D=M \n A=A-1 \n D=M-D \n M=0 \n @SP \n M=M-1 \n "
            "@GT{} \n D;JGT \n @END{} \n 0;JMP \n "
            "(GT{}) \n @SP \n A=M-1 \n M=-1 \n (END{}) \n").format(self.__label_counter, self.__label_counter, self.__label_counter, self.__label_counter, self.__label_counter,
                                                                   self.__label_counter, self.__label_counter, self.__label_counter, self.__label_counter, self.__label_counter,
                                                                   self.__label_counter, self.__label_counter,self.__label_counter)
            #fomatting the comparison labels with a counter to make differences
            self.__label_counter += 1
        elif (command == "and"):
            outpt_command += "A=A-1 \n M = D&M \n @SP \n M=M-1 \n"
        elif (command == "or"):
            outpt_command += "A=A-1 \n M = D|M \n @SP \n M=M-1 \n"
        elif (command == "not"):
            outpt_command += "M = !M \n"
        elif (command == "shiftleft"):
            outpt_command += "M = M<< \n"
        elif (command == "shiftright"):
            outpt_command += "M = M>> \n"
        outpt_command = outpt_command.replace(" ", "")
        self.__output_stream.write(outpt_command)

    

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        memory_seg = {"LOCAL":"LCL", "ARGUMENT":"ARG","THIS":"THIS","THAT":"THAT"}
        pointer_dict = {"0":"THIS", "1":"THAT"}
        index = str(index)
        outpt_cmd = ""
        if (command == "C_PUSH"):
            if (segment in memory_seg):
                seg = memory_seg[segment]
                outpt_cmd += "@" + index + "\n D=A \n @" + seg + "\n A=D+M \n D=M \n"
            elif (segment == "CONSTANT"):
                outpt_cmd += "@" + index + "\n D=A \n"
            elif (segment == "TEMP"):
                index = int(index)
                index += 5
                index = str(index)
                outpt_cmd += "@" + index + "\n D=M \n"
            elif (segment == "POINTER"):
                seg = pointer_dict[index]
                outpt_cmd += "@" + seg + "\n D=M \n"
            else: #Static
                outpt_cmd += "@" + self.__file_name +"." + index +"\n D=M \n " 
            outpt_cmd += "@SP \n A=M \n M=D \n @SP \n M=M+1 \n"
        else: #POP
            outpt_cmd = "@SP \n AM = M-1 \n D=M \n"
            if (segment in memory_seg):
                seg = memory_seg[segment]
                outpt_cmd += "@R13 \n M=D \n @" + index + "\n D=A \n @" + seg + "\n D=D+M \n @R14 \n M=D \n @R13 \n D=M \n @R14 \n A=M \n M=D \n"
            elif (segment == "TEMP"):
                index = int(index)
                index += 5 #Temp starts from 5
                index = str(index)
                outpt_cmd += "@" + index + "\n M=D \n"
            elif (segment == "POINTER"):
                seg = pointer_dict[index]
                outpt_cmd += "@" + seg + "\n M=D \n"
            else: #Static
                outpt_cmd += "@" + self.__file_name +"." + index +"\n M=D \n" 
        outpt_cmd = outpt_cmd.replace(" ", "")
        self.__output_stream.write(outpt_cmd)



    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        formatted_label = f"{self.__current_func}${label}"
        self.__output_stream.write(f"({formatted_label})\n")
    
    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        formatted_label = f"{self.__current_func}${label}"
        self.__output_stream.write(f"@{formatted_label}\n0;JMP\n")
    
    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        formatted_label = f"{self.__current_func}${label}"
        output_cmd = "@SP\nAM=M-1\nD=M\n@" + formatted_label + "\nD;JNE\n" #0=False
        self.__output_stream.write(output_cmd)
        
    
    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass
    
    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass
    
    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass
