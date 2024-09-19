"""
This module contains a Caribou migration.

Migration Name: add_due_date 
Migration Version: 20240915205102
"""

def upgrade(connection):
    sql = '''
        ALTER TABLE tasks
        ADD due TEXT;
    '''
    connection.execute(sql)

def downgrade(connection):
    sql = '''
        ALTER TABLE tasks
        DROP due;
    '''
    connection.execute(sql)
