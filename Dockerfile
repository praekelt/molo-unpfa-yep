FROM praekeltfoundation/django-bootstrap
COPY . /app

RUN apt-get-install.sh \
    gettext \
    libjpeg62 \
    libtiff5

ENV PROJECT_ROOT /app/
ENV DJANGO_SETTINGS_MODULE tuneme.settings.docker
ENV APP_MODULE "tuneme.wsgi:application"

ENV CELERY_APP=tuneme \
    CELERY_BEAT=1

RUN LANGUAGE_CODE=en django-admin compilemessages && \
    mkdir -p /app/media && \
    django-admin compress && \
    django-admin collectstatic --noinput
