from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    @app.route('/<string:task_url>', methods=['POST'])
    def create_task(task_url=None):
        return 'Mock for creating task'

    @app.route('/')
    @app.route('/<int:task_id>')
    def check_task_status(task_id=None):
        return 'Mock for check status'

    return app
