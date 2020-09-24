from datetime import datetime

from ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(15), nullable=False)
    phone = db.Column(db.String(11), nullable=False, unique=True)
    createtime = db.Column(db.DateTime, default=datetime.now())
    is_delete = db.Column(db.Boolean, default=True)
    __tablename = 'user'

    def __str__(self):
        return self.username