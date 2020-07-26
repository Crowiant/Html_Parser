from . import create_app
from .extensions import celery_app

flask_app = create_app()
flask_app.app_context().push()
