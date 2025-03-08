"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import JackTokenizer


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
        self.__output = output_stream

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # self.__output.write("<tokens> \n")
        self.__output.write("<class> \n")
        self.__output.write("<keyword> class </keyword> \n")
        self.__tokenizer.advance()
        current_token = self.__tokenizer.symbol()
        self.__output.write("<identifier> "+ current_token + " </identifier> \n" )
        self.__tokenizer.advance()
        self.__output.write("<symbol> { </symbol> \n")
        self.__tokenizer.advance()
        current_token = self.__tokenizer.keyword()
        while (current_token != "}"):
            if (current_token == "static" or current_token == "field"):
                self.compile_class_var_dec()
            elif (current_token == "constructor" or current_token == "method" or current_token == "function"):
                self.compile_subroutine()
            self.__tokenizer.advance()
            current_token = self.__tokenizer.keyword()
        self.__output.write("<symbol> } </symbol> \n")
        self.__output.write("</class> \n")
        # self.__output.write("</tokens> \n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.__output.write("<classVarDec> \n")
        current_token = self.__tokenizer.keyword()
        self.__output.write("<keyword> " + current_token + " </keyword> \n")
        self.__tokenizer.advance()
        if self.__tokenizer.token_type() == "keyword":
            self.__output.write("<keyword> " + self.__tokenizer.keyword() + " </keyword> \n")
        elif self.__tokenizer.token_type() == "identifier":
            self.__output.write("<identifier> " + self.__tokenizer.identifier() + " </identifier> \n")
        while True:
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "identifier":
                self.__output.write("<identifier> " + self.__tokenizer.identifier() + " </identifier> \n")
            self.__tokenizer.advance()
            if self.__tokenizer.symbol() == ",":
                self.__output.write("<symbol> , </symbol> \n")
            elif self.__tokenizer.symbol() == ";":
                self.__output.write("<symbol> ; </symbol> \n")
                self.__output.write("</classVarDec> \n")
                return


    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        self.__output.write("<subroutineDec> \n")
        current_token = self.__tokenizer.keyword()
        self.__output.write("<keyword> " + current_token + " </keyword> \n")
        self.__tokenizer.advance()
        if self.__tokenizer.token_type() == "keyword":
            self.__output.write("<keyword> " + self.__tokenizer.keyword() + " </keyword> \n")
        elif self.__tokenizer.token_type() == "identifier":
            self.__output.write("<identifier> " + self.__tokenizer.identifier() + " </identifier> \n")
        self.__tokenizer.advance()
        current_token = self.__tokenizer.identifier()
        self.__output.write("<identifier> " + current_token + " </identifier> \n")
        self.__tokenizer.advance()
        self.__output.write("<symbol> ( </symbol> \n")
        self.compile_parameter_list()
        self.__output.write("<symbol> ) </symbol> \n <subroutineBody> \n")
        self.__tokenizer.advance()
        self.__output.write("<symbol> { </symbol> \n")
        while True:
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "keyword":
                if self.__tokenizer.keyword() == "var":
                    self.compile_var_dec()
                else:
                    break
            else:
                break
        self.compile_statements()
        self.__output.write("<symbol> } </symbol> \n </subroutineBody> \n")
        self.__output.write("</subroutineDec> \n")

        


    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        self.__output.write("<parameterList> \n")
        while True:
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "identifier":
                self.__output.write("<identifier> " + self.__tokenizer.identifier() + " </identifier> \n")
            elif self.__tokenizer.token_type() == "keyword":
                self.__output.write("<keyword> " + self.__tokenizer.keyword() + " </keyword> \n")
            elif self.__tokenizer.symbol() == ",":
                self.__output.write("<symbol> , </symbol> \n")
            elif self.__tokenizer.symbol() == ")":
                self.__output.write("</parameterList> \n")
                return

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.__output.write("<varDec> \n <keyword> var </keyword> \n")
        self.__tokenizer.advance()
        if self.__tokenizer.token_type() == "identifier":
            self.__output.write("<identifier> " + self.__tokenizer.identifier() + " </identifier> \n")
        elif self.__tokenizer.token_type() == "keyword":
            self.__output.write("<keyword> " + self.__tokenizer.keyword() + " </keyword> \n")
        while True:
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "identifier":
                self.__output.write("<identifier> " + self.__tokenizer.identifier() + " </identifier> \n")
            self.__tokenizer.advance()
            if self.__tokenizer.symbol() == ",":
                self.__output.write("<symbol> , </symbol> \n")
            elif self.__tokenizer.symbol() == ";":
                self.__output.write("<symbol> ; </symbol> \n")
                self.__output.write("</varDec> \n")
                return
       


    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self.__output.write("<statements> \n")
        while True:
            if_statement = False
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
                self.__output.write("</statements> \n")
                return
            if (not if_statement):
                self.__tokenizer.advance()


    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.__output.write("<doStatement> \n <keyword> do </keyword> \n")
        while True:
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "identifier":
                self.__output.write("<identifier> " + self.__tokenizer.identifier() + " </identifier> \n")
            self.__tokenizer.advance()
            if self.__tokenizer.symbol() == ".":
                self.__output.write("<symbol> . </symbol> \n")
            elif self.__tokenizer.symbol() == "(":
                self.__output.write("<symbol> ( </symbol> \n")
                break
        self.__tokenizer.advance()
        self.compile_expression_list()
        self.__tokenizer.advance()
        self.__output.write("<symbol> ) </symbol> \n <symbol> ; </symbol> \n </doStatement> \n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.__output.write("<letStatement> \n <keyword> let </keyword> \n")
        self.__tokenizer.advance()
        var_name = self.__tokenizer.identifier()
        self.__output.write(f"<identifier> {var_name} </identifier> \n")
        self.__tokenizer.advance()
        if self.__tokenizer.symbol() == "[":
            self.__output.write("<symbol> [ </symbol> \n")
            self.__tokenizer.advance()
            self.compile_expression()
            self.__output.write("<symbol> ] </symbol> \n")
            self.__tokenizer.advance()
        self.__output.write("<symbol> = </symbol> \n")
        self.__tokenizer.advance()
        self.compile_expression()
        self.__output.write("<symbol> ; </symbol> \n")
        self.__output.write("</letStatement> \n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.__output.write("<whileStatement> \n")
        self.__output.write("<keyword> while </keyword> \n")
        self.__tokenizer.advance()
        self.__output.write("<symbol> ( </symbol> \n")
        self.__tokenizer.advance()
        self.compile_expression()
        self.__tokenizer.advance()
        self.__output.write("<symbol> ) </symbol> \n")
        self.__tokenizer.advance()
        self.__output.write("<symbol> { </symbol> \n")
        self.compile_statements()
        self.__output.write("<symbol> } </symbol> \n")
        self.__output.write("</whileStatement> \n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.__output.write("<returnStatement> \n")
        self.__output.write("<keyword> return </keyword> \n")
        self.__tokenizer.advance()
        if self.__tokenizer.token_type() != "symbol" or self.__tokenizer.symbol() != ";":
            self.compile_expression()
        self.__output.write("<symbol> ; </symbol> \n")
        self.__output.write("</returnStatement> \n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.__output.write("<ifStatement> \n")
        self.__output.write("<keyword> if </keyword> \n")
        self.__tokenizer.advance()
        self.__output.write("<symbol> ( </symbol> \n")
        self.__tokenizer.advance()
        self.compile_expression()
        self.__output.write("<symbol> ) </symbol> \n")
        self.__tokenizer.advance()
        self.__output.write("<symbol> { </symbol> \n")
        self.__tokenizer.advance()
        self.compile_statements()
        self.__output.write("<symbol> } </symbol> \n")
        self.__tokenizer.advance()
        if self.__tokenizer.token_type() == "keyword" and self.__tokenizer.keyword() == "else":
            self.__output.write("<keyword> else </keyword> \n")
            self.__tokenizer.advance()
            self.__output.write("<symbol> { </symbol> \n")
            self.__tokenizer.advance()
            self.compile_statements()
            self.__tokenizer.advance()
            self.__output.write("<symbol> } </symbol> \n")
        self.__output.write("</ifStatement> \n")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        operators = {'+',"-",'*','/','&amp;','|','&lt;','&gt;','='}
        self.__output.write("<expression> \n")
        self.compile_term()
        while (self.__tokenizer.token_type() == "symbol" and self.__tokenizer.symbol() in operators):
            self.__output.write("<symbol> " + self.__tokenizer.symbol() + " </symbol> \n")
            self.__tokenizer.advance()
            self.compile_term()
        self.__output.write("</expression> \n")

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
        # Your code goes here!
        look_ahead = True
        self.__output.write("<term> \n")
        type = self.__tokenizer.token_type()
        if type in {"string_const", "int_const", "keyword"}:
            if type == "string_const":
                self.__output.write("<stringConstant> "+self.__tokenizer.string_val() + " </stringConstant> \n")
            elif type == "int_const":
                self.__output.write("<integerConstant> "+str(self.__tokenizer.int_val()) + " </integerConstant> \n")
            else:
                self.__output.write("<keyword> "+ self.__tokenizer.keyword() + " </keyword> \n")
        elif type == "identifier":
             var_name = self.__tokenizer.identifier()
             self.__output.write("<identifier> "+ var_name + " </identifier> \n")
             self.__tokenizer.advance()
             look_ahead = False
             if self.__tokenizer.token_type() == "symbol":
                if self.__tokenizer.symbol() == "[":
                    self.__output.write("<symbol> [ </symbol> \n")
                    self.__tokenizer.advance()
                    self.compile_expression()
                    self.__output.write("<symbol> ] </symbol> \n")
                    look_ahead = True
                elif self.__tokenizer.symbol() == "(":
                    self.__output.write("<symbol> ( </symbol> \n")
                    self.__tokenizer.advance()
                    self.compile_expression_list()
                    self.__output.write("<symbol> ) </symbol> \n")
                    self.__tokenizer.advance()
                    look_ahead = False
                elif self.__tokenizer.symbol() == ".":
                    self.__output.write("<symbol> . </symbol> \n")
                    self.__tokenizer.advance()
                    self.__output.write("<identifier> " + self.__tokenizer.identifier() + " </identifier> \n")
                    self.__output.write("<symbol> ( </symbol> \n")
                    self.__tokenizer.advance()
                    self.__tokenizer.advance()
                    self.compile_expression_list()
                    self.__output.write("<symbol> ) </symbol> \n")
                    look_ahead = True
        elif type == "symbol":
            symbol = self.__tokenizer.symbol()
            if symbol == "(":
                self.__output.write("<symbol> ( </symbol> \n")
                self.__tokenizer.advance()
                self.compile_expression()
                self.__output.write("<symbol> ) </symbol> \n")
            elif symbol in {"-","~","^","#"}:
                self.__output.write("<symbol> " + symbol + " </symbol> \n")
                self.__tokenizer.advance()
                self.compile_term()
                look_ahead = False
        if (look_ahead):
            self.__tokenizer.advance()
        self.__output.write("</term> \n")


    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.__output.write("<expressionList> \n")
        if self.__tokenizer.token_type() != "symbol" or self.__tokenizer.symbol() != ")":
            self.compile_expression()
            while self.__tokenizer.token_type() == "symbol" and self.__tokenizer.symbol() == ",":
                self.__output.write("<symbol> , </symbol> \n")
                self.__tokenizer.advance()
                self.compile_expression()
        self.__output.write("</expressionList> \n")
