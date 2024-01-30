"""
This module contains a Caribou migration.

Migration Name: create_table_tasks
Migration Version: 20230508231919
"""

def upgrade(connection):
    # add your upgrade step here
    sql = '''
        CREATE TABLE tasks
        (
            id INTEGER PRIMARY KEY,
            content TEXT
        )
    '''
    connection.execute(sql)

def downgrade(connection):
    connection.execute('DROP TABLE tasks')
