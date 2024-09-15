import argparse
import sqlite3 as sl
import logging
import sys

from organizer.todoist_client import TodoistClient

logger = logging.getLogger(__name__)

# TODO Rename file to organizer.py and keep `python -m organizer` functional

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
    logger.info(f"Fetched {len(tasks)} tasks")

    logger.debug(tasks[0])

    for task in tasks:
        content = task.content.replace('\'', '\'\'')
        query = f"INSERT OR REPLACE INTO tasks (id, content, prio) VALUES ({task.id}, '{content}', {task.prio})"
        logger.debug('Executing query: ' + query)
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
        logger.info(row)

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
    
def config_logger():
    logging.basicConfig(level=logging.INFO)

def main():
    config_logger();
    logger.info('Started')
    parse_args_and_execute()
    logger.info('Finished')

if __name__ == '__main__':
    sys.exit(main())
    