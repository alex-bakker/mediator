import requests
from flask import Blueprint, request
from models import db
from config import getConfig
from models import Channel

slackapi = Blueprint('slackapi', __name__)

def handleUser():
    pass

def handleChannel(cid):
    channel = db.session.query(Channel).filter(Channel.cid == cid).first()
    print(channel)
    if channel is None:
        token = getConfig().slack_token
        slack_api = getConfig().slack_api
        channel_info = requests.get(slack_api + "channels.info", params={"token":token, "channel":cid} )
        print(channel_info)

        

@slackapi.route('/', methods=['POST'])
def postSlackAPI():
    data = request.get_json()
    request_type = data["event"]["type"]
    if request_type == "message":
        handleUser()
        handleChannel(data["event"]["channel"])
    elif request_type == "channel_rename":
        pass