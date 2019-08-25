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

class UserScore(db.Model):
    __tablename__ = 'user_score'

    id = db.Column(db.Integer, primary_key=True)
    daily_average = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'))

    user = relationship('User')
    
class ChannelScore(db.Model):
    __tablename__ = 'channel_score'

    id = db.Column(db.Integer, primary_key=True)
    daily_average = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    channel_id = db.Column(db.ForeignKey('channel.id'))

    channel = relationship('Channel')
