from datetime import datetime

from sqlalchemy.orm import backref

from ext import db


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(10), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_delete = db.Column(db.Boolean, default=True)
    interface = db.relationship('Interface', backref='project')

    def __str__(self):
        return self.project_name