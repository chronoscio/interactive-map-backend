#!/bin/bash
# wait-for-postgres.sh

set -e

dbname="$DB_DEFAULT_NAME"
host="$DB_DEFAULT_HOST"
port="$DB_DEFAULT_PORT"
user="$DB_DEFAULT_USER"
passwd="$DB_DEFAULT_PASSWORD"
cmd="$@"

>&2 echo "Waiting for Postgres..."

/venv/bin/python bin/wait_for_postgres.py $dbname $host $port $user $passwd

>&2 echo "Postgres is up - executing command"

/bin/ash bin/migrate.sh
printf "from django.contrib.auth.models import User\nif not User.objects.exists(): User.objects.create_superuser(*\"$CREATE_SUPER_USER\".split(\":\"))" |  /venv/bin/python manage.py shell

exec $cmd