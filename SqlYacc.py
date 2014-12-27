#---------------------------------------
#
# SqlYacc.py - small DB yacc
#
#---------------------------------------
import ply.yacc as yacc
import http.client
import sys
import json
import os

from SqlProcess import Relation, Table
import SqlProcess as process

# Get the token map from the lexer. This is required
from SqlLex import tokens
start = 'command'

# Command State
# True --- command mode
# False --- relation mode
isCmdState = True

# Relation and Table dictionary to collect used relation and table
global temp_rel
relation_list = []
with open('Data/relation_list.json', 'r+') as datafile:
    relation_list = json.load(datafile)
    print(relation_list)
table_list = []
with open('Data/table_list.json', 'r+') as datafile:
    table_list = json.load(datafile)
    print(table_list)


# Setting http connection
connection = http.client.HTTPSConnection('localhost')
headers = {'Content-type' : 'application/json'}



def p_command(p):
    '''command : define_cmd
               | set_cmd
               | create_cmd
               | insert_cmd
               | delete_cmd
               | update_cmd
               | select_cmd
               | get_cmd
               | exit_cmd'''

def p_exit_cmd(p):
    # exit database system
    '''exit_cmd : EXIT'''
    sys.exit()

def p_get_cmd(p):
    '''get_cmd : GET TABLE
               | GET RELATION'''

    # check state -----------------------------
    if not isCmdState:
        print('You cannot do this command. plz finish define relation first.')
        return 0

    # Do command ------------------------------
    if p[2] == 'table':
        print(table_list)
        #connection.request('POST', '/markdown', json.dump(table_list), headers)
    elif p[2] == 'relation':
        print(relation_list)
        #connection.request('POST', '/markdown', json.dump(relation_list), headers)
    else:
        print('Error')

def p_define_cmd(p):
    # define relation <relation_name>
    'define_cmd : DEFINE RELATION WORD'
    global temp_rel
    global isCmdState

    # check state
    if not isCmdState:
        print('You cannot do this command. plz finish define relation first.')
        return 0
    
    temp_rel = Relation(p[3])
    isCmdState = False


def p_set_cmd(p):
    # set attribute character <char_number> <attribute_name>
    # set attribute integer <attribute_name> range <front_number> <rear_number>
    # set attribute integer <attribute_name>
    # set primary key <attribute_name>
    '''set_cmd : SET ATTRIBUTE CHARACTER NUMBER WORD
           | SET ATTRIBUTE INTEGER WORD RANGE NUMBER NUMBER
           | SET ATTRIBUTE INTEGER WORD
           | SET PRIMARY KEY  WORD'''
    global isCmdState
    global temp_rel

    # check state -----------------------------
    if isCmdState:
        print('You cannot do this action while not defining a relation.')
        return 0
    
    if p[3] == 'character':
        temp_rel.attribute.append((p[5], p[3], p[4]))
    elif p[3] == 'integer':
        if len(p) is 5:
            temp_rel.attribute.append((p[4], p[3]))
        elif len(p) is 8:
            temp_rel.attribute.appedn((p[4], p[3], p[5], p[6]))
    elif p[3] == 'key':
        if temp_rel.setPrimary_key(p[4]):
            # add new relation into relation list
            relation_list.append( {'name': temp_rel.name, 'primary_key': temp_rel.primary_key, 'attribute': temp_rel.attribute} )
            # change state to command mode
            isCmdState = True
            with open('Data/relation_list.json', 'w') as datafile:
                json.dump(relation_list, datafile)



def p_create_cmd(p):
    # create table <relation_name> <table_name>
    'create_cmd : CREATE TABLE WORD WORD'

    # check state ---------------------------------------
    if not isCmdState:
        print('You cannot do this command. plz finish define relation first.')
        return 0

    # Do command ----------------------------------------
    relation_name = p[3]
    table_name = p[4]
    if relation_name in relation_list:
        table = Table(p[4], relation_list[p[3]]['primary_key'], relation_list[p[3]]['attribute'], {})
        process.createTable(table_name, table)
    else:
        print('Error: relation "' + relation_name + '" is not exist.')

    # renew and write the table list file
    table_list = []
    with open('Data/table_list.json', 'r+') as datafile:
        table_list = json.load(datafile)
    table_list.append(table_name)
    with open('Data/table_list.json', 'w+') as datafile:
        json.dump(table_list, datafile)

    
def p_insert_cmd(p):
    # insert <table_name> (<attribute_value>)+
    'insert_cmd : INSERT WORD attribute_expr'

    # check state ---------------------------------------
    if not isCmdState:
        print('You cannot do this command. plz finish define relation first.')
        return 0

    table_name = p[2]
    table = process.readTable(table_name)
    if table is not None:
        table.addElement(p[3])
        process.writeTable(table_name, table)

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
    
    # check state ---------------------------------------
    if not isCmdState:
        print('You cannot do this command. plz finish define relation first.')
        return 0

    table_name = p[2]
    table = process.readTable(table_name)
    table.delElement(p[3])
    process.writeTable(table_name, table)

def p_update_cmd(p):
    # update <table_name> <primary_key_value> (<attribute_value>)+
    'update_cmd : UPDATE WORD NUMBER attribute_expr'
    
    # check state ---------------------------------------
    if not isCmdState:
        print('You cannot do this command. plz finish define relation first.')
        return 0

    table_name = p[2]
    element = (p[3],) + p[4]
    table = process.readTable(table_name)
    table.updateElement(p[3], element)
    process.writeTable(table_name, table)

def p_select_cmd(p):
    # select <attribute_name> from <table_name> where <expr>
    #      [0]       [1]   [2]  [3]  [4]  [5]   [6]
    '''select_cmd : SELECT WORD FROM WORD WHERE expr
                  | SELECT WORD FROM WORD'''
    
    # check state ---------------------------------------
    if not isCmdState:
        print('You cannot do this command. plz finish define relation first.')
        return 0

    # read table from file
    table_name = p[4]
    table = process.readTable(table_name).table
    for attr in table['attribute']:
        if p[2] in attr:
            attribute = attr
    temp_table = {'name' : table_name, 'attribute':[attribute], 'primary_key': table['primary_key'], 'elements': {}}


    # Do Command collect what to show
    attribute = p[2]

    if len(p) is 5:
        for key in table['elements']:
            temp_table['elements'].update({ key : table['elements'][key][attribute]})
    elif len(p) is 7:
        a = p[6][0]
        b = p[6][1]
        c = p[6][2]
        for key in table['elements']:
            if   b == '=':
                if table['elements'][key][a] == c:
                    temp_table['elements'].update({ key : table['elements'][key][attribute]})
            elif b == '>':
                if table['elements'][key][a] > c:
                    temp_table['elements'].update({ key : table['elements'][key][attribute]})
            elif b == '<':
                if table['elements'][key][a] < c:
                    temp_table['elements'].update({ key : table['elements'][key][attribute]})

    # Send result table to client

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
    # print(result)

