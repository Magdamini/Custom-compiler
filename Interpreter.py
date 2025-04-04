import numpy as np
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys


# TODO czy sprawdzać rozmiary macierzy 

sys.setrecursionlimit(10000)

opers = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,

    '.+': lambda x, y: x + y,
    '.-': lambda x, y: x - y,
    '.*': lambda x, y: x * y,
    './': lambda x, y: x / y,

    '+=': lambda x, y: x + y,
    '-=': lambda x, y: x - y,
    '*=': lambda x, y: x * y,
    '/=': lambda x, y: x / y,

    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '>': lambda x, y: x > y,
    '<': lambda x, y: x < y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y
}

class Interpreter(object):

    def __init__(self):
        self.memory_stack = MemoryStack(Memory('global'))

    @on('node')
    def visit(self, node):
        pass

#--------------when_visit-----------------#

    @when(AST.Program)
    def visit(self, node):
        try:
            self.visit(node.i_list)
        except ReturnException as e:
            print(e)

    @when(AST.Instructions)
    def visit(self, node):
        for instr in node.i_list:
            self.visit(instr)

    @when(AST.IntNum)
    def visit(self, node):
        return node.value


    @when(AST.FloatNum)
    def visit(self, node):
        return node.value


    @when(AST.StringText)
    def visit(self, node):
        return node.txt


    @when(AST.Vector)
    def visit(self, node):
        return [self.visit(x) for x in node.inner_list]

    @when(AST.Matrix)
    def visit(self, node):
        matrix = [self.visit(v) for v in node.outer_list]
        return np.array(matrix)

    @when(AST.InLoopInstr)
    def visit(self, node):
        if node.name == 'continue':
            raise ContinueException()
        else:
            raise BreakException()
        
    @when(AST.Variable)
    def visit(self, node):
        return self.memory_stack.get(node.name)

    @when(AST.MatrixRef)
    def visit(self, node):
        matrix = self.visit(node.name)
        i1 = self.visit(node.indexes[0])
        i2 = self.visit(node.indexes[1])
        n, m = matrix.shape
        if i1 < 0 or i1 >= n:
            print(f"Error at line {node.line_no}: Row index out of range")
            sys.exit(0)
        if i2 < 0 or i2 >= m:
            print(f"Error at line {node.line_no}: Column index out of range")
            sys.exit(0)
        return matrix[i1, i2]
    

    def perform_bin_op(self, r1, r2, op, line_no):
        if op in('/', '/=', './') and not np.all(r2):
            print(f"Error at line {line_no}: Zero division error")
            sys.exit(0)

        if isinstance(r1, np.ndarray) and isinstance(r2, np.ndarray):
            if r1.shape != r2.shape:
                print(f"Error at line {line_no}: Diffrent matrix sizes in: matrix {op} matrix")
                sys.exit(0)


        if isinstance(r1, np.ndarray) and isinstance(r2, np.ndarray) and op == '*':
            if r1.shape[1] != r2.shape[0]:
                print(f"Error at line {line_no}: Incorrect sizes in matrix multiplication")
                sys.exit(0)
            return r1 @ r2
        return opers[op](r1, r2)

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        return self.perform_bin_op(r1, r2, node.op, node.line_no)
        

    @when(AST.AssignInst)
    def visit(self, node):
        right = self.visit(node.right)
        if node.op != '=':
            left = self.visit(node.left)
            right = self.perform_bin_op(left, right, node.op, node.line_no)

        # przypisanie
        if isinstance(node.left, AST.MatrixRef):
            self.visit(node.left)
            matrix = self.visit(node.left.name)
            i1 = self.visit(node.left.indexes[0])
            i2 = self.visit(node.left.indexes[1])
            matrix[i1, i2] = right
        else:
            self.memory_stack.set(node.left.name, right)
        

    @when(AST.RelExpr)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return opers[node.op](left, right)

    @when(AST.MatrixTranspose)
    def visit(self, node):
        matrix = self.visit(node.expr)
        return np.transpose(matrix)

    @when(AST.MatrixExpr)
    def visit(self, node):
        if node.name == 'eye':
            param = self.visit(node.args[0])
            if param <= 0:
                print(f"Error at line {node.line_no}: Invalid argument in {node.name}() function")
                sys.exit(0)
            return np.eye(param)
        else:
            if len(node.args) > 1:
                p1, p2 = self.visit(node.args[0]), self.visit(node.args[1])
            else:
                p1 = p2 = self.visit(node.args[0])
            if p1 <= 0 or p2 <= 0:
                print(f"Error at line {node.line_no}: Invalid argument in {node.name}() function")
                sys.exit(0)
            if node.name == 'zeros':
                return np.zeros(shape=(p1, p2))
            elif node.name == 'ones':
                return np.ones(shape=(p1, p2))

    @when(AST.UnaryMinus)
    def visit(self, node):
        return -1 * self.visit(node.expr)


    @when(AST.IfInstr)
    def visit(self, node):
        cond = self.visit(node.cond)
        self.memory_stack.push(Memory("if-else"))
        if cond:
            self.visit(node.then_instr)
        elif node.else_instr is not None:
            self.visit(node.else_instr)
        self.memory_stack.pop()

    @when(AST.ForLoop)
    def visit(self, node):
        self.memory_stack.push(Memory("for"))
        start = self.visit(node.i1)
        end = self.visit(node.i2)
        self.memory_stack.insert(node.name, start)
        for i in range(start, end):
            try:
                self.memory_stack.set(node.name, i)
                self.visit(node.instruction)
            except ContinueException:
                continue
            except BreakException:
                break
        self.memory_stack.pop()

    # simplistic while loop interpretation
    @when(AST.WhileLoop)
    def visit(self, node):
        self.memory_stack.push(Memory("while"))
        while self.visit(node.cond):
            try:
                self.visit(node.instruction)
            except ContinueException:
                continue
            except BreakException:
                break
        self.memory_stack.pop()
    

    @when(AST.PrintInstr)
    def visit(self, node):
        for arg in node.args:
            print(self.visit(arg), end=" ")
        print()

    @when(AST.ReturnInstr)
    def visit(self, node):
        # print("Program result:", self.visit(node.expr))
        # sys.exit(0)
        raise ReturnException(self.visit(node.expr))
