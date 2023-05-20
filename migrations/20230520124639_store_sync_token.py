"""
This module contains a Caribou migration.

Migration Name: store_sync_token 
Migration Version: 20230520124639
"""

def upgrade(connection):
    # add your upgrade step here
    sql = '''
        CREATE TABLE sync_tokens
        (
            id TEXT
        )
    '''
    connection.execute(sql)

def downgrade(connection):
    # add your downgrade step here
    connection.execute('DROP TABLE sync_tokens')
