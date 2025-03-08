"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        # Your code goes here!
        self.__class_symtable = {}
        self.__static_counter = 0
        self.__field_counter = 0
        self.__subroutine_symtable = {}
        self.__argument_counter = 0
        self.__local_counter = 0

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        self.__subroutine_symtable.clear()
        self.__argument_counter = 0
        self.__local_counter = 0

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        # Your code goes here!
        if (kind == "static" or kind == "field"):
            if (kind == "static"):
                index = self.__static_counter
                self.__static_counter += 1
            else:
                index = self.__field_counter
                self.__field_counter += 1
            self.__class_symtable[name] = (type,kind,index)
        else:
            if (kind == "argument"):
                index = self.__argument_counter
                self.__argument_counter += 1
            else: #Meaning its a var(local segment)
                index = self.__local_counter
                self.__local_counter += 1
            self.__subroutine_symtable[name] = (type,kind,index)

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        # Your code goes here!
        if (kind == "static"):
            return self.__static_counter
        if (kind == "field"):
            return self.__field_counter
        if (kind == "argument"):
            return self.__argument_counter
        return self.__local_counter 

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        # Your code goes here!
        if name in self.__subroutine_symtable:
            return self.__subroutine_symtable[name][1]
        if name in self.__class_symtable:
            if(self.__class_symtable[name][1] == "field"):
                return "this"
            return self.__class_symtable[name][1]
        return None

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        # Your code goes here!
        if name in self.__subroutine_symtable:
            return self.__subroutine_symtable[name][0]
        if name in self.__class_symtable:
            return self.__class_symtable[name][0]
        return None

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        # Your code goes here!
        if name in self.__subroutine_symtable:
            return self.__subroutine_symtable[name][2]
        if name in self.__class_symtable:
            return self.__class_symtable[name][2]
        return None
    def status_of(self, name:str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: data of the named identifier
        """
        kind = self.kind_of(name)
        type = self.type_of(name)
        index = self.index_of(name)
        return f"kind: {kind}, type: {type}, index: {index}"