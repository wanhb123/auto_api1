from datetime import datetime

from ext import db


class Interface(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    inf_url = db.Column(db.String(50), nullable=False)
    inf_name = db.Column(db.String(10), nullable=False)
    req_method = db.Column(db.String(10), nullable=False)
    req_parameters = db.Column(db.String(150), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    create_person = db.Column(db.String(10), default='万海波')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)

    __tablename__ = 'interface'

    def __str__(self):
        return self.inf_name