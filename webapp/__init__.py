from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def create_task():
        return 'Mock for creating task'

    @app.route('/')
    @app.route('/<int:task_id>')
    def check_task_status(task_id=None):
        return 'Mock for check status'

    return app
