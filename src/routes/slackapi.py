import requests
from flask import Blueprint, request
from models import db
from config import getConfig
from models import Channel, User, UserScore
from datetime import date
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

config = getConfig()

# Azure Setup
credentials = CognitiveServicesCredentials(config.azure_key)
text_analytics = TextAnalyticsClient(endpoint=config.text_analytics_url, credentials=credentials)

slackapi = Blueprint('slackapi', __name__)

# Handle the case when a new channel is messaged in for the first time.
def handleChannel(cid):
    channel = db.session.query(Channel).filter(Channel.cid == cid).first()
    if channel is None:
        token = config.slack_token
        slack_api = config.slack_api
        channel_info = requests.get(slack_api + "channels.info", params={"token":token, "channel":cid} ).json()
        channel_name = channel_info["channel"]["name"]
        new_channel = Channel(cid=cid, channel_name=channel_name)
        db.session.add(new_channel)
    return channel.id
     

# Handle the case when the user sending the message is not currently in the db.     
def handleUser(uid):
    user = db.session.query(User).filter(User.uid==uid).first()
    if user is None:
        email = getUserEmail(uid)
        user = User(uid=uid, user_name=email)
        db.session.add(user)
    return user.id
      

# Get the user email based on their UID.
def getUserEmail(uid):
    token = config.slack_token
    slack_api = config.slack_api
    r = requests.get(slack_api + "users.info", params={"token":token, "user":uid}).json()
    return r['user']['profile']['email']


# Get the sentiment analysis of a single message
def getSentiment(msg):
    text = [{
        "id": "1",
        "language": "en",
        "text": msg
    }]
    return text_analytics.sentiment(documents=text)

# Update the users daily score.
def updateUserScore(uid, text):
    sentiment = getSentiment(text)
    cur_record_query = db.session.query(UserScore).filter(UserScore.uid == uid).filter(UserScore.date == date.today())
    cur_record = cur_record_query.first()
    if cur_record is None:
        user_score_record = UserScore(daily_average=int(float(sentiment.documents[0].score * 100)), date=date.today(), total=1, uid=uid)
        db.session.add(user_score_record)
    else:
        daily_average = int((cur_record.daily_average + float(sentiment.documents[0].score) * 100) / (cur_record.total + 1))
        cur_record_query.update({"daily_average": daily_average, "total": cur_record.total + 1})
    db.session.commit()

@slackapi.route('/', methods=['POST'])
def postSlackAPI():
    data = request.get_json()
    request_type = data["event"]["type"]
    if request_type == "message":
        user_id = handleUser(data['event']['user'])
        channel_id = handleChannel(data["event"]["channel"])
        db.session.commit()
        updateUserScore(user_id, data['event']['text'])
    elif request_type == "channel_rename":
        
