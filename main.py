
import sys
from scanner_sly import Scanner
from parser_sly import Mparser
from TypeChecker import TypeChecker
from TreePrinter import TreePrinter
from Interpreter import Interpreter

from time import perf_counter


if __name__ == '__main__':

    # filename = "fibonacci"
    # filename = "matrix"
    # filename = "pi"
    # filename = "primes"
    # filename = "triangle"
    filename = "sqrt"

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/" + f"{filename}.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    parser = Mparser()
    typeChecker = TypeChecker()
    interpreter = Interpreter()


    ast = parser.parse(lexer.tokenize(text))
    if parser.err is True:
        parser.err_node.printTree()
        sys.exit(0)

    # ast.printTree()

    typeChecker.visit(ast)
    if len(typeChecker.error_list) > 0:
        print("-------- ERRORS ----------")
        typeChecker.print_errors()
        sys.exit(0)

    interpreter.visit(ast)