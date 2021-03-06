
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = b'\x84\x0f\xcd\x06\x04\xa6\xe2\x7f\xc7\x7f\x82\xbc$\xb9Jm'
    
_lr_action_items = {'ATTRIBUTE':([3,],[25,]),'SET':([0,],[3,]),'CREATE':([0,],[4,]),'WHERE':([61,62,],[65,66,]),'RELATION':([5,8,13,16,],[28,30,34,37,]),'PRIMARY':([3,],[26,]),'LESS':([69,],[73,]),'NUMBER':([31,32,36,41,46,47,48,63,67,72,73,74,],[47,48,50,55,47,47,47,67,71,75,76,77,]),'RANGE':([54,],[63,]),'EQUAL':([69,],[74,]),'KEY':([26,],[42,]),'WORD':([9,12,16,23,27,28,31,35,37,40,42,43,46,47,48,52,53,55,65,66,],[31,32,36,39,43,44,46,49,51,54,56,57,46,46,46,61,62,64,69,69,]),'ALL':([23,],[38,]),'GET':([0,],[8,]),'CHARACTER':([25,],[41,]),'DATABASE':([13,],[33,]),'$end':([1,2,6,7,10,11,14,15,17,18,19,20,21,22,24,29,30,33,34,44,45,46,47,49,50,51,54,56,57,58,59,60,61,62,64,68,70,71,75,76,77,],[-7,-6,-8,-2,-9,-5,-13,-14,-3,-4,0,-1,-10,-12,-11,-16,-17,-15,-23,-18,-27,-30,-31,-26,-32,-25,-21,-22,-24,-28,-29,-33,-37,-36,-19,-35,-34,-20,-39,-40,-38,]),'UPDATE':([0,],[12,]),'INSERT':([0,],[9,]),'GREATER':([69,],[72,]),'EXIT':([0,],[15,]),'FROM':([38,39,],[52,53,]),'DEFINE':([0,],[5,]),'DELETE':([0,],[16,]),'RESET':([0,],[13,]),'INTEGER':([25,],[40,]),'TABLE':([4,8,16,],[27,29,35,]),'SELECT':([0,],[23,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'delete_cmd':([0,],[11,]),'select_cmd':([0,],[1,]),'get_cmd':([0,],[6,]),'reset_relation_cmd':([0,],[14,]),'command':([0,],[19,]),'attribute_expr':([31,46,47,48,],[45,58,59,60,]),'expr':([65,66,],[68,70,]),'create_cmd':([0,],[17,]),'insert_cmd':([0,],[18,]),'exit_cmd':([0,],[24,]),'define_cmd':([0,],[20,]),'update_cmd':([0,],[2,]),'delete_relation_cmd':([0,],[21,]),'reset_cmd':([0,],[22,]),'set_cmd':([0,],[7,]),'delete_table_cmd':([0,],[10,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> command","S'",1,None,None,None),
  ('command -> define_cmd','command',1,'p_command','SqlYacc.py',48),
  ('command -> set_cmd','command',1,'p_command','SqlYacc.py',49),
  ('command -> create_cmd','command',1,'p_command','SqlYacc.py',50),
  ('command -> insert_cmd','command',1,'p_command','SqlYacc.py',51),
  ('command -> delete_cmd','command',1,'p_command','SqlYacc.py',52),
  ('command -> update_cmd','command',1,'p_command','SqlYacc.py',53),
  ('command -> select_cmd','command',1,'p_command','SqlYacc.py',54),
  ('command -> get_cmd','command',1,'p_command','SqlYacc.py',55),
  ('command -> delete_table_cmd','command',1,'p_command','SqlYacc.py',56),
  ('command -> delete_relation_cmd','command',1,'p_command','SqlYacc.py',57),
  ('command -> exit_cmd','command',1,'p_command','SqlYacc.py',58),
  ('command -> reset_cmd','command',1,'p_command','SqlYacc.py',59),
  ('command -> reset_relation_cmd','command',1,'p_command','SqlYacc.py',60),
  ('exit_cmd -> EXIT','exit_cmd',1,'p_exit_cmd','SqlYacc.py',64),
  ('reset_cmd -> RESET DATABASE','reset_cmd',2,'p_reset_cmd','SqlYacc.py',70),
  ('get_cmd -> GET TABLE','get_cmd',2,'p_get_cmd','SqlYacc.py',85),
  ('get_cmd -> GET RELATION','get_cmd',2,'p_get_cmd','SqlYacc.py',86),
  ('define_cmd -> DEFINE RELATION WORD','define_cmd',3,'p_define_cmd','SqlYacc.py',107),
  ('set_cmd -> SET ATTRIBUTE CHARACTER NUMBER WORD','set_cmd',5,'p_set_cmd','SqlYacc.py',129),
  ('set_cmd -> SET ATTRIBUTE INTEGER WORD RANGE NUMBER NUMBER','set_cmd',7,'p_set_cmd','SqlYacc.py',130),
  ('set_cmd -> SET ATTRIBUTE INTEGER WORD','set_cmd',4,'p_set_cmd','SqlYacc.py',131),
  ('set_cmd -> SET PRIMARY KEY WORD','set_cmd',4,'p_set_cmd','SqlYacc.py',132),
  ('reset_relation_cmd -> RESET RELATION','reset_relation_cmd',2,'p_reset_relation_cmd','SqlYacc.py',172),
  ('create_cmd -> CREATE TABLE WORD WORD','create_cmd',4,'p_create_cmd','SqlYacc.py',179),
  ('delete_relation_cmd -> DELETE RELATION WORD','delete_relation_cmd',3,'p_delete_relation_cmd','SqlYacc.py',210),
  ('delete_table_cmd -> DELETE TABLE WORD','delete_table_cmd',3,'p_delete_table_cmd','SqlYacc.py',231),
  ('insert_cmd -> INSERT WORD attribute_expr','insert_cmd',3,'p_insert_cmd','SqlYacc.py',251),
  ('attribute_expr -> WORD attribute_expr','attribute_expr',2,'p_attribute_expr','SqlYacc.py',280),
  ('attribute_expr -> NUMBER attribute_expr','attribute_expr',2,'p_attribute_expr','SqlYacc.py',281),
  ('attribute_expr -> WORD','attribute_expr',1,'p_attribute_expr','SqlYacc.py',282),
  ('attribute_expr -> NUMBER','attribute_expr',1,'p_attribute_expr','SqlYacc.py',283),
  ('delete_cmd -> DELETE WORD NUMBER','delete_cmd',3,'p_delete_cmd','SqlYacc.py',291),
  ('update_cmd -> UPDATE WORD NUMBER attribute_expr','update_cmd',4,'p_update_cmd','SqlYacc.py',310),
  ('select_cmd -> SELECT WORD FROM WORD WHERE expr','select_cmd',6,'p_select_cmd','SqlYacc.py',330),
  ('select_cmd -> SELECT ALL FROM WORD WHERE expr','select_cmd',6,'p_select_cmd','SqlYacc.py',331),
  ('select_cmd -> SELECT WORD FROM WORD','select_cmd',4,'p_select_cmd','SqlYacc.py',332),
  ('select_cmd -> SELECT ALL FROM WORD','select_cmd',4,'p_select_cmd','SqlYacc.py',333),
  ('expr -> WORD EQUAL NUMBER','expr',3,'p_expr','SqlYacc.py',409),
  ('expr -> WORD GREATER NUMBER','expr',3,'p_expr','SqlYacc.py',410),
  ('expr -> WORD LESS NUMBER','expr',3,'p_expr','SqlYacc.py',411),
]
