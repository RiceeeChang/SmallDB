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
        # check key_name is null
        if key_name == 'null':
            return {'response' : 'Error: Value of primary key cannot be "null".'}

        for attr in self.attribute:
            if key_name in attr:
                primary = attr
                self.attribute.remove(attr)
                self.attribute.insert(0, primary)
                break;
        if primary is None:
            return {'response' : 'Error: Attribute "' + key_name + '" is not found in Relation "' + self.name + '.'}
        else:
            self.primary_key = key_name
            return True

    def addAttribute(self, attribute_name, attribute_type):
        for attr in self.attribute:
            if attribute_name in attr:
                return {'response' : 'Error: Attribute "' + attribute_name + '" has existed in Relation "' + self.name + '.'}

        self.attribute.append(attribute_type)
        return {'response' : 'success'}

    def delAttribute(self, attribute_name):
        for attr in attribute:
            if attribute_name in attr:
                attribute.remove(attr)
                return True
        return {'response' : 'Error: Attribute "' + attribute_name + '" is not found in Relation "' + self.name + '.'}

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
                    return {'response' : 'Error: Integer "' + attr[0] + '" value is out of range.'}
            elif attr[1] == 'integer':
                if type(value) is int:
                    if len(attr) is 2:
                        ele.update({attr[0] : value})
                    elif len(attr) is 4:
                        if value >= attr[2] and value <= attr[3]:
                            ele.update({attr[0] : value})
                        else:
                            return {'response' : 'Error: Integer "' + attr[0] + '" value is out of range.'}
                else:
                    return {'response' : 'Error: "' + str(value) + '" is not integer'}

        # check primary key is unique in element[]
        # row - is the key in the table['elements']
        for key in self.table['elements']:
            if key == str(ele[primary_key]):
                return {'response' : 'Error: Element of Primary key "' + key + '" has existed in Table "' + self.name + '.'}
        
        # cuz in JSON key value cannot be int
        # so we change all primary key value to string
        # add the ele into table
        self.table['elements'].update( { str(ele[primary_key]) : ele})
        return True


    # delete <table> <primary_key>
    def delElement(self, key_value):
        try:
            del self.table['elements'][str(key_value)]
            return {'response' : 'success'}
        except KeyError:
            return {'response' : 'Error: Element of Primary key "' + key_value + '" is not found in Table "' + self.name + '.'}

    # update <table> <primary_key> (<attribute_value>)+
    def updateElement(self, key_value, element):
        data = self.table['elements'][str(key_value)]
        if str(key_value) in self.table['elements']:
            self.delElement(key_value)
        else:
            return {'response' : 'Error: Element of Primary key "' + str(key_value) + '" is not found in Table "' + self.name + '.'}
        
        result = self.addElement(element)

        if result is True:
            return {'response' : 'success'}
        else:
            self.addElement(data)
            return result


def getFilePath(table_name):
    return 'Data/' + table_name + '.json'


def createTable(table_name, table):
    path = getFilePath(table_name)
    if os.path.exists(path):
        return {'response' : 'Error: Table "' + table_name + '" has existed in database.'}
    else:
        with open(path, 'w+') as datafile:
            json.dump(table.table, datafile)
            datafile.close()
        return True
            
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
        # print('Table "' + table_name + '" does not exist.')
        return False

def deleteAll():
    folder = 'Data'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        os.remove(file_path)
    return 