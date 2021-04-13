import re
import sys

token = ''
string = ""
index = 0

def getToken():
    global index
    global string
    global token

    index += 1
    if index >= len(string):
        error("overflow")
    else:
        token = string[index]
        print(token)

def error(expected = ""):

    print("INVALID!")
    if expected != "":
        print("Error: "+expected+" expected, got \""+token+"\".")
    quit()
"""
TOKENS
"""
def is_Int():
    pattern = "[0-9]+"
    return re.match(pattern, token) != None

def is_Dec():
    pattern = "[0-9]+\.[0-9]+"
    return re.match(pattern, token) != None

def is_String():
    pattern = "\".*\""
    return re.match(pattern, token) != None

def is_Keyword():
    return token in [":=", "+", "-", "*", "/", "OR", "AND", "~", "(", ")", "<", ">", "=", "#", ";", "PRINT", "IF", "ELSE", "ENDIF", "WHILE", "ENDW", "PROC", "RETURN", "BEGIN", "END."]

def is_Ident():
    pattern = "([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*"
    return re.match(pattern, token)!= None and token not in [":=", "+", "-", "*", "/", "OR", "AND", "~", "(", ")", "<", ">", "=", "#", ";", "PRINT", "IF", "ELSE", "ENDIF", "WHILE", "ENDW", "PROC", "RETURN", "BEGIN", "END."]
"""
OPERATORS:
"""
def is_Relation():
    return token in ['<', '>', '=', '#']

def is_AddOperator():
    return token in ['+', '-', 'OR']

def is_MulOperator():
    return token in ['*', '/', 'AND']

"""
EXPRESSIONS/FACTORS
"""
def is_Expr():
    is_Simple_Expr()
    if is_Relation():
        is_Simple_Expr()
    return

def is_Simple_Expr():
    is_Term()
    if is_AddOperator():
        is_Simple_Expr()
    return

def is_Term():
    is_Factor()
    if is_MulOperator():
        is_Term()
    return

def is_Factor():
    getToken()
    if is_Int() or is_Dec() or is_String() or is_Ident():
        getToken()
    elif token == '~':
        getToken()
        is_Factor()
    elif token == '(':
        is_Expr()
        getToken()
        if token == ')':
            getToken()
    else:
        error("Int, Decimal, String, or Identifier")
    return
"""
ASSIGNMENT/STATEMENTS
(do not call anything but is_(RetStatement, Statement() or StatementSequence()))
"""
def is_Assignment():
    if is_Ident():
        getToken()
        if token == ":=":
            is_Expr()
        else:
            error(":=")
    else:
        error("Identifier")
    return

def is_PrintStatement():
    if token == "PRINT":
        getToken()
        if token == '(':
            is_Expr()
            if token == ')':
                getToken()
            else:
                error(")")
        else:
            error("(")
    else:
        error("PRINT")
    return

def is_RetStatement():
    if token == "RETURN":
        getToken()
        if is_Ident():
            getToken()
        else:
            error("Identifier")
    else:
        error("RETURN")
    return

def is_IfStatement():
    getToken()
    if token == '(':
        is_Expr()
        if token == ')':
            is_StatementSequence()
            if token == "ELSE":
                is_StatementSequence()
            if token == "ENDIF":
                getToken()
            else:
                error("ENDIF")
        else:
            error("Statement")
    else:
        error("(")
    return

def is_WhileStatement():
    getToken()
    if token == '(':
        is_Expr()
        if token == ')':
            is_StatementSequence()
            if token != "ENDW":
                error("ENDW")
            else:
                getToken()
        else:
            error("Expression")
    else:
        error("(")
    return

def is_Statement():
    getToken()
    if is_Ident():
        is_Assignment()
    elif token == "PRINT":
        is_PrintStatement()
    elif token == "IF":
        is_IfStatement()
    elif token == "WHILE":
        is_WhileStatement()
    else:
        error("Statement")
    return

def is_StatementSequence():
    is_Statement()
    if token == ';':
        is_StatementSequence()

"""
OTHER SEQUENCES:
"""
def is_ParamSequence():
    if is_Ident():
        getToken()
        if token == ',':
            getToken()
            is_ParamSequence()
    else:
        error("Identifier")
    return

def is_FunctionDeclaration():
    if token == "PROC":
        getToken()
        if is_Ident():
            getToken()
            if token == '(':
                getToken()
                if is_Ident():
                    is_ParamSequence()
                if token == ')':
                    getToken()
                else:
                    error("Identifier")
                if token == "BEGIN":
                    is_StatementSequence()
                    if token == "RETURN":
                        is_RetStatement()
                    if token == "END.":
                        getToken()
                    else:
                        error("END.")
                else:
                    error("BEGIN")
            else:
                error("(")
        else:
            error("Identifier")
    else:
        error("PROC")
    return

def is_FunctionSequence():
    is_FunctionDeclaration()
    print("token:", token)
    if token == "PROC":
        is_FunctionSequence()
    return

def Initialize():
    global index
    global string
    inp = sys.stdin.read()
    string = inp.split()
    string += '$'
    index = -1
    print(string)
    getToken()


Initialize()
is_FunctionSequence()
if token == '$':
    print("CORRECT")
else:
    print("INVALID!")
