from app import db
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    field_data = db.Column(JSON)

    def __init__(self, field_data):
        self.field_data = field_data


class WorkQueue(db.Model):
    __tablename__ = "workQueue"

    id = db.Column(db.Integer, primary_key=True)
    field_data = db.Column(JSON)

    def __init__(self, field_data):
        self.field_data = field_data


class NZBFiles(db.Model):
    __tablename__ = 'nzbfile'
    
    id = db.Column(db.Integer, primary_key=True)
    field_data = db.Column(JSON)

    def __init__(self, field_data):
        self.field_data = field_data

