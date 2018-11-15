import flecha.parser as parser
import flecha.ast
from flecha.compiler import FlechaCompiler

def execute(source):
    res = parser.get_parser().parse(source)
    #Printeo el AST
    print(res)
    evaluated = eval(repr(res))

    compiler = FlechaCompiler(evaluated)
    compiled = compiler.compile()
    print(compiled)
