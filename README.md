## Migrations
[Caribou](https://github.com/clutchski/caribou?tab=readme-ov-file#caribou-sqlite-migrations)
### Create migration
`caribou create -d migrations <name>`
### Apply migration
`caribou upgrade test.db migrations`
## Sqlite commands
open sqlite3 CLI: `sqlite3`\
sqlite3 show databases: `.databases`\
sqlite3 open db cmd: `.open <db_name>`\
sqlite3 show tables: `.tables`\
sqlite3 descrive table: `.schema <table_name>`\
close sqlite3 CLI: `^D`