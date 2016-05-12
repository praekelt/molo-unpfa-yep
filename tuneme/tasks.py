from molo.core import content_rotation
from tuneme import celery_app


@celery_app.task(ignore_result=True)
def rotate_content():
    content_rotation.rotate_content()
