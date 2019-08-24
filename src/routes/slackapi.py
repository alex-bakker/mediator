from flask import Blueprint, request
from models import db, User
import requests

slackapi = Blueprint('slackapi', __name__)

def handleUser():
    pass

def handleChannel():
    pass

@slackapi.route('/', methods=['POST'])
def postSlackAPI():
    data = request.get_json()
    request_type = data["event"]["type"]
    if request_type == "message":
        handleUser()
        handleChannel()
    elif request_type == "channel_rename":
        pass


def handleUser(token):
    email = getUserEmail(token)
    user = db.session.query(User).filter(User.user_name==email).first()
    print(user)

def getUserEmail(token):
    URL = 'https://slack.com/api/users.identity.email'
    params = {'token' : token}
    return requests.get(URL, params=params)