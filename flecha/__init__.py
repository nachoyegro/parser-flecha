import flecha.parser as parser
import flecha.ast

def execute(source):
    res = parser.get_parser().parse(source)
    #Printeo el AST
    print(res)
