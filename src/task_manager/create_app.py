from flask import Flask, Blueprint
from flask_restplus import Api

from .__version__ import __version__
from .views import ns_tasks, ns_users


def create_app():

    app = Flask(__name__)
    blueprint = Blueprint("api", __name__, url_prefix="/api")
    api = Api(blueprint, title="Task manager", version=__version__, doc="/docs")

    api.add_namespace(ns_tasks)
    api.add_namespace(ns_users)
    app.register_blueprint(blueprint)

    return app
