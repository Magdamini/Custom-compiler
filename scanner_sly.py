import sys
from sly import Lexer


class Scanner(Lexer):

    tokens = {ID, INTNUM, FLOATNUM, STR,
              ZEROS, ONES, EYE, 
              DOTADD, DOTSUB, DOTMUL, DOTDIV, 
              ADDASSIGN, SUBASSIGN,
              MULASSIGN, DIVASSIGN,
              LE, GE, EQ, NE, 
              IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN, PRINT}

    literals = { '(', ')', '{', '}', '[', ']', ';', ',', '\'', ':', '+', '-', '*', '/', '=', '<', '>'}

    # numbers
    @_(r'((\d+\.\d*|\d*\.\d+)([eE][+-]?\d+)?)|\d+([eE][+-]?\d+)')
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    # regular expressions
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='

    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'
    
    EQ = r'=='
    LE = r'<='
    GE = r'>='
    NE = r'!='
    
    # identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['print'] = PRINT
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES

    # ignore rules
    ignore = ' \t'
    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
    
    # strings
    @_(r'\"([^"\\]|\\.)*\"')
    def STR(self, t):
        t.value = t.value[1:-1]
        self.lineno += t.value.count('\n')
        return t
    
    def error(self, t):
        print(f"Line {self.lineno}: Illegal character '{t.value[0]}'")
        self.index += 1


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/" + "example_lab3.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    
    for tok in lexer.tokenize(text):
        print(f"({tok.lineno}): {tok.type}({tok.value})")
