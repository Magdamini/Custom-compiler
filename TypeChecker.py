import AST
from collections import defaultdict
from SymbolTable import SymbolTable, VariableSymbol

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

# numbers
ttype['+']['int']['int'] = 'int'
ttype['+']['float']['int'] = 'float'
ttype['+']['int']['float'] = 'float'
ttype['+']['float']['float'] = 'float'

ttype['-']['int']['int'] = 'int'
ttype['-']['float']['int'] = 'float'
ttype['-']['int']['float'] = 'float'
ttype['-']['float']['float'] = 'float'

ttype['*']['int']['int'] = 'int'
ttype['*']['float']['int'] = 'float'
ttype['*']['int']['float'] = 'float'
ttype['*']['float']['float'] = 'float'

ttype['/']['int']['int'] = 'float'
ttype['/']['float']['int'] = 'float'
ttype['/']['int']['float'] = 'float'
ttype['/']['float']['float'] = 'float'

# matrices
ttype['*']['matrix']['int'] = 'matrix'
ttype['*']['matrix']['float'] = 'matrix'
ttype['*']['int']['matrix'] = 'matrix'
ttype['*']['float']['matrix'] = 'matrix'
ttype['*']['matrix']['matrix'] = 'matrix'

ttype['/']['matrix']['float'] = 'matrix'
ttype['/']['matrix']['int'] = 'matrix'


ttype['.+']['matrix']['matrix'] = 'matrix'
ttype['.-']['matrix']['matrix'] = 'matrix'
ttype['.*']['matrix']['matrix'] = 'matrix'
ttype['./']['matrix']['matrix'] = 'matrix'

# strings
ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'
ttype['*']['int']['string'] = 'string'


# assign
ttype['+=']['int']['int'] = 'int'
ttype['+=']['int']['float'] = 'float'
ttype['+=']['float']['int'] = 'float'
ttype['+=']['float']['float'] = 'float'
ttype['+=']['matrix']['matrix'] = 'matrix'

ttype['-=']['int']['int'] = 'int'
ttype['-=']['int']['float'] = 'float'
ttype['-=']['float']['int'] = 'float'
ttype['-=']['float']['float'] = 'float'
ttype['-=']['matrix']['matrix'] = 'matrix'

ttype['*=']['int']['int'] = 'int'
ttype['*=']['int']['float'] = 'float'
ttype['*=']['float']['int'] = 'float'
ttype['*=']['float']['float'] = 'float'
ttype['*=']['matrix']['matrix'] = 'matrix'
ttype['*=']['matrix']['float'] = 'matrix'
ttype['*=']['matrix']['int'] = 'matrix'

ttype['/=']['int']['int'] = 'int'
ttype['/=']['int']['float'] = 'float'
ttype['/=']['float']['int'] = 'float'
ttype['/=']['float']['float'] = 'float'
ttype['/=']['matrix']['matrix'] = 'matrix'
ttype['/=']['matrix']['float'] = 'matrix'
ttype['/=']['matrix']['int'] = 'matrix'



#---------------------------------------------------------------------------#

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)

#---------------------------------------------------------------------------#


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.curr_scope = SymbolTable(None, 'main')
        self.error_list = []
        self.loop_cnt = 0

    def add_error(self, line_no, msg):
        self.error_list.append((line_no, msg))

    def print_errors(self):
        err_no = len(self.error_list)
        if err_no == 0:
            print("No errors found")
            return
        print(f"{err_no} error{'' if err_no == 1 else "s"} found")
        for line_no, msg in sorted(self.error_list, key=lambda x: x[0]):
            print(f"Error at line {line_no}: {msg}")

    def get_size(self, node):
        if isinstance(node, AST.Variable):
            var = self.curr_scope.get(node.name)
            return var.size
        return node.size

#----------visit------------------#

    def visit_Program(self, node):
        self.visit(node.i_list)   

    def visit_Instructions(self, node):
        for i in node.i_list:
            self.visit(i)

    def visit_IntNum(self, node):
        return 'int'
    
    def visit_FloatNum(self, node):
        return 'float'
    
    def visit_StringText(self, node):
        return 'string'
    
    def visit_Vector(self, node):
        return len(node.inner_list)
    
    def visit_Matrix(self, node):
        cols = self.visit(node.outer_list[0])
        row = 0
        err = False
        for v in node.outer_list:
            row += 1
            if self.visit(v) != cols:
                self.add_error(v.line_no, "Diffrent vector sizes in matrix initialization")
                err = True

        if not err:
            node.size = row, cols
        return 'matrix'

    def visit_InLoopInstr(self, node):
        if self.loop_cnt == 0:
            self.add_error(node.line_no, f"Incorrect usage of {node.name} statement")
        
    def visit_Variable(self, node):
        s = self.curr_scope.get(node.name)
        if s is None:
            self.add_error(node.line_no, f"Undeclared variable {node.name}")
        else:
            return s.type


    def visit_MatrixRef(self, node):
        t = self.visit(node.name)
        if t is None: return
        if t != 'matrix':
            self.add_error(node.line_no, f"'{t}' object is not subscriptable")
            return
        size = self.get_size(node.name)

        if size != None:
            rows, cols = size
            if isinstance(node.indexes[0], AST.IntNum) and node.indexes[0].value >= rows:
                self.add_error(node.line_no, f"Row index out of range")
            if isinstance(node.indexes[1], AST.IntNum) and node.indexes[1].value >= cols:
                self.add_error(node.line_no, f"Column index out of range")
        


    def visit_BinExpr(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op
        res_type = ttype[op][type1][type2]
        if res_type is None:
            self.add_error(node.line_no, f"Cannot perform: {type1} {op} {type2}")
            return
        
        if type1 == 'matrix' and type2 == 'matrix':
            l_size, r_size = self.get_size(node.left), self.get_size(node.right)
            if l_size is not None and r_size is not None:
                r1, c1 = l_size
                r2, c2 = r_size
                if op[0] == '.':
                    if r1 != r2 or c1 != c2:
                        self.add_error(node.line_no, f"Diffrent matrix sizes in: {type1} {op} {type2}")
                    else:
                        node.size = r1, c1
                else:
                    if c1 != r2:
                        self.add_error(node.line_no, f"Incorrect sizes in matrix multiplication")
                    else:
                        node.size = r1, c2
        elif type1 == 'matrix':
            node.size = l_size
        elif type2 == 'matrix':
            node.size = r_size
        

        return ttype[op][type1][type2]

    def visit_AssignInst(self, node):
        if node.op != '=':
            t1 = self.visit(node.left)
            t2 = self.visit(node.right)
            # check t1 t2 and op types
            op = node.op
            res_type = ttype[op][t1][t2]
            if res_type is None:
                self.add_error(node.line_no, f"Cannot perform: {t1} {node.op} {t2}")
                return
            # zakładam że dla macierzy += to .+
            if t1 == 'matrix' and t2 == 'matrix':
                l_size, r_size = self.get_size(node.left), self.get_size(node.right)
                if l_size is not None and r_size is not None:
                    r1, c1 = l_size
                    r2, c2 = r_size
                    if r1 != r2 or c1 != c2:
                        self.add_error(node.line_no, f"Diffrent matrix sizes in: {t1} {op} {t2}")
        else:
            # new variable in scope
            if isinstance(node.left, AST.MatrixRef):
                self.visit(node.left)
                t = self.visit(node.right)
                if t not in ('float', 'int'):
                    self.add_error(node.line_no, f"Type {t} cannot be a matrix element")
            else:
                t = self.visit(node.right)
                var_sym = VariableSymbol(node.left.name, t)
                self.curr_scope.put(node.left.name, var_sym)
                if t == 'matrix':
                    var_sym.size = node.right.size

    def visit_RelExpr(self, node):
        type1 = self.visit(node.left)      
        type2 = self.visit(node.right)    
        op    = node.op
        if type1 == type2 and op in ('==', '!='):
            return 
        if type1 not in ('float', 'int') or type2 not in ('float', 'int'):
            self.add_error(node.line_no, f"Invalid types: {type1} {op} {type2}")
        

    def visit_MatrixTranspose(self, node):
        expr_type = self.visit(node.expr)
        if expr_type != 'matrix':
            self.add_error(node.line_no, f'Cannot transpose argument of type {expr_type}')
        else:
            s = self.get_size(node.expr)
            if s is not None:
                node.size = s[1], s[0]
        return 'matrix'

    def visit_MatrixExpr(self, node):
        if node.name == 'eye' and len(node.args) > 1: 
            self.add_error(node.line_no, f"Too many arguments in {node.name}() function")
            return 'matrix'
        elif len(node.args) > 2:
            self.add_error(node.line_no, f"Too many arguments in {node.name}() function")
            return 'matrix'

        for arg in node.args:
            expr_type = self.visit(arg)
            if expr_type != 'int':
                self.add_error(node.line_no, f'Invalid argument type in {node.name}() function')
        if len(node.args) == 1 and isinstance(node.args[0], AST.IntNum):
            node.size = (node.args[0].value, node.args[0].value)
        elif len(node.args) == 2 and isinstance(node.args[1], AST.IntNum) and isinstance(node.args[0], AST.IntNum):
            node.size = (node.args[0].value, node.args[1].value)
        return 'matrix'
        
            
    def visit_UnaryMinus(self, node):
        t = self.visit(node.expr)
        if t not in ("int", 'float', 'matrix'):
            self.add_error(node.line_no, f"Unary minus cannot be used with expresion of the type {t}")

        return t
    

    def visit_IfInstr(self, node):
        self.visit(node.cond)
        self.curr_scope = self.curr_scope.pushScope('if')
        self.visit(node.then_instr)
        self.curr_scope = self.curr_scope.popScope()
        if node.else_instr is not None:
            self.curr_scope = self.curr_scope.pushScope('else')
            self.visit(node.else_instr)
            self.curr_scope = self.curr_scope.popScope()


    def visit_ForLoop(self, node):
        range_type1 = self.visit(node.i1)
        range_type2 = self.visit(node.i2)
        if range_type1 != 'int' or range_type2 != 'int':
            self.add_error(node.line_no, "Invalid types in range() in for loop")

        self.loop_cnt += 1
        self.curr_scope = self.curr_scope.pushScope('for')
        self.curr_scope.put(node.name, VariableSymbol(node.name, 'int'))
        
        self.visit(node.instruction)

        self.loop_cnt -= 1
        self.curr_scope = self.curr_scope.popScope()

    def visit_WhileLoop(self, node):
        self.visit(node.cond)

        self.loop_cnt += 1
        self.curr_scope = self.curr_scope.pushScope('while')
        
        self.visit(node.instruction)

        self.loop_cnt -= 1
        self.curr_scope = self.curr_scope.popScope()


    def visit_PrintInstr(self, node):
        for arg in node.args:
            self.visit(arg)

    def visit_ReturnInstr(self, node):
        self.visit(node.expr)