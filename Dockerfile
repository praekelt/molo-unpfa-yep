FROM praekeltfoundation/django-bootstrap
RUN apt-get-install.sh \
    gettext \
    libjpeg62 \
    libtiff5

ENV PROJECT_ROOT /app/
ENV DJANGO_SETTINGS_MODULE tuneme.settings.docker
ENV APP_MODULE "tuneme.wsgi:application"

ENV CELERY_APP tuneme
ENV CELERY_BEAT 1

RUN LANGUAGE_CODE=en ./manage.py compilemessages
RUN mkdir -p /app/media
RUN django-admin compress
RUN django-admin collectstatic --noinput
