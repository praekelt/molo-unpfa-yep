FROM praekeltfoundation/django-bootstrap:onbuild
RUN apt-get-install.sh git libjpeg-dev zlib1g-dev libffi-dev gettext libtiff-dev nodejs npm \
    gcc && ln -s /usr/bin/nodejs /usr/bin/node

ENV PROJECT_ROOT /app/
ENV DJANGO_SETTINGS_MODULE tuneme.settings.docker
ENV CELERY_APP tuneme
ENV CELERY_BEAT 1

RUN mkdir -p /app/media
RUN django-admin compress
RUN django-admin collectstatic --noinput
