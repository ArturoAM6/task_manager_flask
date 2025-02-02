# models.py

from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from enum import Enum
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    task = db.relationship('Task', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
        
class PriorityEnum(Enum):
    Low = 'Low'
    Medium = 'Medium'
    High = 'High'

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    priority = db.Column(db.Enum(PriorityEnum), default=PriorityEnum.Medium, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'
    