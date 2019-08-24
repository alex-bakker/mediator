from flask import Blueprint, request

scores = Blueprint('scores', __name__)

@scores.route('/', methods=['POST'])
def updateScore():
    
