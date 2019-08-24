from flask import Blueprint, request

slackapi = Blueprint('slackapi', __name__)

@slackapi.route('/', methods=['POST'])
def postSlackAPI():
    data = request.get_json()
    return data["challenge"]
    