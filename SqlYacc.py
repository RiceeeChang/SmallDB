#---------------------------------------
#
# SqlYacc.py - small DB yacc
#
#---------------------------------------
import ply.yacc as yacc

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
if os.path.exists('Data/relation_list.json'):
    with open('Data/relation_list.json', 'r+') as datafile:
        relation_list = json.load(datafile)
        # print(relation_list)
else:
    with open('Data/relation_list.json', 'w+') as datafile:
        json.dump(relation_list, datafile)
        datafile.close()

table_list = []
if os.path.exists('Data/table_list.json'):
    with open('Data/table_list.json', 'r+') as datafile:
        table_list = json.load(datafile)
        # print(table_list)
else:
    with open('Data/table_list.json', 'w+') as datafile:
        json.dump(table_list, datafile)
        datafile.close()

def p_command(p):
    '''command : define_cmd
               | set_cmd
               | create_cmd
               | insert_cmd
               | delete_cmd
               | update_cmd
               | select_cmd
               | get_cmd
               | delete_table_cmd
               | delete_relation_cmd
               | exit_cmd
               | reset_cmd
               | reset_relation_cmd'''
    p[0] = p[1]

def p_exit_cmd(p):
    # exit database system
    '''exit_cmd : EXIT'''
    sys.exit()

# Remove all table and relation Data in Data folder
def p_reset_cmd(p):
    '''reset_cmd : RESET DATABASE'''
    # check state -----------------------------
    if not isCmdState:
        p[0] =  {'response' : 'Error: You cannot do this command, please finish defining a relation.'}
        return 

    process.deleteAll()
    for table in table_list:
        del table
    for relation in relation_list:
        del relation
    p[0] = {'response' : 'success'}
    return

def p_get_cmd(p):
    '''get_cmd : GET TABLE
               | GET RELATION'''

    # check state -----------------------------
    if not isCmdState:
        p[0] =  {'response' : 'Error: You cannot do this command, please finish defining a relation.'}
        return 

    # Do command ------------------------------
    if p[2] == 'table':
        print("get table");
        p[0] =  {'response' : 'success', 'data' : table_list}
        return
    elif p[2] == 'relation':
        p[0] =  {'response' : 'success', 'data' : relation_list}
        return 

    p[0] =  {'response' : 'success'}
    return 


def p_define_cmd(p):
    # define relation <relation_name>
    'define_cmd : DEFINE RELATION WORD'
    global temp_rel
    global isCmdState

    relation_name = p[3]
    # check state
    if not isCmdState:
        p[0] =  {'response' : 'Error: You cannot do this command, please finish defining a relation.'}
        return 
    for relation in relation_list:
        if relation['name'] == p[3]:
            p[0] = {'response' : 'Error: Relation "' + relation_name + '" has existed in database.'}
            return

    temp_rel = Relation(p[3])
    isCmdState = False
    p[0] =  {'response' : 'success'}
    return


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
        p[0] =  {'response' : 'You cannot do this command. plz define a relation first.'}
        return 
    
    if p[3] == 'character':
        p[0] = temp_rel.addAttribute(p[5], (p[5], p[3], p[4]))
        return 
    elif p[3] == 'integer':
        if len(p) is 5:
            p[0] = temp_rel.addAttribute(p[4], (p[4], p[3]))
            return
        elif len(p) is 8:
            p[0] = temp_rel.addAttribute(p[4], (p[4], p[3], p[6], p[7]))
            return
    elif p[3] == 'key':
        result = temp_rel.setPrimary_key(p[4])
        if result is True:
            # add new relation into relation list
            relation_list.append( {'name': temp_rel.name, 'primary_key': temp_rel.primary_key, 'attribute': temp_rel.attribute} )
            # change state to command mode
            isCmdState = True
            with open('Data/relation_list.json', 'w') as datafile:
                json.dump(relation_list, datafile)
        else:
            p[0] = result
            return

    p[0] =  {'response' : 'success'}
    return 

def p_reset_relation_cmd(p):
    '''reset_relation_cmd : RESET RELATION'''
    global isCmdState
    isCmdState = True
    p[0] = {'response' : 'success'}
    return

def p_create_cmd(p):
    # create table <relation_name> <table_name>
    'create_cmd : CREATE TABLE WORD WORD'

    # check state ---------------------------------------
    if not isCmdState:
        p[0] =  {'response' : 'Error: You cannot do this command, please finish defining a relation.'}
        return 

    # Do command ----------------------------------------
    relation_name = p[3]
    table_name = p[4]
    for relation in relation_list:
        if relation['name'] == relation_name:
            table = Table(table_name, relation['primary_key'], relation['attribute'], {})
            result = process.createTable(table_name, table)
            # Check table is existing or not
            if result is not True:
                p[0] = result
                return
            table_list.append( {'name': table_name, 'primary_key': relation['primary_key'], 'attribute': relation['attribute']} )
            with open('Data/table_list.json', 'w+') as datafile:
                json.dump(table_list, datafile)

            p[0] =  {'response' : 'success'}
            return

    # if relation_name is not in relation_list, return default error
    p[0] =  {'response' : 'Error: Relation "' + relation_name + '" is not found in database.'}
    return 

def p_delete_relation_cmd(p):   
    '''delete_relation_cmd : DELETE RELATION WORD'''
    
    # check state ---------------------------------------
    if not isCmdState:
        p[0] =  {'response' : 'Error: You cannot do this command, please finish defining a relation.'}
        return 

    relation_name = p[3]

    for relation in relation_list:
        if relation['name'] == relation_name:
            relation_list.remove(relation)
            with open('Data/relation_list.json', 'w+') as datafile:
                json.dump(relation_list, datafile)
            p[0] =  {'response' : 'success'}
            return

    p[0] = {'response' : 'Error: Relation "' + relation_name + '" is not found in database.'}
    return 

def p_delete_table_cmd(p):
    '''delete_table_cmd : DELETE TABLE WORD'''
    
    # check state ---------------------------------------
    if not isCmdState:
        p[0] =  {'response' : 'Error: You cannot do this command, please finish defining a relation.'}
        return

    table_name = p[3]
    if table_name in table_list:
        table_list.remove(table_name)
        with open('Data/table_list.json', 'w+') as datafile:
            json.dump(table_list, datafile)
        os.remove('Data/' + table_name + '.json')
        p[0] =  {'response' : 'success'}
        return

    p[0] = {'response' : 'Error: Table "' + table_name + '" is not found in database.'}
    return
    
def p_insert_cmd(p):
    # insert <table_name> (<attribute_value>)+
    'insert_cmd : INSERT WORD attribute_expr'

    # check state ---------------------------------------
    if not isCmdState:
        p[0] = {'response' : 'Error: You cannot do this command, please finish defining a relation.'}
        return

    if p[3][0] is 'null':
        p[0] = {'response' : 'Error: Value of primary key cannot be "null".'}
        return


    table_name = p[2]
    table = process.readTable(table_name)
    if table is not None:  # table exist
        result = table.addElement(p[3])
        if result is True: # no error while adding 
            process.writeTable(table_name, table)
            p[0] =  {'response' : 'success'}
            return 
        else:
            p[0] = result
            return
    else:
        p[0] = {'response' : 'Error: Table "' + table_name + '" is not found in database.'}
        return

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
        p[0] =  {'response' : 'Error: You cannot do this command, please finish defining a relation.'}
        return 

    table_name = p[2]
    table = process.readTable(table_name)
    if table is not None:
        p[0] = table.delElement(p[3])
        process.writeTable(table_name, table)
        return
    else:
        p[0] = {'response' : 'Error: Table "' + table_name + '" is not found in database.'}
        return 

def p_update_cmd(p):
    # update <table_name> <primary_key_value> (<attribute_value>)+
    'update_cmd : UPDATE WORD NUMBER attribute_expr'
    
    # check state ---------------------------------------
    if not isCmdState:
        p[0] =  {'response' : 'Error: You cannot do this command, please finish defining a relation.'}
        return 

    table_name = p[2]
    element = (p[3],) + p[4]
    table = process.readTable(table_name)
    if table is not None:
        p[0] = table.updateElement(p[3], element)
        process.writeTable(table_name, table)
        return 
    else:
        p[0] = {'response' : 'Error: Table "' + table_name + '" is not found in database.'}
        return 

def p_select_cmd(p):
    # select <attribute_name> from <table_name> where <expr>
    #      [0]       [1]   [2]  [3]  [4]  [5]   [6]
    '''select_cmd : SELECT WORD FROM WORD WHERE expr
    			  | SELECT ALL FROM WORD WHERE expr
                  | SELECT WORD FROM WORD
                  | SELECT ALL FROM WORD'''
    
    # check state ---------------------------------------
    if not isCmdState:
        p[0] =  {'response' : 'Error: You cannot do this command, please finish defining a relation.'}
        return 
    
    # set some 
    table_name = p[4]
    # read table from file
    table = process.readTable(table_name).table
    # check table is existing.
    if table is None:
        p[0] = {'response' : 'Error: Table "' + table_name + '" is not found in database.'}
        return 
    
    # if select all 
    if p[2] == 'all':
        if len(p) is 5:
            p[0] =  {'response' : 'success', 'data' : table}
            return 
        elif len(p) is 7:
            # Create a temp to collection selection item.
            temp_table = {'name' : table_name, 'attribute':table['attribute'], 'primary_key': table['primary_key'], 'elements': {}}
            a = p[6][0]
            b = p[6][1]
            c = p[6][2]
            for key in table['elements']:
                if   b == '=':
                    if table['elements'][key][a] == c:
                        temp_table['elements'].update({ key : table['elements'][key]})
                elif b == '>':
                    if table['elements'][key][a] > c:
                        temp_table['elements'].update({ key : table['elements'][key]})
                elif b == '<':
                    if table['elements'][key][a] < c:
                        temp_table['elements'].update({ key : table['elements'][key]})
            p[0] = {'response' : 'success', 'data' : temp_table}
            return

    # check attribute is in table   [undo] 
    for attr in table['attribute']:
        if p[2] in attr:
            attribute = attr

    # Create a temp to collection selection item.
    temp_table = {'name' : table_name, 'attribute':[attribute], 'primary_key': table['primary_key'], 'elements': {}}

    # Do Command collect what to show
    attribute = p[2]
    if len(p) is 5:    # No WHERE
        print('here')
        for key in table['elements']:
            temp_table['elements'].update({ key : table['elements'][key][attribute]})
    elif len(p) is 7:  # WHERE 
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
    p[0] =  {'response' : 'success', 'data' : temp_table}
    return 

def p_expr(p):
    # <attribute_name> [=|>|<] <value>
    '''expr : WORD EQUAL NUMBER
            | WORD GREATER NUMBER
            | WORD LESS NUMBER'''
    p[0] = (p[1], p[2], p[3])
    return

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in ", p.value)

# parser has been import in Server
# --------------------------------
parser = yacc.yacc()
# --------------------------------

if __name__ == '__main__':
    # Build the parser
    
    while True:
        try:
            s = input('sql > ')
        except EOFError:
            break

        if not s: continue
        result = parser.parse(s)
        print(result)

