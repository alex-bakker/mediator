from flask import Blueprint, request

scores = Blueprint('slackapi', __name__)

@scores.route('/', methods=['POST'])
def updateScore():
    pass
