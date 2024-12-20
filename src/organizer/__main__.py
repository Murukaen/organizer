import argparse
import sys

from .organizer import Organizer
    
def parse_args_and_execute():
    parser = argparse.ArgumentParser(prog = 'Organizer')
    parser.add_argument('-d', '--database', required = True)
    sub_parsers = parser.add_subparsers(help='Available commands', dest='command', required=True)
    _ = sub_parsers.add_parser('clear', help='clear db')
    parser_sync = sub_parsers.add_parser('sync', help='sync tasks from Todoist API')
    parser_sync.add_argument('-k', '--key', required = True)
    parser_search = sub_parsers.add_parser('search', help='search tasks')
    group_search = parser_search.add_mutually_exclusive_group(required=True)
    group_search.add_argument('-q', '--query')
    group_search.add_argument('-l', '--label')
    parser_get = sub_parsers.add_parser('get', help='get details about a task')
    parser_get.add_argument('-id', '--id', required = True)
    parser_get.add_argument('-p', '--props', required = True) # TODO Add help description
    args = parser.parse_args()
    
    organizer = Organizer(args.database)
    
    if args.command == 'clear':
        organizer.clear_db()
    elif args.command == 'sync':
        organizer.sync(args.key)
    elif args.command == 'search':
        if args.query:
            organizer.search(args.query)
        else:
            # args.label is set
            tasks = organizer.search_label(args.label)
            print('Items:\n------')
            for task in tasks:
                print(task)
            print(f'------\nReturned {len(tasks)} items')
    elif args.command == 'get':
        data = organizer.get(args.id, args.props)
        print(data)

def main():
    parse_args_and_execute()

if __name__ == '__main__':
    sys.exit(main())
    