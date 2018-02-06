#!/bin/bash

printf "from django.contrib.auth.models import User\nif not User.objects.exists(): User.objects.create_superuser(*\"$CREATE_SUPER_USER\".split(\":\"))" |  /venv/bin/python manage.py shell