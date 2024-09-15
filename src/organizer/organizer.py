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

    def sync(self):
        # TODO Use sync tokens for requests
        # TODO fetch due dates
        con = sl.connect(self.db_path)
        cur = con.cursor()

        todoist_client = TodoistClient(self.api_key)
        tasks = todoist_client.get_tasks_sync(self.db_path)
        logger.info(f"Fetched {len(tasks)} tasks")

        logger.debug(tasks[0])

        for task in tasks:
            content = task.content.replace('\'', '\'\'')
            query = f"INSERT OR REPLACE INTO tasks (id, content, prio) VALUES ({task.id}, '{content}', {task.prio})"
            logger.debug('Executing query: ' + query)
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
        