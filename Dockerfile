FROM praekeltfoundation/django-bootstrap



RUN apt-get-install.sh gettext

ENV PROJECT_ROOT=/app/ \
    DJANGO_SETTINGS_MODULE=tuneme.settings.docker \
    APP_MODULE="tuneme.wsgi:application"

ENV CELERY_APP=tuneme \
    CELERY_BEAT=1

COPY . /app

RUN pip install -e .

RUN LANGUAGE_CODE=en django-admin compilemessages && \
    mkdir -p /app/media && \
    django-admin compress && \
    django-admin collectstatic --noinput
