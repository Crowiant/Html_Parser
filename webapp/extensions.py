from celery import Celery
from webapp.utils import parse_text


celery_app = Celery(__name__, broker='redis://localhost:6379/0')
