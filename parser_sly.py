from sly import Parser
from scanner_sly import Scanner
import AST

class Mparser(Parser):

    def __init__(self):
        self.err = False


    tokens = Scanner.tokens

    # debugfile = 'parser.out'

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("nonassoc", ">", "<", 'LE', 'GE', 'EQ', 'NE'),
        ('left', "+", "-", 'DOTADD', 'DOTSUB'),
        ("left", '*', '/', 'DOTMUL', 'DOTDIV'),
        ('right', "'"),
        ('right', 'UMINUS')
    )




    @_('instructions')
    def program(self, p):
        return AST.Program(p[0], line_no=p.lineno)

    @_('instructions instruction')
    def instructions(self, p):
        return AST.Instructions(p[0].i_list + [p[1]], line_no=p.lineno)

    @_('instruction')
    def instructions(self, p):
        return AST.Instructions([p[0]], line_no=p.lineno)

    @_('loop_instruction',
       'return_instruction',
       'print_instruction',
       'assignment_instruction',
       'if_instruction')
    def instruction(self, p):
        return p[0]

    @_('BREAK ";"',
       'CONTINUE ";"')
    def instruction(self, p):
        return AST.InLoopInstr(p[0], line_no=p.lineno)

    @_('"{" instructions "}"')
    def instruction(self, p):
        return p[1]

    # matrix
    @_('number')
    def inner_list(self, p):
        return [p[0]]

    @_('number "," inner_list')
    def inner_list(self, p):
        return [p[0]] + p[2]

    @_('"[" inner_list "]"')
    def vector(self, p):
        return AST.Vector(p[1], line_no=p.lineno)

    @_('vector')
    def outer_list(self, p):
        return [p[0]]

    @_('vector "," outer_list')
    def outer_list(self, p):
        return [p[0]] + p[2]

    @_('"[" outer_list "]"')
    def matrix(self, p):
        return AST.Matrix(p[1], line_no=p.lineno)

    # assiggnments
    @_('ID')
    def ref(self, p):
        return AST.Variable(p[0], line_no=p.lineno)

    @_('ref "[" indexes "]"')
    def ref(self, p):
        return AST.MatrixRef(p[0], p[2], line_no=p.lineno)
    
    @_('ref "[" indexes "]"')
    def number(self, p):
        return AST.MatrixRef(p[0], p[2], line_no=p.lineno)

    @_('integer')
    def index(self, p):
        return p[0]

    # @_('index')
    # def indexes(self, p):
    #     return [p[0]]

    @_('index "," index')
    def indexes(self, p):
        return [p[0], p[2]]


    @_('ref "=" expr ";"',
       'ref ADDASSIGN expr ";"',
       'ref SUBASSIGN expr ";"',
       'ref MULASSIGN expr ";"',
       'ref DIVASSIGN expr ";"')
    def assignment_instruction(self, p):
        return AST.AssignInst(p[1], p[0], p[2], line_no=p.lineno)

    # expressions

    @_('"(" expr ")"')
    def expr(self, p):
        return p[1]

    @_('expr "+" expr',
       'expr DOTADD expr',
       'expr "-" expr',
       'expr DOTSUB expr',
       'expr "*" expr',
       'expr DOTMUL expr',
       'expr "/" expr',
       'expr DOTDIV expr')
    def expr(self, p):
        return AST.BinExpr(p[1], p[0], p[2], line_no=p.lineno)
    
    
    @_('expr ">" expr',
       'expr "<" expr',
       'expr LE expr',
       'expr GE expr',
       'expr EQ expr',
       'expr NE expr')
    def condition(self, p):
        return AST.RelExpr(p[1], p[0], p[2], line_no=p.lineno)

    @_('ZEROS "(" args ")"',
       'ONES "(" args ")"',
       'EYE "(" args ")"')
    def expr(self, p):
        return AST.MatrixExpr(p[0], p[2], line_no=p.lineno)

    @_('expr "\'"' )
    def expr(self, p):
        return AST.MatrixTranspose(p[0], line_no=p.lineno)

    @_('FLOATNUM')
    def number(self, p):
        return AST.FloatNum(p[0], line_no=p.lineno)

    @_('INTNUM')
    def integer(self, p):
        return AST.IntNum(p[0], line_no=p.lineno)
    
    @_('ID')
    def integer(self, p):
        return AST.Variable(p[0], line_no=p.lineno)

    @_('integer')
    def number(self, p):
        return p[0]

    @_('matrix')
    def expr(self, p):
        return p[0]

    @_('number')
    def expr(self, p):
        return p[0]

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return AST.UnaryMinus(p[1], line_no=p.lineno)

    # if
    @_('IF "(" condition ")" instruction %prec IFX')
    def if_instruction(self, p):
        return AST.IfInstr(p[2], p[4], line_no=p.lineno)

    @_('IF "(" condition ")" instruction ELSE instruction')
    def if_instruction(self, p):
        return AST.IfInstr(p[2], p[4], p[6], line_no=p.lineno)

    # loops
    @_('WHILE "(" condition ")" instruction')
    def loop_instruction(self, p):
        return AST.WhileLoop(p[2], p[4], line_no=p.lineno)

    @_('FOR ID "=" expr ":" expr instruction')
    def loop_instruction(self, p):
        return AST.ForLoop(p[1], p[3], p[5], p[6], line_no=p.lineno)

    # print
    @_('PRINT args ";"')
    def print_instruction(self, p):
        return AST.PrintInstr(p[1], line_no=p.lineno)
    
    @_('STR')
    def expr(self, p):
        return AST.StringText(p[0], line_no=p.lineno)
    
    @_('expr')
    def arg(self, p):
        return p[0]
        
    @_('arg')
    def args(self, p):
        return [p[0]]

    @_('args "," arg')
    def args(self, p):
        return p[0] + [p[2]]

    # return
    @_('RETURN expr ";"')
    def return_instruction(self, p):
        return AST.ReturnInstr(p[1], line_no=p.lineno)

    def error(self, p):
        if p is not None:
            self.err_node = AST.Error(f"Syntax error near {p.type}", line_no = p.lineno)
        else:
            self.err_node = AST.Error(f"Syntax error near EOF", line_no='end')
        self.err = True
        while True:
            tok = next(self.tokens, None)
            if not tok:
                break
            # self.errok()
        return tok

    



