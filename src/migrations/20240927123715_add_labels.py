"""
This module contains a Caribou migration.

Migration Name: add_labels 
Migration Version: 20240927123715
"""

def upgrade(connection):
    sql = '''
        ALTER TABLE tasks
        ADD labels TEXT;
    '''
    connection.execute(sql)

def downgrade(connection):
    sql = '''
        ALTER TABLE tasks
        DROP labels;
    '''
    connection.execute(sql)
