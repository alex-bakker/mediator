from main import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__= 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Text, nullable=False)
    user_name = db.Column(db.Text, nullable=False)

class Channel(db.Model):
    __tablename__= 'channel'
    
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Text, nullable=False)
    channel_name = db.Column(db.Text, nullable=False)

class Score(db.Model):
    __tablename__ = 'score'

    id = db.Column(db.Integer, primary_key=True)
    daily_average = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    uid = db.Column(db.ForeignKey('user.id'))
    cid = db.Column(db.ForeignKey('channel.id'))

    user = relationship('User')
    channel = relationship('Channel')
    
