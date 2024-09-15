import logging
import sqlite3 as sl

from .todoist_client import TodoistClient

logger = logging.getLogger(__name__)

class Organizer:
    
    def config_logger(self):
        logging.basicConfig(level=logging.INFO)
    
    def __init__(self, db_path, api_key) -> None:
        self.config_logger()
        self.db_path = db_path
        self.api_key = api_key
    
    def clear_db(self):
        con = sl.connect(self.db_path)
        cur = con.cursor()
        q = f'DELETE FROM tasks'
        cur.execute(q)
        q = f'DELETE FROM sync_tokens'
        cur.execute(q)
        con.commit()
        con.close()
        
    def save_sync_token(self, sync_token):
        con = sl.connect(self.db_path)
        cur = con.cursor()
        logger.debug(sync_token) # TODO Clarify log message
        # Clear sync_tokens table
        q = f"DELETE FROM sync_tokens"
        cur.execute(q)
        # Insert new sync token
        q = f"INSERT INTO sync_tokens VALUES ('{sync_token}')"
        logger.debug(f"Executing query: {q}")
        cur.execute(q)
        con.commit()
        con.close()

    def sync(self):
        # TODO Use sync tokens for requests
        # TODO fetch due dates
        con = sl.connect(self.db_path)
        cur = con.cursor()
        
        # Get stored sync token
        query = f'SELECT id FROM sync_tokens LIMIT 1'
        cur.execute(query)
        rows = cur.fetchall()
        sync_token = None
        if (len(rows) > 0):
            sync_token = rows[0][0]
        logger.debug(f'sync_token: {sync_token}')

        todoist_client = TodoistClient(self.api_key)
        response = todoist_client.get_tasks_sync(sync_token)
        tasks = response.tasks
        sync_token = response.sync_token
        logger.info(f"Fetched {len(tasks)} tasks")
        
        self.save_sync_token(sync_token)

        # logger.debug(tasks[0])

        for task in tasks:
            content = task.content.replace('\'', '\'\'')
            query = f"INSERT OR REPLACE INTO tasks (id, content, prio) VALUES ({task.id}, '{content}', {task.prio})"
            # logger.debug('Executing query: ' + query)
            cur.execute(query)
        
        con.commit()
        con.close()

    def search(self, text: str):
        con = sl.connect(self.db_path)
        cur = con.cursor()
        query = f"SELECT * FROM tasks WHERE content LIKE '%{text}%'"
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            logger.info(row)
        