ARG MOLO_VERSION=6
FROM praekeltfoundation/molo-bootstrap:${MOLO_VERSION}-onbuild

ENV DJANGO_SETTINGS_MODULE=tuneme.settings.docker \
    CELERY_APP=tuneme

RUN LANGUAGE_CODE=en SECRET_KEY=compilemessages-key django-admin compilemessages && \
    SECRET_KEY=collectstatic-key django-admin collectstatic --noinput && \
    SECRET_KEY=compress-key django-admin compress

CMD ["tuneme.wsgi:application", "--timeout", "1800"]
