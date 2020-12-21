from flask import Flask
from flask_cors import CORS

import settings
from apps.interface.view import interface
from apps.project.views import project_Bp
from apps.user.views import UserApi, user_api
from ext import db


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(settings.Development)
    db.init_app(app)
    CORS(app)
    app.register_blueprint(user_api)
    app.register_blueprint(interface)
    app.register_blueprint(project_Bp)
    return app
