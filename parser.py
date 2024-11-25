import ply.yacc as yacc
from lexer import tokens
from tabla_simbolos import SymbolTable

def p_program(p):
    '''program : statement_list'''
    p.parser.symbol_table = SymbolTable()
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement statement_list
                      | statement'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | if_statement
                 | print_statement'''  
    p[0] = p[1]

def p_declaration(p):
    '''declaration : TYPE ID SEMICOLON
                   | TYPE ID ASSIGN expression SEMICOLON'''
    if len(p) == 4:
        p.parser.symbol_table.add(p[2], p[1])
        p[0] = ('declaration', p[1], p[2])
    elif len(p) == 6:
        p.parser.symbol_table.add(p[2], p[1])
        p[0] = ('declaration_assignment', p[1], p[2], p[4])

def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMICOLON'''
    if not p.parser.symbol_table.exists(p[1]):
        raise SyntaxError(f"Error: La variable '{p[1]}' no ha sido declarada antes de su uso.")
    p[0] = ('assignment', p[1], p[3])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE statement_list RBRACE'''
    if len(p) == 12:
        p[0] = ('if_else', p[3], p[6], p[10])
    else:
        p[0] = ('if', p[3], p[6])

def p_print_statement(p):
    '''print_statement : PRINT LPAREN expression RPAREN SEMICOLON'''
    p[0] = ('print', p[3])

def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term
                  | expression LT term
                  | expression LE term
                  | expression EQ term
                  | expression GT term
                  | expression GE term
                  | expression NE term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary_op', p[2], p[1], p[3])

def p_term(p):
    '''term : factor
            | term MULTIPLY factor
            | term DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary_op', p[2], p[1], p[3])

def p_factor(p):
    '''factor : NUMBER
              | STRING
              | ID'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Error sintáctico: Token inesperado '{p.value}' en la línea {p.lineno}")
    else:
        print("Error sintáctico: Fin de archivo inesperado.")

def build_parser():
    return yacc.yacc()
