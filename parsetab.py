
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = b'%\x1b\xa8\x16sM-\xe2\xd32\x82\x8d\xe0\xd2`M'
    
_lr_action_items = {'ATTRIBUTE':([2,],[20,]),'SET':([0,],[2,]),'CREATE':([0,],[10,]),'GET':([0,],[19,]),'DELETE':([0,],[5,]),'INSERT':([0,],[6,]),'GREATER':([53,],[56,]),'NUMBER':([22,23,24,31,35,36,37,49,52,56,57,58,],[33,36,37,42,36,36,36,52,55,59,60,61,]),'WHERE':([47,],[51,]),'WORD':([5,6,7,9,23,26,27,30,32,35,36,37,38,39,42,51,],[22,23,24,25,35,39,40,41,43,35,35,35,47,48,50,53,]),'RELATION':([11,19,],[27,28,]),'$end':([1,3,4,8,12,13,14,15,16,17,18,28,29,33,34,35,36,40,41,43,44,45,46,47,48,50,54,55,59,60,61,],[-8,-6,-1,-9,-4,-3,-7,-10,-2,-5,0,-12,-11,-24,-19,-22,-23,-13,-16,-17,-20,-21,-25,-27,-18,-14,-26,-15,-29,-28,-30,]),'KEY':([21,],[32,]),'DEFINE':([0,],[11,]),'EQUAL':([53,],[57,]),'LESS':([53,],[58,]),'SELECT':([0,],[9,]),'UPDATE':([0,],[7,]),'TABLE':([10,19,],[26,29,]),'EXIT':([0,],[15,]),'RANGE':([41,],[49,]),'PRIMARY':([2,],[21,]),'FROM':([25,],[38,]),'INTEGER':([20,],[30,]),'CHARACTER':([20,],[31,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'get_cmd':([0,],[1,]),'attribute_expr':([23,35,36,37,],[34,44,45,46,]),'update_cmd':([0,],[3,]),'select_cmd':([0,],[14,]),'define_cmd':([0,],[4,]),'exit_cmd':([0,],[8,]),'expr':([51,],[54,]),'set_cmd':([0,],[16,]),'delete_cmd':([0,],[17,]),'command':([0,],[18,]),'insert_cmd':([0,],[12,]),'create_cmd':([0,],[13,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> command","S'",1,None,None,None),
  ('command -> define_cmd','command',1,'p_command','SqlYacc.py',43),
  ('command -> set_cmd','command',1,'p_command','SqlYacc.py',44),
  ('command -> create_cmd','command',1,'p_command','SqlYacc.py',45),
  ('command -> insert_cmd','command',1,'p_command','SqlYacc.py',46),
  ('command -> delete_cmd','command',1,'p_command','SqlYacc.py',47),
  ('command -> update_cmd','command',1,'p_command','SqlYacc.py',48),
  ('command -> select_cmd','command',1,'p_command','SqlYacc.py',49),
  ('command -> get_cmd','command',1,'p_command','SqlYacc.py',50),
  ('command -> exit_cmd','command',1,'p_command','SqlYacc.py',51),
  ('exit_cmd -> EXIT','exit_cmd',1,'p_exit_cmd','SqlYacc.py',54),
  ('get_cmd -> GET TABLE','get_cmd',2,'p_get_cmd','SqlYacc.py',59),
  ('get_cmd -> GET RELATION','get_cmd',2,'p_get_cmd','SqlYacc.py',60),
  ('define_cmd -> DEFINE RELATION WORD','define_cmd',3,'p_define_cmd','SqlYacc.py',78),
  ('set_cmd -> SET ATTRIBUTE CHARACTER NUMBER WORD','set_cmd',5,'p_set_cmd','SqlYacc.py',93),
  ('set_cmd -> SET ATTRIBUTE INTEGER WORD RANGE NUMBER NUMBER','set_cmd',7,'p_set_cmd','SqlYacc.py',94),
  ('set_cmd -> SET ATTRIBUTE INTEGER WORD','set_cmd',4,'p_set_cmd','SqlYacc.py',95),
  ('set_cmd -> SET PRIMARY KEY WORD','set_cmd',4,'p_set_cmd','SqlYacc.py',96),
  ('create_cmd -> CREATE TABLE WORD WORD','create_cmd',4,'p_create_cmd','SqlYacc.py',128),
  ('insert_cmd -> INSERT WORD attribute_expr','insert_cmd',3,'p_insert_cmd','SqlYacc.py',155),
  ('attribute_expr -> WORD attribute_expr','attribute_expr',2,'p_attribute_expr','SqlYacc.py',170),
  ('attribute_expr -> NUMBER attribute_expr','attribute_expr',2,'p_attribute_expr','SqlYacc.py',171),
  ('attribute_expr -> WORD','attribute_expr',1,'p_attribute_expr','SqlYacc.py',172),
  ('attribute_expr -> NUMBER','attribute_expr',1,'p_attribute_expr','SqlYacc.py',173),
  ('delete_cmd -> DELETE WORD NUMBER','delete_cmd',3,'p_delete_cmd','SqlYacc.py',181),
  ('update_cmd -> UPDATE WORD NUMBER attribute_expr','update_cmd',4,'p_update_cmd','SqlYacc.py',195),
  ('select_cmd -> SELECT WORD FROM WORD WHERE expr','select_cmd',6,'p_select_cmd','SqlYacc.py',210),
  ('select_cmd -> SELECT WORD FROM WORD','select_cmd',4,'p_select_cmd','SqlYacc.py',211),
  ('expr -> WORD EQUAL NUMBER','expr',3,'p_expr','SqlYacc.py',253),
  ('expr -> WORD GREATER NUMBER','expr',3,'p_expr','SqlYacc.py',254),
  ('expr -> WORD LESS NUMBER','expr',3,'p_expr','SqlYacc.py',255),
]
