#!/bin/bash
# wait-for-postgres.sh

set -e

host="$DB_DEFAULT_HOST"
port="$DB_DEFAULT_PORT"
cmd="$@"

python bin/wait_for_postgres.py $host $port

>&2 echo "Postgres is up - executing command"

/bin/ash bin/migrate.sh
/bih/ash bin/superuser.sh

exec $cmd