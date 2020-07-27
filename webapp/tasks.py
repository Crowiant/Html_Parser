import time
from .utils import parse_text, create_file, create_zip
from .extensions import celery_app as celery


@celery.task(bind=True)
def create_parse_task(self, text):
    time.sleep(60)
    task_id = '{0.id}'.format(self.request)
    data = parse_text(text)
    file = create_file(data)
    zip_file = create_zip(file, task_id)

