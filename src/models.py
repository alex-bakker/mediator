from main import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Score(db.Model):
    __tablename__ = 'score'

    id = db.Column(db.Integer, primary_key=True)
    daily_average = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.Text, nullable=False)
    channel = db.Column(db.Text, nullable=False)

    
