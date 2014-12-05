#-----------------------------------------
#
# SqlProcess - a Processor to deal SQL command
#
#-----------------------------------------
import itertools


class Relation(object):
    def __init__(self, name):
        self.name = name
        primary_key = ''
        attribute = []

    def setPrimary_key(key_name):
        priary_key = key_name
        for attr in attribute:
            if key_name in attr:
                primary = attr
                attribute.remove(attr)
                attribute.insert(0, primary)
                break;
        if primary is None:
            print('Error: there is no attribute named ' + key_name + ' in relation')

    def addAttribute(attribute_name, attribute_type):
        for attr in attribute:
            if attribute_name in attr:
                print('Error: there has been a attribute named ' + attribute_name)
                return 0
        attribute.update({attribute_name : attribute_type})

    def delAttribute(attribute_name):
        for attr in attribute:
            if attribute_name in attr:
                attribute.remove(attribute_name)
                break

# attribute format
# (attribute_name, type = character, length)
# (attribute_name, type = integer)
# (attribute_name, type = integer, min, max)


class Table:
    def _init_(self, relation, name):
        self.name = name
        self.attribute = relation.attribute
        primary_key = relation.primary_key
        element = {}


    # element - a tuple of inserted values (value1, value2, ...)
    def addElement(element):
        ele = {}

        # check is the value valid
        # add the value into ele
        for attr, value in zip(attribute, element):
            if attr[1] is 'character':
                if type(value) is str and len(value) < attr[2]:
                    ele.update({attr[0] : value})
            elif attr[1] is 'integer':
                if type(value) is int:
                    if len(attr) is 2:
                        ele.update({attr[0] : value})
                    elif len(attr) is 4 and value >= attr[2] and value <= attr[3]:
                        ele.update({attr[0] : value})
            print(attr, value)

        # check primary key is unique in element[]
        for row in element:
            if row[primary_key] is ele[primary_key]:
                print('Error: there has been a row with same primary key.'+ primary_key + ": " + ele[primary_key])
                return 0
        # add the ele into table
        element.update({ele[primary_key] : ele})


    # delete <table> <primary_key>
    def delElement(key_value):
        del element[key_value]

    # update <table> <primary_key> (<attribute_value>)+
    def updateElement(key_value, element):
        for attr, value in zip(attribute[1:], element[1:]):
            element[key_value][attr[0]] = value

    # select Attribute and constrain ...
    #def selectElement(query_attribute, constrain):
        
