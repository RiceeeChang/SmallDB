#---------------------------------------
#
# SqlYacc.py - small DB yacc
#
#---------------------------------------
import ply.yacc as yacc

from SqlProcess import Relation, Table

# Get the token map from the lexer. This is required
from SqlLex import tokens

start = 'command'


# Command State
# cmd --- command mode
# rel --- relation mode
global state
state = 'cmd'

# Relation and Table dictionary to collect used relation and table
global temp_rel
relation = {}
table    = {}

def p_command(p):
    '''command : define_cmd
               | set_cmd
               | create_cmd
               | insert_cmd
               | delete_cmd
               | update_cmd
               | select_cmd'''

def p_define_cmd(p):
    # define relation <relation_name>
    'define_cmd : DEFINE RELATION WORD'
    global state
    global temp_rel
    if state is 'cmd':
        temp_rel = Relation(p[3])
        state = 'rel'
        print(temp_rel.name)

def p_set_cmd(p):
    # set attribute character <char_number> <attribute_name>
    # set attribute integer <attribute_name> range <front_number> <rear_number>
    # set attribute integer <attribute_name>
    # set primary key <attribute_name>
    '''set_cmd : SET ATTRIBUTE CHARACTER NUMBER WORD
           | SET ATTRIBUTE INTEGER WORD RANGE NUMBER NUMBER
           | SET ATTRIBUTE INTEGER WORD
           | SET PRIMARY KEY  WORD'''
    global state
    global temp_rel
    print(len(p))
    if state is 'rel':
        if p[3] is 'character':
            temp_rel.attribute.append((p[4], p[3], p[5]))
        elif p[3] is 'integer':
            if len(p) is 5:
                temp_rel.attribute.append((p[4], p[3]))
            elif len(p) is 8:
                temp_rel.attribute.appedn((p[4], p[3], p[5], p[6]))
        elif p[3] is 'key':
            temp_rel.setPrimary_key(p[4])
            relation.update({temp_rel.name : temp_rel})
            state = 'cmd'


def p_create_cmd(p):
    # create table <relation_name> <table_name>
    'create_cmd : CREATE TABLE WORD WORD'
    table.update({p[4] : Table(relation[p[3]], p[4])})

    
def p_insert_cmd(p):
    # insert <table_name> (<attribute_value>)+
    'insert_cmd : INSERT WORD attribute_expr'
    table[p[2]].addElement(p[3])

def p_attribute_expr(p):
    # <attribute_value> <attribute_expr>
    '''attribute_expr : WORD attribute_expr
                      | NUMBER attribute_expr
                      | WORD
                      | NUMBER'''
    if len(p) is 2:
        p[0] = (p[1],)
    elif len(p) is 3:
        p[0] = (p[1],) + p[2]

def p_delete_cmd(p):
    # delete <table_name> <primary_key_value>
    'delete_cmd : DELETE WORD NUMBER'
    table[p[2]].delElement(p[3])


def p_update_cmd(p):
    # update <table_name> <primary_key_value> (<attribute_value>)+
    'update_cmd : UPDATE WORD NUMBER attribute_expr'
    table[p[2]].update(p[3], p[4])


def p_select_cmd(p):
    # select <attribute_name> from <table_name> where <expr>
    'select_cmd : SELECT WORD FROM WORD WHERE expr'
    temp_table = table[p[4]]
    if   p[6][1] is '=':
        for element in temp_table.element:
            if element[p[6][0]] is p[6][2]:
                print(element[p[2]])
    elif p[6][1] is '>':
        for element in temp_table.element:
            if element[p[6][0]] > p[6][2]:
                print(element[p[2]])
    elif p[6][1] is '<':
        for element in temp_table.element:
            if element[p[6][0]] < p[6][2]:
                print(element[p[2]])

def p_expr(p):
    # <attribute_name> [=|>|<] <value>
    '''expr : WORD EQUAL NUMBER
          | WORD GREATER NUMBER
          | WORD LESS NUMBER'''
    p[0] = (p[1], p[2], p[3])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in " + p.value)

# Build the parser
parser = yacc.yacc()


while True:
    try:
        s = input('parser > ')
    except EOFError:
        break

    if not s: continue
    result = parser.parse(s)
    print(result)
