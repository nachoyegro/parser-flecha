#!/usr/bin/python
import sys
sys.path.append("../..")

import ply.yacc as yacc
from lexer import *
from ast import *


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
#
def p_error(parser):
    if parser:
       print("Syntax error at token", parser.type)
    else:
       print("Syntax error at EOF")

def p_program(p):
    ''' program : not_empty
                | empty '''
    p[0]=p[1]

def p_not_empty(p):
    ''' not_empty : program definition '''
    p[0] = p[1].add_child(p[2])

def p_empty(p):
    ''' empty : '''
    p[0]=Program(children=[])

#TODO: faltan los parametros
def p_definition(p):
    '''definition : DEF LOWERID parameters DEFEQ expression'''
    p[0]=Def(leaf=p[2], children=[p[3], p[5]])

def p_parameters(p):
    '''parameters : empty
                  | LOWERID parameters'''
    if len(p) == 3:
        p[0]=p[2].add_child(p[1])
    else:
        p[0]=Parameters(children=[])

#TODO: escribir en terminos de LET
def p_expression(p):
    '''expression : externexp
                  | externexp SEMICOLON expression'''
    if len(p) > 2:
        p[0]=[p[1], ';', p[3]]
    else:
        p[0]=p[1]

#TODO: en realidad no deberia ser apply
def p_externexp(p):
    '''externexp : ifexp
                 | caseexp
                 | letexp
                 | lambdaexp
                 | internexp'''
    p[0]=p[1]

def p_ifexp(p):
    '''ifexp : IF internexp THEN internexp elsebranch'''
    p[0]=ExprCase(children=[p[2], [CaseBranch(leaf=["True", []], children=[p[4]]), CaseBranch(leaf=["False", []], children=[p[5]])]])

def p_elsebranch(p):
    '''elsebranch : ELIF internexp THEN internexp elsebranch
                  | ELSE internexp'''
    if len(p) == 3:
        p[0]=p[2]
    else:
        p[0]=ExprCase(children=[p[2], [CaseBranch(leaf=["True", []], children=[p[4]]), CaseBranch(leaf=["False", []], children=[p[5]])]])

def p_caseexp(p):
    '''caseexp : CASE internexp casebranches'''
    p[0]=ExprCase(children=[p[2], p[3]])

def p_casebranches(p):
    '''casebranches : empty
                    | casebranch casebranches'''
    if len(p)==3:
        p[0]=ExprCase(children=[p[1],p[2]])
    else:
        p[0]=[]

def p_casebranch(p):
    '''casebranch : PIPE exprVar parameters ARROW internexp'''
    p[0]=CaseBranch(leaf=[p[2], p[3]], children=[p[5]])

def p_letexp(p):
    '''letexp : LET lower parameters DEFEQ internexp IN externexp'''
    p[0] = ExprLet(leaf=[p[2], p[3]], children=[p[5], p[7]])

def p_lambdaexp(p):
    '''lambdaexp : LAMBDA lambdaParams ARROW externexp'''
    p[0] = ExprLambda(parameters=p[2], children=[], expr=p[4])

def p_lambdaParams(p):
    '''lambdaParams : LOWERID lambdaParams
                    | empty'''
    if len(p) > 2:
        p[0]=[p[1]] + p[2]
    else:
        p[0]=[]

def p_internexp(p):
    '''internexp : appexp
                 | internexp binop internexp
                 | unop internexp'''
    if len(p) == 2:
        p[0]=p[1]
    elif len(p) == 3:
        p[0]=['unop', p[2]]
    else:
        p[0]=ExprApply(children=[p[2], p[1], p[3]])

def p_unop(p):
    '''unop : NOT
            | UMINUS'''
    p[0]=p[1]

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
    p[0]=ExprVar(leaf=p[1])

def p_appexp(p):
    '''appexp : atomexp
             | appexp atomexp'''
    if len(p) == 2:
        p[0]=p[1]
    else:
        p[0]=ExprApply(children=[p[1], p[2]])

def p_atomexp(parser):
    '''atomexp : exprNumber
               | exprVar
               | exprChar
               | exprString
               | LPAREN expression RPAREN'''
    if len(parser)==3:
        parser[0]=['(', parser[2], ')']
    else:
        parser[0]=parser[1]

def p_exprChar(p):
    '''exprChar : CHAR'''
    p[0]=ExprChar(leaf=p[1])

def p_exprNumber(p):
    '''exprNumber : NUM'''
    p[0]=ExprNumber(leaf=p[1])

def p_exprString(p):
    '''exprString : STRING'''
    p[0]=ExprString(leaf=p[1])

def p_exprVar(p):
    '''exprVar : upper
               | lower'''
    p[0]=p[1]

def p_upper(p):
    '''upper : UPPERID'''
    p[0]=ExprConstructor(leaf=p[1])

def p_lower(p):
    '''lower : LOWERID'''
    p[0]=ExprVar(leaf=p[1])

def get_parser():
    return yacc.yacc()
