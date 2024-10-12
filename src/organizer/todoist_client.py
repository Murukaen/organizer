import requests
import logging
from datetime import datetime
from .logger_utils import configure_logger
from utils.datetime_utils import extract_date

class Task:
    def __init__(self, id: str):
        self.id = id
        self.due = None
    def set_content(self, content: str):
        self.content = content
    def set_prio(self, prio: int):
        self.prio = prio
    def set_checked(self, checked: bool):
        self.checked = checked
    def set_due(self, due: datetime):
        self.due = due
    def set_labels(self, labels: list[str]):
        self.labels = labels
    def __str__(self) -> str:
        return f'[id:{self.id}] [content:{self.content}] [p:{self.prio}] [due:{self.due}] [labels:{self.labels}]'
    
class SyncResponse:
    def __init__(self, tasks: list[Task], sync_token: str):
        self.tasks = tasks
        self.sync_token = sync_token

class TodoistClient:
    
    LOG_LEVEL = logging.DEBUG
    TASKS_URL = 'https://api.todoist.com/rest/v2/tasks'
    SYNC_URL = 'https://api.todoist.com/sync/v9/sync'
    
    logger = logging.getLogger(__name__)
    
    def __init__(self, key):
        self.key = key
        self.__configure_logger()
        
    def __configure_logger(self):
        configure_logger(TodoistClient.logger, self.LOG_LEVEL)
    
    # not used
    # TODO Consider cleanup
    def get_tasks(self):
        url = self.TASKS_URL
        headers = {'Authorization': 'Bearer ' + self.key}
        res = requests.get(url, headers=headers)
        if (res.status_code == 401):
            TodoistClient.logger.error('Forbidden')
            return
        ret = []
        for item in res.json():
            task = Task(item['id'])
            task.set_content(item['content'])
            ret.append(task)
        return ret
            
    def __extract_prio(self, prio: int) -> int:
        return 5 - prio 

    def get_tasks_sync(self, sync_token: None | str) -> SyncResponse:
        # Get items from Todoist
        TodoistClient.logger.info('Fetching tasks ...')
        url = self.SYNC_URL
        headers = {'Authorization': 'Bearer ' + self.key}
        payload = {
            'sync_token': f'{sync_token if(sync_token) else "*"}',
            'resource_types': '["items"]'
        }
        res = requests.post(url, headers=headers, json=payload)
        if (res.status_code == 401):
            TodoistClient.logger.error('Forbidden')
            return
        sync_token = res.json()['sync_token']
        TodoistClient.logger.info(f'Fetched tasks')

        # Construct response
        tasks:list[Task] = []
        for item in res.json()['items']:
            task = Task(item['id'])
            task.set_content(item['content'])
            task.set_prio(self.__extract_prio(item['priority']))
            task.set_checked(item['checked'])
            due_json = item['due']
            if due_json:
                due = extract_date(due_json['date'])
                task.set_due(due)
            else:
                task.set_due(None)
            task.set_labels(item['labels'])
            tasks.append(task)
        return SyncResponse(tasks, sync_token)