#!/usr/bin/python
import sys
sys.path.append("../..")

import ply.yacc as yacc
from flecha.lexer import *


############################################################################

# Precedencia
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('right', 'NOT'),
    ('left','EQ','NE', 'GE', 'LE', 'GT', 'LT',),
    ('left','PLUS','SUB'),
    ('left','TIMES'),
    ('left','DIV', 'MOD'),
    ('right','UMINUS'),
    )

#################################################################
#definiciones
def p_empty(p):
    ''' empty : '''
    p[0] = []

def p_program(p):
    '''program : empty
             | program definition'''
    p[0]=p[1]

def p_definition(p):
    '''definition : DEF LOWERID parameters DEFEQ expression'''
    p[0]=p[1]

def p_parameters(p):
    '''parameters : empty
                  | LOWERID parameters'''
    p[0] = p[1]

def p_expression(p):
    '''expression : externexp
                  | externexp SEMICOLON expression'''
    pass

def p_externexp(p):
    '''externexp : ifexp
                 | caseexp
                 | letexp
                 | lambdaexp
                 | internexp'''
    pass

def p_ifexp(p):
    '''ifexp : IF internexp THEN internexp elsebranch'''
    pass

def p_elsebranch(p):
    '''elsebranch : ELIF internexp THEN internexp elsebranch
                  | ELSE internexp'''
    pass

def p_caseexp(p):
    '''caseexp : CASE internexp casebranches'''
    pass

def p_casebranches(p):
    '''casebranches : empty
                    | casebranch casebranches'''
    pass

def p_casebranch(p):
    '''casebranch : PIPE UPPERID parameters ARROW internexp'''
    pass

def p_letexp(p):
    '''letexp : LET ID parameters DEFEQ internexp IN externexp'''
    pass

def p_lambdaexp(p):
    '''lambdaexp : LAMBDA parameters ARROW externexp'''
    pass

def p_internexp(p):
    '''internexp : appexp
                 | internexp binop internexp
                 | unop internexp'''
    pass

def p_unop(p):
    '''unop : NOT
            | UMINUS'''
    pass

def p_binop(p):
    '''binop : AND
            | OR
            | EQ
            | NE
            | GE
            | LE
            | GT
            | LT
            | PLUS
            | SUB
            | TIMES
            | DIV
            | MOD'''
    pass

def p_appexp(p):
    '''appexp : atomexp
             | appexp atomexp'''
    pass

def p_atomexp(p):
    '''atomexp : LOWERID
               | UPPERID
               | NUM
               | STRING
               | LPAREN expression RPAREN'''
    pass

def get_parser():
    return yacc.yacc()
