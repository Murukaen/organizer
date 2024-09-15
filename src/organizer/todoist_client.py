import requests
import sqlite3 as sl
import logging

logger = logging.getLogger(__name__)

class Task:
    def __init__(self, id: str):
        self.id = id
    def set_content(self, content: str):
        self.content = content
    def set_prio(self, prio: int):
        self.prio = prio
    def set_checked(self, checked: bool):
        self.checked = checked
    def __str__(self) -> str:
        return f'[id:{self.id}] [content:{self.content}] [p:{self.prio}]'
    
class SyncResponse:
    def __init__(self, tasks: list[Task], sync_token: str):
        self.tasks = tasks
        self.sync_token = sync_token

class TodoistClient:
    
    TASKS_URL = 'https://api.todoist.com/rest/v2/tasks'
    SYNC_URL = 'https://api.todoist.com/sync/v9/sync'
    
    def __init__(self, key):
        self.key = key
        logging.basicConfig(level=logging.INFO)
    
    # not used
    def get_tasks(self):
        url = self.TASKS_URL
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

    def get_tasks_sync(self, sync_token: None | str) -> SyncResponse:
        # Get items from Todoist
        url = self.SYNC_URL
        headers = {'Authorization': 'Bearer ' + self.key}
        payload = {
            'sync_token': f'{sync_token if(sync_token) else "*"}',
            'resource_types': '["items"]'
        }
        res = requests.post(url, headers=headers, json=payload)
        if (res.status_code == 401):
            logger.error('Forbidden')
            return
        sync_token = res.json()['sync_token']

        # Construct response
        tasks:list[Task] = []
        for item in res.json()['items']:
            task = Task(item['id'])
            task.set_content(item['content'])
            task.set_prio(item['priority'])
            task.set_checked(item['checked'])
            tasks.append(task)
        return SyncResponse(tasks, sync_token)