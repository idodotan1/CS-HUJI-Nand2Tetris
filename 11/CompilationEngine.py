"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.__tokenizer = input_stream
        self.__VMWriter= VMWriter(output_stream)
        self.__symbol_table = SymbolTable()
        self.__num_of_expressions = 0 #Will be used later to count number of expressions in compile expression list
        self.__class_name = ""
        self.__label_counter = 0 #Used in order to make unique labels
        self.__local_vars = 0 #Counts how many local variables a function uses
        self.__method_caller_type = "" #Used in order to push the this argument

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.__tokenizer.advance() #Class
        self.__class_name = self.__tokenizer.identifier()
        self.__tokenizer.advance()
        self.__tokenizer.advance() #Now after {
        current_token = self.__tokenizer.keyword()
        while (current_token != "}"):
            if (current_token == "static" or current_token == "field"):
                self.compile_class_var_dec()
            elif (current_token == "constructor" or current_token == "method" or current_token == "function"):
                self.compile_subroutine()
            self.__tokenizer.advance()
            current_token = self.__tokenizer.keyword()

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        current_token = self.__tokenizer.keyword()
        kind = current_token
        self.__tokenizer.advance()
        if self.__tokenizer.token_type() == "keyword": #A built in type
            type = self.__tokenizer.keyword()
        elif self.__tokenizer.token_type() == "identifier": #A program class type
            type = self.__tokenizer.identifier()
        while True:
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "identifier":
                name = self.__tokenizer.identifier()
                self.__symbol_table.define(name,type,kind)
            self.__tokenizer.advance()
            if self.__tokenizer.symbol() == ",": #If its a multiple variable decleration
                pass
            elif self.__tokenizer.symbol() == ";":
                return


    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        function_name = self.__class_name
        self.__symbol_table.start_subroutine()
        current_token = self.__tokenizer.keyword() #Fucntion, method or constructor
        is_constructor = False
        is_method = False
        if (current_token == "method"):
            is_method = True
        if (current_token == "constructor"):
            is_constructor = True
        self.__tokenizer.advance() #Type of return
        self.__tokenizer.advance() #Name of function
        function_name += "." + self.__tokenizer.identifier()
        self.__tokenizer.advance() #Entering parameter list
        if (is_method): #We want to define this as argument 0
            self.__symbol_table.define("this",self.__method_caller_type,"argument")
        self.compile_parameter_list()
        self.__tokenizer.advance() #Entering the subroutine
        self.__local_vars = 0
        while True:
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "keyword":
                if self.__tokenizer.keyword() == "var":
                    self.compile_var_dec()
                else:
                    break
            else:
                break
        self.__VMWriter.write_function(function_name,self.__local_vars)
        if (is_constructor):
            num_of_vars = self.__symbol_table.var_count("field") #We allocate memory according to the class fields
            self.__VMWriter.write_push("constant",num_of_vars)
            self.__VMWriter.write_call("Memory.alloc",1)
            self.__VMWriter.write_pop("pointer",0)
        elif(is_method): #Setting the this segment
            self.__VMWriter.write_push("argument",0)
            self.__VMWriter.write_pop("pointer",0)
        self.compile_statements()

    def compile_parameter_list(self) -> int:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        num_of_expressions = 0
        kind = "argument" #Parameters are arguments
        is_var_name = False #Used to distinguish between class names and var names
        while True:
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "identifier":
                if (not is_var_name): #So its a class name
                    type = self.__tokenizer.identifier()
                    is_var_name = True #Meaning the next word is the var name
                else: #So its a var name
                    name = self.__tokenizer.identifier()
                    is_var_name = False 
                    self.__symbol_table.define(name,type,kind)
                    num_of_expressions += 1
            elif self.__tokenizer.token_type() == "keyword": #A built in type of var
                type = self.__tokenizer.keyword()
                is_var_name = True #Next will come the var name
            elif self.__tokenizer.symbol() == ",":
                pass
            elif self.__tokenizer.symbol() == ")":
                return num_of_expressions

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.__tokenizer.advance()
        kind = "var" #All vars declared here are local
        if self.__tokenizer.token_type() == "identifier": #This means the type is a program class
            type = self.__tokenizer.identifier()
        elif self.__tokenizer.token_type() == "keyword": #This means the type is a built in type
            type = self.__tokenizer.keyword()
        while True:
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "identifier":
                name = self.__tokenizer.identifier()
                self.__symbol_table.define(name,type,kind)
                self.__local_vars += 1
            self.__tokenizer.advance()
            if self.__tokenizer.symbol() == ",":
                pass
            elif self.__tokenizer.symbol() == ";":
                return


    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        while True:
            if_statement = False #If its an "if" statement we dont need to advance the tokenizer after the statement
            if (self.__tokenizer.token_type() == "keyword"):
                current_statement = self.__tokenizer.keyword()
                if current_statement == "var":
                    self.compile_var_dec()
                elif current_statement == "let":
                    self.compile_let()
                elif current_statement == "if":
                    self.compile_if()
                    if_statement = True
                elif current_statement == "while":
                    self.compile_while()
                elif current_statement == "":
                    self.compile_do()
                elif current_statement == "return":
                    self.compile_return()
                elif current_statement in {"function, method, constructor"}:
                    self.compile_subroutine()
                elif current_statement == "class":
                    self.compile_class()
                elif current_statement == "do":
                    self.compile_do()
            elif self.__tokenizer.token_type() == "symbol":
                return
            if (not if_statement):
                self.__tokenizer.advance()



    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        function_name = ""
        self.__tokenizer.advance()
        is_inner_method = False #A flag to understand if its a method call from inside the class
        is_method = False
        if self.__tokenizer.token_type() == "identifier":
            var_name = self.__tokenizer.identifier()
            if (self.__symbol_table.type_of(var_name)): #If its a var name we need to know its type in order to call the method
                class_name = self.__symbol_table.type_of(var_name)
                function_name += class_name
            else: #If its not a var name its either an inner class method or an OS method
                is_inner_method = True
                function_name += var_name
        self.__tokenizer.advance()
        if self.__tokenizer.symbol() == ".":
            is_inner_method = False #If there is a dot that means its not a method from the current class
            if (self.__symbol_table.kind_of(var_name)): #If its a variable name its a program class method, otherwise its an OS class
                is_method = True
            function_name += "."
            self.__tokenizer.advance()
            function_name += self.__tokenizer.identifier() #The subroutine name
            self.__tokenizer.advance()
            if (is_method): #If its a method we push the var that called the method
                self.__VMWriter.write_push(self.__symbol_table.kind_of(var_name),self.__symbol_table.index_of(var_name))
        self.__tokenizer.advance()
        if (is_inner_method): #If its a call to a method from inside the class we need to add the class name to the function
            function_name = self.__class_name + "." + function_name
            self.__VMWriter.write_push("pointer",0)
        num_of_expressions= self.compile_expression_list()
        if (is_method or is_inner_method):
            num_of_expressions += 1
            if (is_method): #If we called a the type of this would be the type of the caller
                self.__method_caller_type = self.__symbol_table.type_of(var_name)
            else: #If its an inner method than the type of this will be the current class
                self.__method_caller_type = self.__class_name
        self.__tokenizer.advance()
        self.__VMWriter.write_call(function_name,num_of_expressions)
        self.__VMWriter.write_pop("temp",0)
        
    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        is_array = False
        self.__tokenizer.advance()
        var_name = self.__tokenizer.identifier()
        self.__tokenizer.advance()
        if self.__tokenizer.symbol() == "[": #We need to deal with an array
            is_array = True
            self.__VMWriter.write_push(self.__symbol_table.kind_of(var_name),self.__symbol_table.index_of(var_name))
            #We push the array start address        
            self.__tokenizer.advance()
            self.compile_expression() #We compile the expression inside the brackets
            self.__VMWriter.write_arithmetic("add") #We add the base address and the compiled expression
            self.__tokenizer.advance()
        self.__tokenizer.advance() #Now after the = sign
        self.compile_expression()
        if (is_array):
            self.__VMWriter.write_pop("temp",0)
            self.__VMWriter.write_pop("pointer",1)
            self.__VMWriter.write_push("temp",0)
            self.__VMWriter.write_pop("that",0)
        else:
            self.__VMWriter.write_pop(self.__symbol_table.kind_of(var_name),self.__symbol_table.index_of(var_name))
        

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.__label_counter += 1 #For each while or if statement we want a unique label index
        current_label = str(self.__label_counter) 
        self.__VMWriter.write_label("L1$" + current_label)
        self.__tokenizer.advance()
        self.__tokenizer.advance()
        self.compile_expression() #The expression inside the ()
        self.__VMWriter.write_arithmetic("not")
        self.__VMWriter.write_if("L2$" + current_label)
        self.__tokenizer.advance()
        self.__tokenizer.advance()
        self.compile_statements() #Now inside the {}
        self.__VMWriter.write_goto("L1$" + current_label)
        self.__VMWriter.write_label("L2$" + current_label)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.__tokenizer.advance()
        is_void = True
        if self.__tokenizer.token_type() != "symbol" or self.__tokenizer.symbol() != ";":
            self.compile_expression()
            is_void = False #If its not just return; that meant the function returns something
        if (is_void): #We always have to return something
            self.__VMWriter.write_push("constant",0)
        self.__VMWriter.write_return()

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.__label_counter += 1 #For each while or if statement we want a unique label index
        current_label = str(self.__label_counter)
        self.__tokenizer.advance()
        self.__tokenizer.advance()
        self.compile_expression() #The expression inside the ()
        has_else = False #If there is no else we dont need to generate labels for it
        self.__VMWriter.write_arithmetic("not")
        self.__VMWriter.write_if("L1$" + current_label)
        while(self.__tokenizer.symbol() != "{"):
            self.__tokenizer.advance()
        self.__tokenizer.advance()
        self.compile_statements() #Inside the {}
        self.__tokenizer.advance()
        if self.__tokenizer.token_type() == "keyword" and self.__tokenizer.keyword() == "else":
            has_else = True
            self.__VMWriter.write_goto("L2$" + current_label)
            self.__tokenizer.advance()
            self.__VMWriter.write_label("L1$" + current_label)
            self.__tokenizer.advance()
            self.compile_statements() #Inside the {}
            self.__tokenizer.advance()
        if (has_else):
            self.__VMWriter.write_label("L2$" + current_label)
        else:
            self.__VMWriter.write_label("L1$" + current_label)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        operators = {'+',"-",'*','/','&amp;','|','&lt;','&gt;', '='}
        self.compile_term()
        while (self.__tokenizer.token_type() == "symbol" and self.__tokenizer.symbol() in operators): 
            #For expressions that include multiple operations
            op = self.__tokenizer.symbol()
            self.__tokenizer.advance()
            self.compile_term()
            if op == "+":
                self.__VMWriter.write_arithmetic("add")
            elif op == "-":
                self.__VMWriter.write_arithmetic("sub")
            elif op == "*":
                self.__VMWriter.write_call("Math.multiply",2)
            elif op == "/":
                self.__VMWriter.write_call("Math.divide",2)
            elif op == "&amp;":
                self.__VMWriter.write_arithmetic("and")
            elif op == "|":
                self.__VMWriter.write_arithmetic("or")
            elif op == "&lt;":
                self.__VMWriter.write_arithmetic("lt")
            elif op == "&gt;":
                self.__VMWriter.write_arithmetic("gt")
            else: #Only "=" left
                self.__VMWriter.write_arithmetic("eq")

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
        """
        look_ahead = True #A flag we will use in order to decide if we need to advance the tokenizer
        type = self.__tokenizer.token_type()
        if type in {"string_const", "int_const", "keyword"}: #Just a value
            if type == "string_const": #We use the built in String constructor
                word = self.__tokenizer.string_val()
                length = len(word)
                self.__VMWriter.write_push("constant",length)
                self.__VMWriter.write_call("String.new",1)
                for char in word:
                    self.__VMWriter.write_push("constant",ord(char))
                    self.__VMWriter.write_call("String.appendChar",2)
            if type == "int_const":
                self.__VMWriter.write_push("constant",self.__tokenizer.int_val())
            else: #Its a keyword
                keyword = self.__tokenizer.keyword()
                if (keyword == "true"):
                    self.__VMWriter.write_push("constant",1)
                    self.__VMWriter.write_arithmetic("neg")
                elif keyword == "false":
                    self.__VMWriter.write_push("constant",0)
                elif keyword == "this":
                    self.__VMWriter.write_push("pointer",0)
                elif keyword == "null":
                    self.__VMWriter.write_push("constant",0)
        elif type == "identifier": #Meaning its a variable, class or method
             var_name = self.__tokenizer.identifier()
             segment = self.__symbol_table.kind_of(var_name)
             index = self.__symbol_table.index_of(var_name)
             if (segment): #If its a variable we push it into the stack
                self.__VMWriter.write_push(segment,index)
             self.__tokenizer.advance()
             look_ahead = False
             if self.__tokenizer.token_type() == "symbol":
                if self.__tokenizer.symbol() == "[": #So its a variable access term
                    self.__tokenizer.advance() #We already pushed the array base address
                    self.compile_expression()
                    self.__VMWriter.write_arithmetic("add")
                    self.__VMWriter.write_pop("pointer",1)
                    self.__VMWriter.write_push("that",0)
                    look_ahead = True
                elif self.__tokenizer.symbol() == "(": #This means we called an inner class method
                    self.__tokenizer.advance()
                    self.__VMWriter.write_push("pointer",0) #So we push this to the stack
                    self.__method_caller_type = self.__class_name #The this type is the current class
                    num_of_expressions = self.compile_expression_list()
                    self.__tokenizer.advance()
                    function_name = self.__class_name + "." + var_name
                    self.__VMWriter.write_call(function_name,num_of_expressions +1) #We add 1 for this
                    look_ahead = False
                elif self.__tokenizer.symbol() == ".": #This means we need to call a method
                    self.__tokenizer.advance()
                    method_name = self.__tokenizer.identifier()
                    if (self.__symbol_table.type_of(var_name)): #If its a var and not an OS class
                        function_name = self.__symbol_table.type_of(var_name)+ "." + method_name
                    else:
                        function_name = var_name + "." + method_name #The var name is an OS or outer class
                    self.__tokenizer.advance()
                    self.__tokenizer.advance()
                    is_method = False
                    if (self.__symbol_table.kind_of(var_name)): #If it's a var that means its not an OS class method
                        is_method = True
                        # self.__VMWriter.write_push(self.__symbol_table.kind_of(var_name),self.__symbol_table.index_of(var_name))
                        self.__method_caller_type = self.__symbol_table.type_of(var_name)
                        #We pushed the object that called the method and saved its type
                    num_of_expressions = self.compile_expression_list()
                    if (is_method):
                        num_of_expressions += 1 #For the object we pushed
                    self.__VMWriter.write_call(function_name,num_of_expressions)
                    look_ahead = True
        elif type == "symbol":
            symbol = self.__tokenizer.symbol()
            if symbol == "(":
                self.__tokenizer.advance()
                self.compile_expression()
            elif symbol in {"-","~","^","#"}: #Unary operation
                self.__tokenizer.advance()
                self.compile_term() #We first push whats after the operator and then operate on it
                if symbol == "-":
                    self.__VMWriter.write_arithmetic("neg")
                elif symbol == "~":
                    self.__VMWriter.write_arithmetic("not")
                elif symbol == "^":
                    self.__VMWriter.write_arithmetic("shiftleft")
                else:
                    self.__VMWriter.write_arithmetic("shiftright")
                look_ahead = False
        if (look_ahead):
            self.__tokenizer.advance()


    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        num_of_expressions = 0
        if self.__tokenizer.token_type() != "symbol" or self.__tokenizer.symbol() != ")":
            self.compile_expression()
            num_of_expressions += 1
            while self.__tokenizer.token_type() == "symbol" and self.__tokenizer.symbol() == ",":
                self.__tokenizer.advance()
                self.compile_expression()
                num_of_expressions += 1
        return num_of_expressions
