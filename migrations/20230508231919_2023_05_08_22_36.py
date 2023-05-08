"""
This module contains a Caribou migration.

Migration Name: 2023_05_08_22_36 
Migration Version: 20230508231919
"""

def upgrade(connection):
    # add your upgrade step here
    sql = '''
        CREATE TABLE tasks
        (
            id INTEGER,
            content TEXT
        )
    '''
    connection.execute(sql)

def downgrade(connection):
    connection.execute('DROP TABLE tasks')
