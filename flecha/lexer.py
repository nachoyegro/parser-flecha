import ply.lex as lex

reserved = {
    'def': 'DEF',
    'if' : 'IF',
    'then': 'THEN',
    'elif': 'ELIF',
    'else': 'ELSE',
    'case': 'CASE',
    'let': 'LET',
    'in' : 'IN',
}



tokens = [
    'ID', #strings
    'LOWERID',
    'UPPERID',
    'NUM',
    'CHAR',
    'STRING',
    #Delimitadores
    'DEFEQ',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
    'LAMBDA',
    'PIPE',
    'ARROW',
    #Operadores Logicos
    'AND',
    'OR',
    'NOT',
    #Operadores Racionales
    'EQ',
    'NE',
    'GE',
    'LE',
    'GT',
    'LT',
    #Operadores aritmeticos
    'PLUS',
    'SUB',
    'TIMES',
    'DIV',
    'MOD',
    'UMINUS',
    ] + list(reserved.values())

# Tokens
t_ID              = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LOWERID         = r'[a-z][a-zA-Z0-9_]*'
t_UPPERID         = r'[A-Z][a-zA-Z0-9_]*'
t_STRING          = r'("[^"]*")'

t_DEFEQ           = r'='
t_SEMICOLON       = r';'
t_LPAREN          = r'\('
t_RPAREN          = r'\)'
t_LAMBDA          = r'\\'
t_PIPE            = r'\|'
t_ARROW           = r'->'

t_AND             = r'&&'
t_OR              = r'\|\|'
t_NOT             = r'!'

t_EQ              = r'=='
t_NE              = r'!='
t_GE              = r'>='
t_LE              = r'<='
t_GT              = r'>'
t_LT              = r'<'

t_PLUS            = r'\+'
t_SUB             = r'-'
t_UMINUS          = r'-'
t_TIMES           = r'\*'
t_DIV             = r'\/'
t_MOD             = r'%'

t_ignore = ' '

def t_NUM(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
    t.value = 0
    return t # Ignored characters t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.skip(1)

def t_COMMENT(t):
    r'\--.*'
    pass
    # No return value. Token discarded

lexer = lex.lex(debug=1)
