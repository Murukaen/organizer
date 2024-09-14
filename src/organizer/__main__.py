import argparse
import sqlite3 as sl

from organizer.todoist_client import TodoistClient

def clear_db(db):
    con = sl.connect(db)
    cur = con.cursor()
    q = f'DELETE FROM tasks'
    cur.execute(q)
    q = f'DELETE FROM sync_tokens'
    cur.execute(q)
    con.commit()
    con.close()

def sync(key: str, db: str):
    # TODO Use sync tokens for requests
    # TODO fetch due dates
    con = sl.connect(db)
    cur = con.cursor()

    todoist_client = TodoistClient(key)
    tasks = todoist_client.get_tasks_sync(db)

    print(tasks[0])

    for task in tasks:
        content = task.content.replace('\'', '\'\'')
        query = f"INSERT INTO tasks (id, content, prio) VALUES ({task.id}, '{content}', {task.prio})"
        print('Executing query: ' + query)
        cur.execute(query)
    
    con.commit()
    con.close()

def search(text: str, db: str):
    con = sl.connect(db)
    cur = con.cursor()
    query = f"SELECT * FROM tasks WHERE content LIKE '%{text}%'"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)

def parse_args_and_execute():
    parser = argparse.ArgumentParser(prog = 'Organizer')
    parser.add_argument('-k', '--key', required = True)
    parser.add_argument('-d', '--database', required = True)
    sub_parsers = parser.add_subparsers(help='sub_parsers help here', dest='subparser_name', required=True)
    parser_clear = sub_parsers.add_parser('clear', help='clear db')
    parser_sync = sub_parsers.add_parser('sync', help='desc here')
    parser_search = sub_parsers.add_parser('search', help='desc here')
    parser_search.add_argument('-q', '--query', required=True)
    args = parser.parse_args()
    
    if args.subparser_name == 'clear':
        clear_db(args.database)
    elif args.subparser_name == 'sync':
        sync(args.key, args.database)
    elif args.subparser_name == 'search':
        search(args.query, args.database)

if __name__ == '__main__':
    parse_args_and_execute()
    