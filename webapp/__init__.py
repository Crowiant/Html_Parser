import requests
from flask import Flask, request
from .extensions import celery_app
from .utils import create_main_directory
from webapp.tasks import create_parse_task


def create_app():
    app = Flask(__name__)
    print(create_main_directory())
    init_celery(app)

    @app.route('/', methods=['POST'])
    def create_task():
        url = request.data

#       Validating html TODO: make deco from this
        try:
            get_html = requests.get(url)
            get_html.raise_for_status()
        except (requests.exceptions.MissingSchema,
                requests.exceptions.InvalidSchema):
            return 'Not valid url'
        except requests.exceptions.ConnectionError:
            return "Can't connect to url", 500

        result = create_parse_task.delay(get_html.text)
        return result.id

    @app.route('/')
    @app.route('/<str:task_id>')
    def check_task_status(task_id=None):
        return 'Mock for check status'

    return app


def init_celery(app=None):
    celery = celery_app
    #celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        "Make celery tasks work with Flask app context"
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
