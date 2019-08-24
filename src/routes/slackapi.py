import requests
from flask import Blueprint, request
from models import db
from config import getConfig
from models import Channel, User

slackapi = Blueprint('slackapi', __name__)

def handleChannel(cid):
    channel = db.session.query(Channel).filter(Channel.cid == cid).first()
    if channel is None:
        token = getConfig().slack_token
        slack_api = getConfig().slack_api
        channel_info = requests.get(slack_api + "channels.info", params={"token":token, "channel":cid} ).json()
        channel_name = channel_info["channel"]["name"]
        new_channel = Channel(cid=cid, channel_name=channel_name)
        db.session.add(new_channel)
     



# Handle the case when the user sending the message is not currently in the db.     
def handleUser(uid):
    user = db.session.query(User).filter(User.uid==uid).first()
    if user is None:
        email = getUserEmail(uid)
        user = User(uid=uid, user_name=email)
        db.session.add(user)
      

# Get the user email based on their UID.
def getUserEmail(uid):
    token = getConfig().slack_token
    slack_api = getConfig().slack_api
    r = requests.get(slack_api + "users.info", params={"token":token, "user":uid}).json()
    return r['user']['profile']['email']


@slackapi.route('/', methods=['POST'])
def postSlackAPI():
    data = request.get_json()
    request_type = data["event"]["type"]
    if request_type == "message":
        handleUser(data['event']['user'])
        handleChannel(data["event"]["channel"])
        db.session.commit()
    elif request_type == "channel_rename":
        pass
