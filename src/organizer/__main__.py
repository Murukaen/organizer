import argparse
import sys

from .organizer import Organizer
    
def parse_args_and_execute():
    parser = argparse.ArgumentParser(prog = 'Organizer')
    parser.add_argument('-k', '--key', required = True)
    parser.add_argument('-d', '--database', required = True)
    sub_parsers = parser.add_subparsers(help='sub_parsers help here', dest='subparser_name', required=True)
    parser_clear = sub_parsers.add_parser('clear', help='clear db')
    parser_sync = sub_parsers.add_parser('sync', help='desc here')
    parser_search = sub_parsers.add_parser('search', help='desc here')
    group_search = parser_search.add_mutually_exclusive_group(required=True)
    group_search.add_argument('-q', '--query')
    group_search.add_argument('-l', '--label')
    args = parser.parse_args()
    
    organizer = Organizer(args.database, args.key)
    
    if args.subparser_name == 'clear':
        organizer.clear_db()
    elif args.subparser_name == 'sync':
        organizer.sync()
    elif args.subparser_name == 'search':
        if args.query:
            organizer.search(args.query)
        else:
            # args.label is set
            tasks = organizer.search_label(args.label)
            for task in tasks:
                print(task)

def main():
    parse_args_and_execute()

if __name__ == '__main__':
    sys.exit(main())
    