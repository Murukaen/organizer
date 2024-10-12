import logging
import sqlite3 as sl
import json

from .todoist_client import Task, TodoistClient
from .logger_utils import configure_logger
from utils.datetime_utils import extract_date

class Organizer:
    
    LOG_LEVEL = logging.DEBUG
    TASK_URL_PREFIX = 'https://app.todoist.com/app/task/'
    
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
                due_sql = 'NULL'
                if task.due:
                    due_sql = f'\'{task.due.isoformat()}\''
                labels_str = json.dumps(task.labels)
                query = f"INSERT OR REPLACE INTO tasks (id, content, prio, due, labels) VALUES ({task.id}, '{content}', {task.prio}, {due_sql}, '{labels_str}')"
            else:
                query = f"DELETE FROM tasks WHERE id = {task.id}"
            Organizer.logger.debug('Executing query: ' + query)
            cur.execute(query)
        
        con.commit()
        con.close()
        
    def __get_todo_from_db_row(self, row) -> Task:
        ret = Task(row[0])
        ret.set_content(row[1])
        ret.set_prio(row[2])
        if row[3] != None:
            ret.set_due(extract_date(row[3]) if row[3] != None else None)
        ret.labels = json.loads(row[4])
        return ret

    def search(self, text: str):
        con = sl.connect(self.db_path)
        cur = con.cursor()
        query = f"SELECT * FROM tasks WHERE content LIKE '%{text}%'"
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            task = self.__get_todo_from_db_row(row)
            print(task)
            
    def clear_db(self):
        con = sl.connect(self.db_path)
        cur = con.cursor()
        q = f'DELETE FROM tasks'
        cur.execute(q)
        q = f'DELETE FROM sync_tokens'
        cur.execute(q)
        con.commit()
        con.close()
    
    def search_label(self, label: str) -> list[Task]:
        Organizer.logger.debug(f'Called search_label() for label "{label}"')
        con = sl.connect(self.db_path)
        cur = con.cursor()
        query = f"SELECT DISTINCT tasks.* from tasks, json_each(tasks.labels) where json_each.value = '{label}'"
        cur.execute(query)
        rows = cur.fetchall()
        tasks = []
        for row in rows:
            task = self.__get_todo_from_db_row(row)
            tasks.append(task)
        return tasks
    
    def get(self, id, props):
        ret = {}
        for w in props.split(','):
            if w == 'url':
                ret['url'] = Organizer.TASK_URL_PREFIX + id
        return ret
        