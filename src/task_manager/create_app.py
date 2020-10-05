from flask import Flask

import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(20).hex()

    return app
