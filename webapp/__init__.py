import os
import requests
from flask import Flask, request, jsonify, url_for, send_file
from .extensions import celery_app
from .utils import create_main_directory, check_task, DIR_NAME
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
            return jsonify(status='Not valid url')
        except requests.exceptions.ConnectionError:
            return jsonify("Can't connect to url"), 500

        result = create_parse_task.delay(get_html.text)
        return jsonify(url=url_for('check_task_status', task_id=result.id))

    @app.route('/')
    @app.route('/<string:task_id>')
    def check_task_status(task_id=None):
        if not task_id:
            return jsonify(status='No data')

        task_value_dict = celery_app.control.inspect().active().values()
        result = check_task(task_id, task_value_dict)
        path_to_file = os.path.join(DIR_NAME, f'{task_id}.zip')

        if os.path.exists(path_to_file):
            return jsonify(status='Ready', url=url_for('send_zip', file_name=task_id))
        elif result:
            return jsonify(status='In progress')

        return jsonify(status='Not found'), 404

    @app.route('/download/<string:file_name>')
    def send_zip(file_name):
        path_to_file = os.path.join(DIR_NAME, f'{file_name}.zip')

        if os.path.exists(path_to_file):
            return send_file(os.path.abspath(path_to_file), as_attachment=True)

        return jsonify(status='No file exists'), 404

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
