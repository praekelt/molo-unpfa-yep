ARG MOLO_VERSION
FROM praekeltfoundation/molo-bootstrap:${MOLO_VERSION}-onbuild

ENV DJANGO_SETTINGS_MODULE=tuneme.settings.docker \
    CELERY_APP=tuneme \
    CELERY_WORKER=1 \
    CELERY_BEAT=1

RUN LANGUAGE_CODE=en django-admin compilemessages && \
    django-admin collectstatic --noinput && \
    django-admin compress

CMD ["tuneme.wsgi:application", "--timeout", "1800"]
