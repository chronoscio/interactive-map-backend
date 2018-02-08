#!/bin/bash
# wait-for-postgres.sh

set -e

host="$DB_DEFAULT_HOST"
port="$DB_DEFAULT_PORT"
cmd="$@"

python bin/wait_for_postgres.py $host $port

>&2 echo "Postgres is up - executing command"

/bin/ash bin/migrate.sh
printf "from django.contrib.auth.models import User\nif not User.objects.exists(): User.objects.create_superuser(*\"$CREATE_SUPER_USER\".split(\":\"))" |  /venv/bin/python manage.py shell
# /bih/ash bin/superuser.sh

exec $cmd