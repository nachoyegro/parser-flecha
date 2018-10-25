
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

    def print_leaf(self):
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
            string += "  "*level+ "], \n"
        return string

    #TODO: refactorear esto
    def __repr__(self, level=0):
        ret = '  '*level+ '['
        ret += self.print_type(level)
        ret += self.print_leaf()
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
            ret += "  "*level+ "]\n"
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
    def __init__(self,children=[], leaf=None):
        super(CaseBranch, self).__init__('CaseBranch',children, leaf)

    def print_leaf(self):
        string = ''
        if self.leaf:
            for leaf in self.leaf:
                string += repr(leaf) + ', '
        if not self.children:
            string += '],'
        return string

class ExprCase(Node):
    def __init__(self,children=[], leaf=None):
        super(ExprCase, self).__init__('ExprCase',children, leaf)

    def print_children(self, level):
        if not self.children:
            return '[]\n'
        else:
            return super(ExprCase, self).print_children(level)

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


class ExprVar(Node):

    _symbols = { '+': 'ADD',
                 '-': 'SUB',
                 '||': 'OR',
                 '==': 'EQ',
                 '&&': 'AND',
                 '*' : 'MUL',
                 '/' : 'DIV',
                 '%' : 'MOD'}

    def __init__(self, type='ExprVar', children=[], leaf=None):
        super(ExprVar, self).__init__(type,[], self._symbols[leaf] if self._symbols.has_key(leaf) else leaf)

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
            ret += child.repr(level+1)
        return ret

    def __repr__(self, level=0):
        ret = ''
        if self.type:
            ret = '  '*level+ '['
            ret += self.print_type(level)
            ret += '\n'
            ret += self.print_children(level)
            ret += "  "*level+ "], \n"
        else:
            ret += self.print_children(level)
        return ret

    def print_type(self, level=0):
        if self.type:
            return '"' +str(self.type)+'", "' + str(self.leaf) + '",'
        else:
            return ''

class ExprString(Node):
    def __init__(self,children=[], leaf=None):
        super(ExprString, self).__init__('ExprString', children, leaf)

    def print_type(self, level=0):
        return ''

    def transform(self):
        self.leaf = self.leaf.replace('"', '')
        for char in self.leaf:
            self.children.append(ExprChar(leaf=char))

class ExprChar(Node):
    def __init__(self,children=[], leaf=None):
        super(ExprChar, self).__init__('ExprChar', children, leaf)

    def print_leaf(self):
        string = ''
        if self.leaf:
            string += str(ord(self.leaf.replace("'", ''))) + '],'
        return string
