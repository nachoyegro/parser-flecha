
class Node(object):
    def __init__(self,type,children=[], leaf=None):
        self.type = type
        self.children = children
        self.leaf = leaf
        self.transform()

    def transform(self):
        pass

    def add_child(self,child):
        self.children.append(child)
        return self

    def print_leaf(self, level=0):
        string = ''
        if self.leaf:
            string += repr(self.leaf)
            if self.children:
                string += ','
            else:
                string += '],'
        return string

    def print_children(self, level):
        string = ''
        if self.children:
            for child in self.children:
                if child and repr(child):
                    try:
                        string += child.repr(level+1)
                    except:
                        string += repr(child) + ', '
            string += " "*level+ "], \n"
        return string

    #TODO: refactorear esto
    def __repr__(self, level=0):
        ret = ' '*level+ '['
        ret += self.print_type(level)
        ret += self.print_leaf(level)
        ret += '\n'
        ret += self.print_children(level)
        return ret

    def print_type(self, level):
        return '"' +str(self.type)+'",'

    def repr(self, level=0):
        return self.__repr__(level)

class Empty(Node):
    pass

    def __str__(self):
        return 'Empty'

class Program(Node):
    def __init__(self,children=[], leaf=None):
        super(Program, self).__init__('Program',children, leaf)

    def __repr__(self, level=0):
        ret = "["
        if self.children:
            ret += '\n'
            for child in self.children:
                if child:
                    #TODO: esto hay que cambiarlo
                    try:
                        ret += child.repr(level+1)
                    except:
                        ret += repr(child)
            ret += " "*level+ "]\n"
        else:
            ret += ']'
        return ret


class Def(Node):
    def __init__(self,children=[], leaf=None):
        super(Def, self).__init__('Def',children, leaf)

class BinOp(Node):

    def __init__(self, children=[], leaf=None):
        super(BinOp, self).__init__('BinOp',children, leaf)

class ExprNumber(Node):
    def __init__(self,children=[], leaf=None):
        super(ExprNumber, self).__init__('ExprNumber',children, leaf)

class ExprApply(Node):
    def __init__(self,children=[], leaf=None):
        super(ExprApply, self).__init__('ExprApply',children, leaf)

class CaseBranch(Node):
    def __init__(self,children=[], leaf=None, parameters=None):
        self.parameters=parameters
        super(CaseBranch, self).__init__('CaseBranch',children, leaf)

    def print_leaf(self, level=0):
        string = ''
        if self.leaf:
            string += repr(self.leaf) + self.print_parameters()
        if not self.children:
            string += '],'
        return string

    def print_parameters(self):
        if self.parameters is not None:
            return ', ' + repr(self.parameters) + ','
        return ''

class ExprCase(Node):
    def __init__(self,children=[], leaf=None):
        super(ExprCase, self).__init__('ExprCase',children, leaf)

    def print_leaf(self, level=0):
        str = ''
        if self.leaf:
            str = '\n'
            str += ' '*level + repr(self.leaf)
        return str

    def __repr__(self, level=0):
        ret = ' '*level + '['
        ret += self.print_type(level+1) if self.leaf else ''
        ret += self.print_leaf(level+1)
        ret += ' '*(level+1) + '[\n'
        ret += self.print_children(level+1)
        ret += ' '*(level+1) + ']\n'
        ret += ' '*level + ']\n'
        return ret

    def print_children(self, level):
        ret = ''
        for child in self.children:
            if child:
                ret += child.repr(level+1)
        return ret

class ExprLet(Node):
    def __init__(self,children=[], leaf=None):
        super(ExprLet, self).__init__('ExprLet',children, leaf)

class Parameters(Node):
    def __init__(self,children=[], leaf=None):
        super(Parameters, self).__init__('',children, leaf)

    def print_children(self, level):
        return ', '.join(self.children)

    def __repr__(self, level=0):
        return self.print_children(level)

class CaseParameters(Parameters):
    def __init__(self,children=[], leaf=None):
        super(CaseParameters, self).__init__(children, leaf)

    def print_children(self, level):
        return '[' + ', '.join(self.children) + ']'



class ExprVar(Node):

    _symbols = { '+': 'ADD',
                 '-': 'SUB',
                 '||': 'OR',
                 '==': 'EQ',
                 '&&': 'AND',
                 '*' : 'MUL',
                 '/' : 'DIV',
                 '%' : 'MOD',
                 '!=' : 'NE',
                 '<' : 'LT',
                 '<=': 'LE',
                 '>=': 'GE',
                 '>' : 'GT'}

    def __init__(self, type='ExprVar', children=[], leaf=None):
        super(ExprVar, self).__init__(type,[], self._symbols[leaf] if self._symbols.has_key(leaf) else leaf)

class ExprUnop(ExprVar):
    _symbols = { '!': 'NOT',
                 '-': 'UMINUS',
                 'unsafePrintInt': 'unsafePrintInt',
                 'unsafePrintChar': 'unsafePrintChar'}

class ExprConstructor(ExprVar):
    def __init__(self,children=[], leaf=None):
        super(ExprConstructor, self).__init__('ExprConstructor', children, leaf)

class ExprLambda(Node):
    def __init__(self,type='', children=[], leaf=None, parameters=[], expr=None):
        self.parameters = parameters
        self.expr = expr
        super(ExprLambda, self).__init__(type, children, leaf)

    def transform(self):
        if len(self.parameters) > 0:
            #Genero los hijos recursivamente
            self.children = [ExprLambda(leaf=self.parameters[0], type='ExprLambda', parameters=self.parameters[1:], expr=self.expr)]
        else:
            #Soy el ultimo
            self.children = [self.expr]

    def print_children(self, level):
        ret = ''
        for child in self.children:
            if child:
                ret += child.repr(level+1)
        return ret

    def __repr__(self, level=0):
        ret = ''
        if self.type:
            ret = ' '*level+ '['
            ret += self.print_type(level)
            ret += '\n'
            ret +=    self.print_children(level)
            ret += " "*level+ "], \n"
        else:
            ret += self.print_children(level)
        return ret

    def print_type(self, level=0):
        if self.type:
            return '"' +str(self.type)+'", ' + self.print_leaf(level)
        else:
            return ''

    def print_leaf(self, level=0):
        return '"' + str(self.leaf) + '",'

class ExprString(ExprLambda):
    def __init__(self,type='', children=[], leaf=None, parameters='', parent=False):
        self.parent=parent
        super(ExprString, self).__init__('ExprApply', children, '', parameters.replace('"', ''), None)

    def transform(self):
        if len(self.parameters) >= 1:
            #Genero los hijos recursivamente
            str = ExprString(children=[ExprString(children=[ExprConstructor(leaf="Cons"),
                                                                            ExprChar(leaf=self.parameters[0])])],
                                            parameters=self.parameters[1:])
            self.children.append(str)
        #Cuando llego al ultimo, agrego Nil a mis hijos
            if len(self.parameters) == 1:
                nil = ExprConstructor(leaf="Nil")
                str.children.append(nil)

    def print_leaf(self, level=0):
        return ''

    def print_children(self, level):
        ret = ''
        for child in self.children:
            if child:
                ret += child.repr(level+1)
        return ret

    def __repr__(self, level=0):
        ret = ''
        if self.type and not self.parent:
            ret = ' '*level+ '['
            ret += self.print_type(level)
            ret += '\n'
            ret +=    self.print_children(level)
            ret += " "*level+ "], \n"
        else:
            ret += self.print_children(level)
        return ret

class ExprChar(Node):
    def __init__(self,children=[], leaf=None):
        super(ExprChar, self).__init__('ExprChar', children, leaf)

    def print_leaf(self, level):
        import codecs
        result = ''
        if self.leaf:
            string = self.leaf.replace("'", '', 2)
            try:
                decoded = codecs.decode(string, 'unicode_escape')
            except UnicodeDecodeError:
                #Python no permite que un string termine con un numero par de contrabarras
                decoded = string
            result += str(ord(decoded)) + '],'
        return result
