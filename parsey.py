import ply.yacc as yacc
from lexy import tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('left', 'GT', 'LT', 'EQUAL', 'LE', 'GE', 'NE'),
)

def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

def p_statement_list_multiple(p):
    '''statement_list : statement_list statement'''
    p[0] = p[1] + [p[2]]

def p_statement_list_single(p):
    '''statement_list : statement'''
    p[0] = [p[1]]

def p_statement_class(p):
    '''statement : CLASS VAR OPEN_BRACE statement_list CLOSE_BRACE'''
    p[0] = ('class_def', p[2], p[4])

def p_statement_function(p):
    '''statement : FUNCTION VAR OPEN_PAREN parameter_list CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE'''
    p[0] = ('function_def', p[2], p[4], p[7])

def p_parameter_list_multiple(p):
    '''parameter_list : parameter_list COMMA VAR'''
    p[0] = p[1] + [p[3]]

def p_parameter_list_single(p):
    '''parameter_list : VAR'''
    p[0] = [p[1]]

def p_parameter_list_empty(p):
    '''parameter_list : '''
    p[0] = []

def p_statement_assign(p):
    '''statement : VAR ASSIGN expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])

def p_statement_print(p):
    '''statement : PRINT OPEN_PAREN expression CLOSE_PAREN SEMICOLON'''
    p[0] = ('print', p[3])

def p_statement_return(p):
    '''statement : RETURN expression SEMICOLON'''
    p[0] = ('return', p[2])

def p_statement_if_else(p):
    '''statement : IF OPEN_PAREN expression CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE ELSE OPEN_BRACE statement_list CLOSE_BRACE'''
    p[0] = ('if_else', p[3], p[6], p[10])

def p_statement_if(p):
    '''statement : IF OPEN_PAREN expression CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE'''
    p[0] = ('if', p[3], p[6])

# Call statement grammar
def p_statement_call(p):
    '''statement : CALL call_expr SEMICOLON'''
    p[0] = ('call', p[2])

def p_call_expr_method(p):
    '''call_expr : VAR DOT VAR'''
    p[0] = ('call_method', p[1], p[3], [])

def p_call_expr_method_args(p):
    '''call_expr : VAR DOT VAR OPEN_PAREN arg_list CLOSE_PAREN'''
    p[0] = ('call_method', p[1], p[3], p[5])

def p_call_expr_function(p):
    '''call_expr : VAR OPEN_PAREN arg_list CLOSE_PAREN'''
    p[0] = ('call_function', p[1], p[3])

def p_call_expr_function_empty(p):
    '''call_expr : VAR OPEN_PAREN CLOSE_PAREN'''
    p[0] = ('call_function', p[1], [])

def p_arg_list_multiple(p):
    '''arg_list : arg_list COMMA expression'''
    p[0] = p[1] + [p[3]]

def p_arg_list_single(p):
    '''arg_list : expression'''
    p[0] = [p[1]]

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIV expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_relop(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression EQUAL expression
                  | expression LE expression
                  | expression GE expression
                  | expression NE expression'''
    p[0] = ('relop', p[2], p[1], p[3])

def p_expression_group(p):
    '''expression : OPEN_PAREN expression CLOSE_PAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ('number', p[1])

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = ('string', p[1])

def p_expression_var(p):
    '''expression : VAR'''
    p[0] = ('var', p[1])

def p_error(p):
    if p:
        print("Syntax error at token:", p.type, "with value:", p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()
