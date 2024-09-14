"""
This module contains a Caribou migration.

Migration Name: add_prios 
Migration Version: 20240126230630
"""

def upgrade(connection):
    sql = '''
        ALTER TABLE tasks 
        ADD prio INTEGER;
    '''
    connection.execute(sql)

def downgrade(connection):
    sql = '''
        ALTER TABLE tasks 
        DROP prio;
    '''
    connection.execute(sql)
