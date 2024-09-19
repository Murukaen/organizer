import logging
import sqlite3 as sl

from .todoist_client import Task, TodoistClient
from .logger_utils import configure_logger

class Organizer:
    
    LOG_LEVEL = logging.DEBUG
    
    logger = logging.getLogger(__name__)
    
    def __init__(self, db_path, api_key) -> None:
        self.__config_logger()
        self.db_path = db_path
        self.api_key = api_key
    
    def __config_logger(self):
        configure_logger(Organizer.logger, self.LOG_LEVEL);
        
    def __save_sync_token(self, sync_token):
        con = sl.connect(self.db_path)
        cur = con.cursor()
        Organizer.logger.debug(f'sync_token: {sync_token}')
        # Clear sync_tokens table
        q = f"DELETE FROM sync_tokens"
        cur.execute(q)
        # Insert new sync token
        q = f"INSERT INTO sync_tokens VALUES ('{sync_token}')"
        Organizer.logger.debug(f"Executing query: {q}")
        cur.execute(q)
        con.commit()
        con.close()
        
    def __log_fetched_tasks_stats(self, tasks: list[Task]):
        Organizer.logger.info(f"Fetched {len(tasks)} tasks")
        

    def sync(self):
        Organizer.logger.info('Starting sync ...')
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
        Organizer.logger.debug(f'sync_token: {sync_token}')

        # Get items from Todoist
        todoist_client = TodoistClient(self.api_key)
        response = todoist_client.get_tasks_sync(sync_token)
        tasks = response.tasks
        sync_token = response.sync_token
        self.__log_fetched_tasks_stats(tasks)
        
        # Save sync token
        self.__save_sync_token(sync_token)

        # logger.debug(tasks[0])

        for task in tasks:
            Organizer.logger.debug(f'Analyzing task: {task}')
            content = task.content.replace('\'', '\'\'')
            query = ''
            if not task.checked:
                query = f"INSERT OR REPLACE INTO tasks (id, content, prio) VALUES ({task.id}, '{content}', {task.prio})"
            else:
                query = f"DELETE FROM tasks WHERE id = {task.id}"
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
            # TODO Convert to and print a Task
            Organizer.logger.info(row)
            
    def clear_db(self):
        con = sl.connect(self.db_path)
        cur = con.cursor()
        q = f'DELETE FROM tasks'
        cur.execute(q)
        q = f'DELETE FROM sync_tokens'
        cur.execute(q)
        con.commit()
        con.close()
        