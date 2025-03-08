import ply.lex as lex

# Updated tokens list including DOT and CALL
tokens = (
    'VAR', 'NUMBER', 'STRING', 'ASSIGN',
    'PLUS', 'MINUS', 'MULT', 'DIV',
    'EQUAL', 'LT', 'GT', 'LE', 'GE', 'NE',
    'IF', 'ELSE', 'FOR', 'WHILE',
    'PRINT', 'INPUT', 'RETURN',
    'SWITCH', 'CASE', 'BREAK', 'DEFAULT',
    'FUNCTION', 'CLASS', 'OBJECT',
    'OPEN_PAREN', 'CLOSE_PAREN', 'OPEN_BRACE', 'CLOSE_BRACE',
    'SEMICOLON', 'COMMA', 'DOT', 'CALL'
)

# Token definitions using string literals
t_ASSIGN    = r'='
t_PLUS      = r'➕'
t_MINUS     = r'➖'
t_MULT      = r'✖️'
t_DIV       = r'➗'
t_EQUAL     = r'🟰'
t_LT        = r'📉'
t_GT        = r'📈'
t_LE        = r'📉🟰'
t_GE        = r'📈🟰'
t_NE        = r'🚫🟰'

t_IF        = r'🤔'
t_ELSE      = r'🔄'
t_FOR       = r'➿'
t_WHILE     = r'🔁'
t_PRINT     = r'🖨️'
t_INPUT     = r'📥'
t_RETURN    = r'🔙'
t_SWITCH    = r'🔀'
t_CASE      = r'🔂'
t_BREAK     = r'❌'
t_DEFAULT   = r'🚪'
t_FUNCTION  = r'🎭'
t_CLASS     = r'🏛'
t_OBJECT    = r'🎭'

t_OPEN_PAREN  = r'\('
t_CLOSE_PAREN = r'\)'
t_OPEN_BRACE  = r'\{'
t_CLOSE_BRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA     = r','

# New tokens:
t_DOT = r'\.'
t_CALL = r'call'

# Reserve the keyword "call" in the VAR rule.
reserved = {
    "call": "CALL"
}

def t_VAR(t):
    r'[😀🔥💰🔧🚗🚦a-zA-Z][😀🔥💰🔧🚗📜🚦a-zA-Z0-9]*'
    t.type = reserved.get(t.value, "VAR")
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
