from flask import Blueprint, Flask
from .categories_bp import bp as bp_categories
from .task_bp import bp as bp_tasks

bp_api = Blueprint("api", __name__, url_prefix="/api")


def init_app(app: Flask):
    bp_api.register_blueprint(bp_categories)
    bp_api.register_blueprint(bp_tasks)

    app.register_blueprint(bp_api)
