## Migrations
[Caribou](https://github.com/clutchski/caribou?tab=readme-ov-file#caribou-sqlite-migrations)
### Create migration
`caribou create -d migrations <name>`
### Apply migration
`caribou upgrade local/test.db src/migrations`
## Sqlite commands
open sqlite3 CLI: `sqlite3`\
sqlite3 show databases: `.databases`\
sqlite3 open db cmd: `.open <db_name>`\
sqlite3 show tables: `.tables`\
sqlite3 descrive table: `.schema <table_name>`\
close sqlite3 CLI: `^D`
## Run application
### Setup
Run once per terminal session: `source setup.sh`\
`python -m organizer` from top level directory
## Data states
- Db holds only uncompleted tasks (refreshed on every sync)