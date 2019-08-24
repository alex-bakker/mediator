from flask import Blueprint, request

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