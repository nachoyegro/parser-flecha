

class FlechaCompiler(object):

    def __init__(self, program):
        self.program = program
        self.last_registry = None
        self.registers = {'$r0': False, '$r1': False, '$r2': False,
                          '$r3': False, '$r4': False, '$r5': False,
                          '$r6': False, '$r7': False, '$r8': False,
                          '$r9': False, }

    def compile(self):
        for definition in self.program:
            #Por ahora no soporta parametros
            name = definition[1]
            expression = definition[2]
            res = self.compile_expression(expression)
            registry = self.last_registry
            function_reg = '@G_' + name
            res += self.mov_reg(function_reg, registry)
            print(res)

    def compile_ExprNumber(self, num):
        res = ''
        registry = self.next_registry()
        res += self.alloc(registry, 2) + '\n'                 #Reservo 2 celdas
        temp_registry = self.next_registry()                  #Traigo el proximo registro disponible
        res += self.mov_int(temp_registry, 1) + '\n'          #Pongo el numero 1, correspondiente a enteros
        res += self.store(registry, 0, temp_registry) + '\n'  #Pongo en la celda 0 de registry el numero 1
        res += self.mov_int(temp_registry, num[0]) + '\n'    #Pongo el numero que representa el char en el registro temporal
        res += self.store(registry, 1, temp_registry) + '\n'  #Pongo en la celda 1 de registry el valor de temp
        self.free_registry(temp_registry)                     #Libero el registro temp
        self.last_registry = registry
        return res

    def compile_ExprVar(self, expression):
        # ['unsafePrintChar']
        res = ''
        temp_registry = self.next_registry()
        registry = self.last_registry
        res += self.load(temp_registry, registry, 1) + '\n'   #Pongo en temp_registry el valor que hay en la posicion 1 de registry
        res += self.print_char(temp_registry) + '\n'          #Hago print
        self.free_registry(temp_registry)
        return res

    def compile_ExprChar(self, char):
        res = ''
        registry = self.next_registry()
        res += self.alloc(registry, 2) + '\n'                 #Reservo 2 celdas
        temp_registry = self.next_registry()                  #Traigo el proximo registro disponible
        res += self.mov_int(temp_registry, 2) + '\n'          #Pongo el numero 2, correspondiente a chars #TODO: no necesito hacer alloc?
        res += self.store(registry, 0, temp_registry) + '\n'  #Pongo en la celda 0 de registry el numero 2
        res += self.mov_int(temp_registry, char[0]) + '\n'    #Pongo el numero que representa el char en el registro temporal
        res += self.store(registry, 1, temp_registry) + '\n'  #Pongo en la celda 1 de registry el valor de temp
        self.free_registry(temp_registry)                     #Libero el registro temp
        self.last_registry = registry
        return res


    def compile_expression(self, expression):
        # ['ExprApply', [e], [e]]
        # ['ExprChar', 97]
        # ['ExprVar', 'UMINUS']
        function = expression[0]
        children = expression[1:]
        method_to_call = getattr(self, 'compile_'+function)
        return method_to_call(children)


    def compile_ExprApply(self, children):
        #Primero compilo children[1:] y despues children[0]
        #Al parecer, los apply siempre vienen con una parte
        res1 = self.compile_expression(children[1])
        res0 = self.compile_expression(children[0])
        return res1 + res0

    def next_registry(self):
        for key, value in sorted(self.registers.iteritems()):
            if not value:
                self.registers[key] = True
                return key

    def last_registry(self):
        return self.last_registry

    def free_registry(self, registry):
        self.registers[registry] = False

    def alloc(self, reg, cant):
        return 'alloc(%s, %d)' % (reg, cant)

    def load(self, reg_d, reg_o, int):
        return 'load(%s, %s, %d)' % (reg_d, reg_o, int)

    def mov_int(self, reg, int):
        return 'mov_int(%s, %d)' % (reg, int)

    def mov_reg(self, function, registry):
        return 'mov_reg %s %s' % (function, registry)

    def store(self, reg_d, slot, reg_o):
        return 'store(%s, %d, %s)' % (reg_d, slot, reg_o)

    def print_char(self, registry):
        return 'print_char(%s)' % registry
