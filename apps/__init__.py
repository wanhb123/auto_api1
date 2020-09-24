from flask import Flask
import settings
from apps.interface.view import interface
from apps.project.views import project
from apps.user.views import user

from ext import db


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(settings.Development)
    db.init_app(app)
    app.register_blueprint(user)
    app.register_blueprint(project)
    app.register_blueprint(interface)
    return app