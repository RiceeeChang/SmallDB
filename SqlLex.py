#-----------------------------------------
#
# SqlLex.py - a lexer for small database
#
#-----------------------------------------
import ply.lex as lex


# List of token names. This is always required
reserved = {
    'define' : 'DEFINE',
    'relation'  : 'RELATION',
    'attribute' : 'ATTRIBUTE',
    'set'       : 'SET',
    'primary'   : 'PRIMARY',
    'key'       : 'KEY',
    'create'    : 'CREATE',
    'table'     : 'TABLE',
    'insert'    : 'INSERT',
    'delete'    : 'DELETE',
    'update'    : 'UPDATE',
    'select'    : 'SELECT',
    'from'      : 'FROM',
    'where'     : 'WHERE',
    'integer'   : 'INTEGER',
    'character' : 'CHARACTER',
    'range'     : 'RANGE'
}

tokens = list(reserved.values()) + [
    'EQUAL',
    'GREATER',
    'LESS',
    'WORD',
    'NUMBER'
]

# Regular expression rules for simple tokens
t_EQUAL     = r'='
t_GREATER   = r'>'
t_LESS      = r'<'

# Identifiers and reserved words
#reserved_map = {}
#for r in reserved:
#    reserved_map[r.lower()] = r

def t_WORD(t):
    r'[A-Za-z][\w_]*'
    t.type = reserved.get(t.value, "WORD")
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters(spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character" + t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()



# Test it out 
#data = 'select SPOINT2 from STUDENT_DB where SPOINT1<70'

# Give the lexer some input
#lexer.input(data)

#Tokenize
#while True:
#    tok = lexer.token()
#    if not tok: break  # No more input
#    print(tok)
