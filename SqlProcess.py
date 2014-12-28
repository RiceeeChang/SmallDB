#-----------------------------------------
#
# SqlProcess - a Processor to deal SQL command
#
#-----------------------------------------
import itertools
import os
import json


class Relation(object):
    def __init__(self, name):
        self.name = name
        self.primary_key = ''
        self.attribute = []

    def setPrimary_key(self, key_name):
        for attr in self.attribute:
            if key_name in attr:
                primary = attr
                self.attribute.remove(attr)
                self.attribute.insert(0, primary)
                break;
        if primary is None:
            print('Error: there is no attribute named ' + key_name + ' in relation')
            return False
        else:
            self.primary_key = key_name
            return True

    def addAttribute(self, attribute_name, attribute_type):
        for attr in self.attribute:
            if attribute_name in attr:
                print('Error: there has been a attribute named ' + attribute_name)
                return 0
        attribute.append(attribute_type)

    def delAttribute(attribute_name):
        for attr in attribute:
            if attribute_name in attr:
                attribute.remove(attr)
                return 0
        print('Error: attribute "' + attribute_name + '" is not existing.')

# attr format is in a tuple
# (attribute_name, type = character, length)
# (attribute_name, type = integer)
# (attribute_name, type = integer, min, max)


class Table(object):
    def __init__(self, name, primary_key, attribute, element):
        self.name = name
        self.primary_key = primary_key
        self.attribute = attribute

        self.table = {'name' : name, 
                'primary_key' : primary_key, 
                'attribute' : attribute, 
                'elements' : element}

    # element - a tuple of inserted values (value1, value2, ...)
    def addElement(self, element):
        ele = {}
        primary_key = self.primary_key
        attribute = self.attribute

        # check the value type is valid.
        # add the value into ele
        for attr, value in zip(attribute, element):
            if attr[1] == 'character':
                value = str(value)
                if len(value) < attr[2]:
                    ele.update({attr[0] : value})
                else:
                    return {'response' : value + 'is over the ' + attr[0] + ' lenth limit.'}
            elif attr[1] == 'integer':
                if type(value) is int:
                    if len(attr) is 2:
                        ele.update({attr[0] : value})
                    elif len(attr) is 4:
                        if value >= attr[2] and value <= attr[3]:
                            ele.update({attr[0] : value})
                        else:
                            return {'response' : str(value) + ' is out of range.'}
                else:
                    value = str(value)
                    return {'response' : value  + ' is not integer.'}

        # check primary key is unique in element[]
        # ------------------
        # row - is the key in the table['elements']
        for key in self.table['elements']:
            if key == str(ele[primary_key]):
                return ('response' : 'Error: there has been a row with same primary key. ' + primary_key + " : " + str(ele[primary_key]))
        
        # cuz in JSON key value cannot be int
        # so we change all primary key value to string
        # add the ele into table
        self.table['elements'].update( { str(ele[primary_key]) : ele})
        return True


    # delete <table> <primary_key>
    def delElement(self, key_value):
        try:
            del self.table['elements'][str(key_value)]
        except KeyError:
            print('Key value "' + kay_value + '" is not existing.')

    # update <table> <primary_key> (<attribute_value>)+
    def updateElement(self, key_value, element):
        if str(key_value) in self.table['elements']:
            self.delElement(key_value)
        else:
            print('Key value "' + kay_value + '" is not existing.')
            return 0
        self.addElement(element)

def getFilePath(table_name):
    return 'Data/' + table_name + '.json'


def createTable(table_name, table):
    path = getFilePath(table_name)
    if os.path.exists(path):
        print('Table "' + table_name + '" has existed.')
    else:
        with open(path, 'w+') as datafile:
            json.dump(table.table, datafile)
            datafile.close()
            
def readTable(table_name):
    path = getFilePath(table_name)
    if os.path.exists(path):
        with open(path, 'r') as datafile:
            data = json.load(datafile)
            table = Table(data['name'], data['primary_key'], data['attribute'], data['elements'])
            return table
    else:
        return None

# -------------------------------
# writeTable - save table to a json file
# table_name - name of table and let it be file name
# table - table class object table.table is what to save
# -------------------------------

def writeTable(table_name, table):
    path = getFilePath(table_name)
    if os.path.exists(path):
        with open(path, 'w') as datafile:
            json.dump(table.table, datafile)
        return True
    else:
        print('Table "' + table_name + '" does not exist.')
        return False