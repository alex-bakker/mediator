from main import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    average_postive = db.Column(db.Integer, nullable=False)
    average_neutral = db.Column(db.Integer, nullable=False)
    average_negative = db.Column(db.Integer, nullable=False)