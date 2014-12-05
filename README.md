SmallDB
=======

a small database for course

System Fuction

    1. user log in/out
        log in <user_id> <password>
        log out
        sysadmin authentication
    2. build relation table 

Support Command as following:

assigned:

    define relation <relation_name>
    set attribute integer <attribute_name>
    set attribute integer <attribute_name> range <minimum> <maximum>
    set attribute character <attribute_name> <size>
    set primary key <attribute_name>
    
    create table <relation_name> <table_name>
    insert <table_name> <primary_key_value> (<attribute_value>)+
    delete <table_name> <primary_key_value>
    update <table_name> <primary_key_value> (<attribute_value>)+
    select (<attribute_name>)+ from <table_name> where (<condition>)+ ; <condition> := <attribute_name> ['='|'>'|'<'] <value>
    
addition:

    show <table_name>
    shutdown
