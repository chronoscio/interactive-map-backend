1. virtualenv setup:
* virtualenv -p python3 venv
* source venv/bin/activate
* pip install -r requirements.txt
2. postgres + postgis setup https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04, https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/postgis/
* service start postgresql
* sudo su - postgres
* psql
* create database interactivemap;
* psql interactivemap
* CREATE EXTENSION postgis;
* CREATE USER dwaxe WITH PASSWORD 'asdf1234';
* ALTER ROLE dwaxe SET client_encoding TO 'utf8';
* ALTER ROLE dwaxe SET default_transaction_isolation TO 'read committed';
* ALTER ROLE dwaxe SET timezone TO 'UTC';
* GRANT ALL PRIVILEGES ON DATABASE interactivemap TO dwaxe;
3. data setup:
* ./manage.py migrate
* ./manage.py loaddata france
* ./manage.py createsuperuser
4. running:
* In c9.io: `python manage.py runserver $IP:$PORT`