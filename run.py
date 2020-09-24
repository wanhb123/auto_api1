from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from apps.project.models import Project
from apps.user.models import User
from apps.interface.models import Interface
from apps import create_app
from ext import db

app = create_app()

manager = Manager(app)

Migrate(app=app, db=db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()