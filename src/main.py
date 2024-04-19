import argparse
import json
import sqlite3 as sl

import requests


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

    def get_tasks_sync(self):
        url = 'https://api.todoist.com/sync/v9/sync'
        headers = {'Authorization': 'Bearer ' + self.key}
        payload = {
            'sync_token': '*',
            'resource_types': '["items"]'
        }
        res = requests.post(url, headers=headers, json=payload)
        if (res.status_code == 401):
            print('Forbidden')
            return
        sync_token = res.json()['sync_token']

        con = sl.connect('test.db')
        cur = con.cursor()
        print(sync_token)
        q = f"INSERT INTO sync_tokens VALUES ('{sync_token}')"
        print(f"Executing query: {q}")
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

def clear_db():
    con = sl.connect('test.db')
    cur = con.cursor()
    q = f'DELETE FROM tasks'
    cur.execute(q)
    q = f'DELETE FROM sync_tokens'
    cur.execute(q)
    con.commit()
    con.close()

def sync(key: str):
    # TODO Use sync tokens for requests
    # TODO fetch due dates
    con = sl.connect('test.db')
    cur = con.cursor()

    todoist_client = TodoistClient(key)
    tasks = todoist_client.get_tasks_sync()

    print(tasks[0])

    for task in tasks:
        content = task.content.replace('\'', '\'\'')
        query = f"INSERT INTO tasks (id, content, prio) VALUES ({task.id}, '{content}', {task.prio})"
        print('Executing query: ' + query)
        cur.execute(query)
    
    con.commit()
    con.close()

def search(text: str):
    con = sl.connect('test.db')
    cur = con.cursor()
    query = f"SELECT * FROM tasks WHERE content LIKE '%{text}%'"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'Organizer')
    parser.add_argument('-k', '--key', required = True)
    sub_parsers = parser.add_subparsers(help='sub_parsers help here', dest='subparser_name', required=True)
    parser_clear = sub_parsers.add_parser('clear', help='clear db')
    parser_sync = sub_parsers.add_parser('sync', help='desc here')
    parser_search = sub_parsers.add_parser('search', help='desc here')
    parser_search.add_argument('-q', '--query', required=True)
    args = parser.parse_args()
    
    if args.subparser_name == 'clear':
        clear_db()
    elif args.subparser_name == 'sync':
        sync(args.key)
    elif args.subparser_name == 'search':
        search(args.query)
    