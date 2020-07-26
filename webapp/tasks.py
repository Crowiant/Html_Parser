from .utils import parse_text
from .extensions import celery_app as celery


@celery.task
def create_parse_task(text):
    parse_text(text)
