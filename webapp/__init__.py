from flask import Flask, request
import requests


def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def create_task():
        url = request.data

#       Validating html TODO: make deco from this
        try:
            get_html = requests.get(url)
        except (requests.exceptions.MissingSchema,
                requests.exceptions.InvalidSchema):
            return 'Not valid url'
        except requests.exceptions.ConnectionError:
            return "Can't connect to url", 500

        return url

    @app.route('/')
    @app.route('/<int:task_id>')
    def check_task_status(task_id=None):
        return 'Mock for check status'

    return app
