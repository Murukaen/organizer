import argparse
import sqlite3 as sl
import requests
import json

class Task:
    def __init__(self, id):
        self.id = id
    def set_content(self, content):
        self.content = content
    def __str__(self) -> str:
        return f'[id:{self.id}] [content:{self.content}]'

class TodoistClient:
    def __init__(self, key):
        self.key = key
    
    def get_tasks(self):
        url = 'https://api.todoist.com/rest/v2/tasks'
        headers = {'Authorization': 'Bearer ' + self.key}
        res = requests.get(url, headers=headers)
        if (res.status_code == 401):
            print('Forbidden')
            return
        ret = []
        for item in res.json():
            task = Task(item['id'])
            task.set_content(item['content'])
            ret.append(task)
        return ret

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'Organizer')
    parser.add_argument('-k', '--key', required = True)
    args = parser.parse_args()

    con = sl.connect('test.db')

    todoist_client = TodoistClient(args.key)
    tasks = todoist_client.get_tasks()
    print(tasks[0])
    