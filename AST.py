
class Node(object):
    def __init__(self, line_no):
        self.line_no = line_no
        self.size = None

class Program(Node):
    def __init__(self, i_list, line_no):
        super().__init__(line_no)
        self.i_list = i_list

class Instructions(Node):
    def __init__(self, i_list, line_no):
        super().__init__(line_no)
        self.i_list = i_list

class IntNum(Node):
    def __init__(self, value, line_no):
        super().__init__(line_no)
        self.value = value

class FloatNum(Node):
    def __init__(self, value, line_no):
        super().__init__(line_no)
        self.value = value

class StringText(Node):
    def __init__(self, txt, line_no):
        super().__init__(line_no)
        self.txt = txt

class Vector(Node):
    def __init__(self, inner_list, line_no):
        super().__init__(line_no)
        self.inner_list = inner_list

class Matrix(Node):
    def __init__(self, outer_list, line_no):
        super().__init__(line_no)
        self.outer_list = outer_list

class InLoopInstr(Node):
    def __init__(self, name, line_no):
        super().__init__(line_no)
        self.name = name


class Variable(Node):
    def __init__(self, name, line_no):
        super().__init__(line_no)
        self.name = name

class MatrixRef(Node):
    def __init__(self, name, indexes, line_no):
        super().__init__(line_no)
        self.name = name
        self.indexes = indexes

class BinExpr(Node):
    def __init__(self, op, left, right, line_no):
        super().__init__(line_no)
        self.op = op
        self.left = left
        self.right = right

class AssignInst(Node):
    def __init__(self, op, left, right, line_no):
        super().__init__(line_no)
        self.op = op
        self.left = left
        self.right = right

class RelExpr(Node):
    def __init__(self, op, left, right, line_no):
        super().__init__(line_no)
        self.op = op
        self.left = left
        self.right = right

class MatrixTranspose(Node):
    def __init__(self, expr, line_no):
        super().__init__(line_no)
        self.expr = expr

class MatrixExpr(Node):
    def __init__(self, name, args, line_no):
        super().__init__(line_no)
        self.name = name
        self.args = args

class UnaryMinus(Node):
    def __init__(self, expr, line_no):
        super().__init__(line_no)
        self.expr = expr


class IfInstr(Node):
    def __init__(self, cond, then_instr, else_instr=None, line_no=0):
        super().__init__(line_no)
        self.cond = cond
        self.then_instr = then_instr
        self.else_instr = else_instr

class ForLoop(Node):
    def __init__(self, name, i1, i2, instruction, line_no):
        super().__init__(line_no)
        self.name = name
        self.i1 = i1
        self.i2 = i2
        self.instruction = instruction

class WhileLoop(Node):
    def __init__(self, cond, instruction, line_no):
        super().__init__(line_no)
        self.cond = cond
        self.instruction = instruction

class PrintInstr(Node):
    def __init__(self, args, line_no):
        super().__init__(line_no)
        self.args = args


class ReturnInstr(Node):
    def __init__(self, expr, line_no):
        super().__init__(line_no)
        self.expr = expr



class Error(Node):
    def __init__(self, msg, line_no):
        super().__init__(line_no)
        self.msg = msg
