reserved_vars = ['unsafePrintInt', 'unsafePrintChar']
constructors = {'True': 4, 'False': 5, 'Nil': 6, 'Cons': 7}

class FlechaCompiler(object):

    def __init__(self, program):
        self.program = program
        self.last_registry = None
        self.register_count = 0
        self.registers = {}
        self.global_env = {}
        self.loaded = {}

    def compile(self):
        for definition in self.program:
            #Por ahora no soporta parametros
            env = {}
            name = definition[1]
            expression = definition[2]
            res, env = self.compile_expression(expression, env)
            registry = self.last_registry
            function_reg = '@G_' + name
            res += self.mov_reg(function_reg, registry)
            self.last_registry = function_reg
            self.global_env[function_reg] = registry
            print(res)

    def compile_ExprVar(self, expression, env, reg=None):
        # ['unsafePrintChar']
        res = ''
        #Si lo que viene es unsafePrintInt, por ejemplo
        if expression[0] in reserved_vars:
            registry = self.last_registry
            if '@' in registry:
                #Chequeo si el registro esta en el entorno local
                if registry in env.keys():
                    temp_registry = env[registry]
                    res += self.mov_reg(registry, temp_registry) + '\n'
                    res += self.load(temp_registry, registry, 1) + '\n'   #Pongo en temp_registry el valor que hay en la posicion 1 de registry
                #Sino, chequeo si esta en el entorno global
                elif registry in self.global_env.keys():
                    temp_registry = self.global_env[registry]
                    res += self.mov_reg(registry, temp_registry) + '\n'
                    #Chequeo que no haya sido cargado ya
                    if temp_registry not in self.loaded.keys():
                        res += self.load(temp_registry, registry, 1) + '\n'   #Pongo en temp_registry el valor que hay en la posicion 1 de registry
                        self.loaded[temp_registry] = True
                #Sino, lo agrego al entorno local
                else:
                    temp_registry = self.next_registry()
                    env[registry] = temp_registry
                    res += self.mov_reg(temp_registry, registry) + '\n'
                    res += self.load(temp_registry, registry, 1) + '\n'   #Pongo en temp_registry el valor que hay en la posicion 1 de registry
            else:
                temp_registry = self.next_registry()
                res += self.load(temp_registry, registry, 1) + '\n'   #Pongo en temp_registry el valor que hay en la posicion 1 de registry
            #TODO: En el caso que @G_foo este en el entorno global no deberia hacer load

            res += self.unsafe_print(temp_registry, expression[0]) + '\n'          #Hago print
        else:
            global_registry = '@G_' + expression[0]
            self.last_registry = global_registry
        return res, env

    def compile_ExprChar(self, char, env, reg=None):
        res = ''
        registry = self.next_registry()
        res += self.alloc(registry, 2) + '\n'                 #Reservo 2 celdas
        temp_registry = self.next_registry()                  #Traigo el proximo registro disponible
        res += self.mov_int(temp_registry, 2) + '\n'          #Pongo el numero 2, correspondiente a chars #TODO: no necesito hacer alloc?
        res += self.store(registry, 0, temp_registry) + '\n'  #Pongo en la celda 0 de registry el numero 2
        res += self.mov_int(temp_registry, char[0]) + '\n'    #Pongo el numero que representa el char en el registro temporal
        res += self.store(registry, 1, temp_registry) + '\n'  #Pongo en la celda 1 de registry el valor de temp
        #self.free_registry(temp_registry)                     #Libero el registro temp
        self.last_registry = registry
        return res, env

    def compile_ExprNumber(self, num, env, reg=None):
        res = ''
        registry = self.next_registry()
        res += self.alloc(registry, 2) + '\n'                 #Reservo 2 celdas
        temp_registry = self.next_registry()                  #Traigo el proximo registro disponible
        res += self.mov_int(temp_registry, 1) + '\n'          #Pongo el numero 1, correspondiente a enteros
        res += self.store(registry, 0, temp_registry) + '\n'  #Pongo en la celda 0 de registry el numero 1
        res += self.mov_int(temp_registry, num[0]) + '\n'     #Pongo el numero que representa el char en el registro temporal
        res += self.store(registry, 1, temp_registry) + '\n'  #Pongo en la celda 1 de registry el valor de temp
        self.last_registry = registry
        return res, env

    def compile_ExprConstructor(self, cons, env, reg=None):
        res = ''
        registry = self.next_registry()
        res += self.alloc(registry, 1) + '\n'                 #Reservo 1 celda
        res += self.mov_int('$t', constructors[cons[0]])  + '\n'                  #4 = Tag para el constructor True.
        res += self.store(registry, 0, '$t') + '\n'
        self.last_registry = registry
        return res, env

    def compile_ExprLet(self, children, env, reg=None):
        res = ''
        var = children[0]
        res1, env = self.compile_expression(children[1], env)
        #Agrego el registro al env
        env['@G_'+var] = self.last_registry
        res2, env = self.compile_expression(children[2], env)
        return res + res1 + res2, {}


    def compile_expression(self, expression, env, reg=None):
        # ['ExprApply', [e], [e]]
        # ['ExprChar', 97]
        # ['ExprVar', 'UMINUS']
        function = expression[0]
        children = expression[1:]
        method_to_call = getattr(self, 'compile_'+function)
        return method_to_call(children, env, reg)


    def compile_ExprApply(self, children, env, reg=None):
        #Primero compilo children[1:] y despues children[0]
        #Al parecer, los apply siempre vienen con una parte
        res1, env = self.compile_expression(children[1], env)
        res0, env = self.compile_expression(children[0], env)
        return res1 + res0, env

    def next_registry(self):
        registry = '$r' + str(self.register_count)
        self.register_count += 1
        return registry


    def free_registry(self, registry):
        self.registers[registry] = False

    def alloc(self, reg, cant):
        return 'alloc(%s, %d)' % (reg, cant)

    def load(self, reg_d, reg_o, int):
        return 'load(%s, %s, %d)' % (reg_d, reg_o, int)

    def mov_int(self, reg, int):
        return 'mov_int(%s, %d)' % (reg, int)

    def mov_reg(self, function, registry):
        return 'mov_reg(%s, %s)' % (function, registry)

    def store(self, reg_d, slot, reg_o):
        return 'store(%s, %d, %s)' % (reg_d, slot, reg_o)

    def unsafe_print(self, registry, unsafe):
        if unsafe == 'unsafePrintInt':
            return self.print_int(registry)
        if unsafe == 'unsafePrintChar':
            return self.print_char(registry)

    def print_char(self, registry):
        return 'print_char(%s)' % registry

    def print_int(self, registry):
        return 'print(%s)' % registry
