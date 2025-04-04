#!/usr/bin/python

class Symbol():
    def __init__(self, name):
        self.name = name


class VariableSymbol(Symbol):

    def __init__(self, name, type, size=None):
        super().__init__(name)
        self.type = type
        self.size = size
    


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = {}
    

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
    

    def get(self, name): # get variable symbol or fundef from <name> entry
        s = self.symbols.get(name)
        if s is not None: return s
        if self.parent is not None:
            return self.parent.get(name)
    

    def getParentScope(self):
        return self.parent
    

    def pushScope(self, name):
        return SymbolTable(self, name)
    

    def popScope(self):
        return self.parent
    


