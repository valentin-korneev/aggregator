REM PWD postgres
SET PGPASSWORD=admin
SET PGCLIENTENCODING=UTF-8

psql -p 5433 -U postgres -d postgres -a -f ./database/_role.sql -L ./logs/_role.log
psql -p 5433 -U postgres -d postgres -a -f ./database/_database.sql -L ./logs/_database.log

REM PWD aggregator
SET PGPASSWORD=admin

psql -p 5433 -U aggregator -d aggregator -a -f ./database/_schema.sql -L ./logs/_schema.log