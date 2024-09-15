import requests
import sqlite3 as sl
import logging

logger = logging.getLogger(__name__)

class Task:
    def __init__(self, id):
        self.id = id
    def set_content(self, content):
        self.content = content
    def set_prio(self, prio):
        self.prio = prio
    def __str__(self) -> str:
        return f'[id:{self.id}] [content:{self.content}] [p:{self.prio}]'

class TodoistClient:
    def __init__(self, key):
        self.key = key
        logging.basicConfig(level=logging.INFO)
    
    # not used
    def get_tasks(self):
        url = 'https://api.todoist.com/rest/v2/tasks' # TODO Externalize
        headers = {'Authorization': 'Bearer ' + self.key}
        res = requests.get(url, headers=headers)
        if (res.status_code == 401):
            logger.error('Forbidden')
            return
        ret = []
        for item in res.json():
            task = Task(item['id'])
            task.set_content(item['content'])
            ret.append(task)
        return ret

    def get_tasks_sync(self, db: str):
        url = 'https://api.todoist.com/sync/v9/sync'
        headers = {'Authorization': 'Bearer ' + self.key}
        payload = {
            'sync_token': '*',
            'resource_types': '["items"]'
        }
        res = requests.post(url, headers=headers, json=payload)
        if (res.status_code == 401):
            logger.error('Forbidden')
            return
        sync_token = res.json()['sync_token']

        con = sl.connect(db) # TODO Remove db ops from API client
        cur = con.cursor()
        logger.debug(sync_token) # TODO Clarify log message
        q = f"INSERT INTO sync_tokens VALUES ('{sync_token}')"
        logger.debug(f"Executing query: {q}")
        cur.execute(q)
        con.commit()
        con.close()

        ret = []
        for item in res.json()['items']:
            task = Task(item['id'])
            task.set_content(item['content'])
            task.set_prio(item['priority'])
            ret.append(task)
        return ret