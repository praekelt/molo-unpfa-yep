FROM praekeltfoundation/django-bootstrap

RUN apt-get-install.sh gettext

ENV PROJECT_ROOT=/app/ \
    DJANGO_SETTINGS_MODULE=tuneme.settings.docker \
    CELERY_APP=tuneme \
    CELERY_BEAT=1

COPY . /app
COPY docker_nginx.conf /etc/nginx/conf.d/django.conf

RUN pip install -e .

RUN LANGUAGE_CODE=en django-admin compilemessages && \
    django-admin collectstatic --noinput && \
    django-admin compress

CMD ["tuneme.wsgi:application", "--timeout", "900"]
