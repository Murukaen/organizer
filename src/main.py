import argparse
import sqlite3 as sl

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'Organizer')
    parser.add_argument('-k', '--key', required = True)
    args = parser.parse_args()

    con = sl.connect('test.db')
    