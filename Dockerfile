FROM python:3.6-alpine

ADD requirements.txt /requirements.txt

RUN set -ex \
    && apk add --no-cache alpine-sdk \
    && apk add --no-cache --virtual .build-deps-testing \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        gdal-dev \
        geos-dev \
    && apk add --no-cache --virtual .build-deps \
            gcc \
            make \
            libc-dev \
            musl-dev \
            postgresql-dev \
            linux-headers \
            pcre-dev \
    && pyvenv /venv \
    && /venv/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install --no-cache-dir -r /requirements.txt" \
    && runDeps="$( \
            scanelf --needed --nobanner --recursive /venv \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $runDeps \
    && apk del .build-deps

RUN mkdir /app/ && mkdir /appstatic/
WORKDIR /app/
ADD . /app/

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=interactive_map_backend.settings.production
# Default Django secret key to be able to run manage.py at build time.
# A real secret key must be given at runtime.
ENV SECRET_KEY='dummy'

ENV UWSGI_VIRTUALENV=/venv UWSGI_WSGI_FILE=interactive_map_backend/wsgi.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN DB_URL=none /venv/bin/python manage.py collectstatic --noinput

# Start uWSGI
CMD ["/bin/ash", "./bin/wait_for_postgres.sh", "/venv/bin/uwsgi", "--http-auto-chunked", "--http-keepalive"]
# CMD ["/venv/bin/python", "manage.py", "runserver"]