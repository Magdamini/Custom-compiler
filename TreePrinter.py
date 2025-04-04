import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

def print_indent(indent=0):
        s = "| "
        print(s * indent, end='')

class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.i_list.printTree(indent)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instr in self.i_list:
            instr.printTree(indent)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print_indent(indent)
        print(str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print_indent(indent)
        print(str(self.value))

    @addToClass(AST.StringText)
    def printTree(self, indent=0):
        print_indent(indent)
        print(self.txt)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print_indent(indent)
        print("VECTOR")
        for i in self.inner_list:
            i.printTree(indent + 1)
    
    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print_indent(indent)
        print("VECTOR")
        for v in self.outer_list:
            v.printTree(indent + 1)

    @addToClass(AST.InLoopInstr)
    def printTree(self, indent=0):
        print_indent(indent)
        print(self.name.upper())

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print_indent(indent)
        print(self.name)

    @addToClass(AST.MatrixRef)
    def printTree(self, indent=0):
        print_indent(indent)
        print("REF")
        self.name.printTree(indent + 1)
        for i in self.indexes:
            i.printTree(indent + 1)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print_indent(indent)
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.AssignInst)
    def printTree(self, indent=0):
        print_indent(indent)
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.RelExpr)
    def printTree(self, indent=0):
        print_indent(indent)
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.MatrixTranspose)
    def printTree(self, indent=0):
        print_indent(indent)
        print("TRANSPOSE")
        self.expr.printTree(indent + 1)

    @addToClass(AST.MatrixExpr)
    def printTree(self, indent=0):
        print_indent(indent)
        print(self.name)
        for arg in self.args:
            arg.printTree(indent + 1)

    @addToClass(AST.UnaryMinus)
    def printTree(self, indent=0):
        print_indent(indent)
        print("-")
        self.expr.printTree(indent + 1)

    @addToClass(AST.IfInstr)
    def printTree(self, indent=0):
        print_indent(indent)
        print("IF")
        self.cond.printTree(indent + 1)
        print_indent(indent)
        print("THEN")
        self.then_instr.printTree(indent + 1)
        if self.else_instr is not None:
            print_indent(indent)
            print("ELSE")
            self.else_instr.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print_indent(indent)
        print("FOR")
        print_indent(indent + 1)
        print(self.name)
        print_indent(indent + 1)
        print("RANGE")
        self.i1.printTree(indent + 2)
        self.i2.printTree(indent + 2)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        print_indent(indent)
        print("WHILE")
        self.cond.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.PrintInstr)
    def printTree(self, indent=0):
        print_indent(indent)
        print("PRINT")
        for arg in self.args:
            arg.printTree(indent + 1)

    @addToClass(AST.ReturnInstr)
    def printTree(self, indent=0):
        print_indent(indent)
        print("RETURN")
        self.expr.printTree(indent + 1)


    @addToClass(AST.Error)
    def printTree(self, indent=0):
        print_indent(indent)
        print(f"Parser error at line {self.line_no}: {self.msg}")

