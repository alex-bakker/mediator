import requests
from flask import Blueprint, request, Response
from sqlalchemy import desc, asc
from models import db
from config import getConfig
from models import Channel, User, UserScore, ChannelScore
from datetime import date
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from flask import jsonify

config = getConfig()

# Azure Setup
credentials = CognitiveServicesCredentials(config.azure_key)
text_analytics = TextAnalyticsClient(endpoint=config.text_analytics_url, credentials=credentials)

slackapi = Blueprint('slackapi', __name__)

@slackapi.route('/overview')
def showOverview():
    try:
        users = db.session.query(UserScore).filter(UserScore.date == date.today()).order_by(asc(UserScore.id)).limit(3).all()
        channels = db.session.query(ChannelScore).filter(ChannelScore.date == date.today()).order_by(asc(ChannelScore.id)).limit(3).all()

        user_list = ''
        for user in users:
            user_list += '\n' + db.session.query(User).filter(User.id == user.user_id).first().email + ' : ' + user.daily_average

        channel_list = ''
        for channel in channels:
            channel_list += '\n' + db.session.query(Channel).filter(Channel.id == channel.channel_id).first().channel_name + ' : ' + channel.daily_average


        digest = 'Channels to look out for include: ' + user_list + channel_list
    return digest
    

@slackapi.route('/user', methods=['POST'])
def getUser():
    params = request.form['text'].split(' ')
    timeframe = ""
    user_email = ""
    if len(params) == 2:
        user_email = params[0]
        timeframe = params[1]
    else:
        return "Hey! Please provide a timeframe and an email!"

    time = 1
    if timeframe == "month":
        time = 30
    elif timeframe == "week":
        time = 7

    try:
        id = db.session.query(User).filter(User.user_name == user_email).first().id
        results = db.session.query(UserScore).filter(UserScore.user_id == id).order_by(desc(UserScore.id)).limit(time).all()
        
        sum_of_avg = 0
        num_of_records = len(results)
        
        for result in results:
            sum_of_avg += result.daily_average

        total_avg = sum_of_avg / num_of_records
        return 'User ' + user_email + ' had a score of ' + total_avg + ', this ' + timeframe

    except Exception:
        return "No data has been collected on that user yet! :("


@slackapi.route('/channel', methods=['POST'])
def getChannel():
    params = request.form['text'].split(' ')
    timeframe = ""
    channel_name = ""
    if len(params) == 2:
        channel_name = params[0]
        timeframe = params[1]
    else:
        return "Hey! Please provide a timeframe and a channel name!"

    time = 1
    if timeframe == "month":
        time = 30
    elif timeframe == "week":
        time = 7

    timeframe = 'day'

    try:
        id = db.session.query(Channel).filter(Channel.channel_name == channel_name).first().id
        results = db.session.query(ChannelScore).filter(ChannelScore.channel_id == id).order_by(desc(ChannelScore.id)).limit(time).all()

        sum_of_avg = 0
        num_of_records = len(results)
        
        for result in results:
            sum_of_avg += result.daily_average

        total_avg = sum_of_avg / num_of_records
        return 'Channel ' + channel_name + ' had a score of ' + total_avg + ', this ' + timeframe

    except Exception:
        return "No data has been collected on that channel yet! :("


# Handle the case when a new channel is messaged in for the first time.
def handleChannel(cid):
    channel = db.session.query(Channel).filter(Channel.cid == cid).first()
    if channel is None:
        token = config.slack_token
        slack_api = config.slack_api
        channel_info = requests.get(slack_api + "channels.info", params={"token":token, "channel":cid} ).json()
        channel_name = channel_info["channel"]["name"]
        channel = Channel(cid=cid, channel_name=channel_name)
        db.session.add(channel)
        db.session.commit()
    return channel.id
     

# Handle the case when the user sending the message is not currently in the db.     
def handleUser(uid):
    user = db.session.query(User).filter(User.uid==uid).first()
    if user is None:
        email = getUserEmail(uid)
        user = User(uid=uid, user_name=email)
        db.session.add(user)
        db.session.commit()
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
    sentiment = text_analytics.sentiment(documents=text)
    return text_analytics.sentiment(documents=text)

# Update the users daily score.
def updateUserScore(user_id, sentiment):
    cur_record_query = db.session.query(UserScore).filter(UserScore.user_id == user_id).filter(UserScore.date == date.today())
    cur_record = cur_record_query.first()
    if cur_record is None:
        user_score_record = UserScore(daily_average=int(float(sentiment.documents[0].score)*100), date=date.today(), total=1, user_id=user_id)
        db.session.add(user_score_record)
    else:
        score_as_int = float(sentiment.documents[0].score) * 100
        daily_average = score_as_int + (cur_record.daily_average * cur_record.total)
        daily_average = int(daily_average / (cur_record.total + 1))
        cur_record_query.update({"daily_average": daily_average, "total": cur_record.total + 1})
    db.session.commit()

# Update the channels daily score.
def updateChannelScore(channel_id, sentiment):
    cur_record_query = db.session.query(ChannelScore).filter(ChannelScore.channel_id == channel_id).filter(ChannelScore.date == date.today())
    cur_record = cur_record_query.first()
    if cur_record is None:
        channel_score_record = ChannelScore(daily_average=int(float(sentiment.documents[0].score)*100), date=date.today(), total=1, channel_id=channel_id)
        db.session.add(channel_score_record)
    else:
        score_as_int = float(sentiment.documents[0].score) * 100
        daily_average = score_as_int + (cur_record.daily_average * cur_record.total)
        daily_average = int(daily_average / (cur_record.total + 1))
        cur_record_query.update({"daily_average": daily_average, "total": cur_record.total + 1})
    db.session.commit()

@slackapi.route('/', methods=['POST'])
def postSlackAPI():
    data = request.get_json()
    request_type = data["event"]["type"]
    if request_type == "channel_rename":
        channel = db.session.query(Channel).filter(Channel.cid == data["event"]["channel"]["id"]).update({'channel_name': data["event"]["channel"]["name"]})
        db.session.commit()
    elif request_type == "message":
        user_id = handleUser(data['event']['user'])
        channel_id = handleChannel(data["event"]["channel"])
        db.session.commit()
        sentiment = getSentiment(data['event']['text'])
        updateUserScore(user_id, sentiment)
        updateChannelScore(channel_id, sentiment) 
    resp = Response('Warm')
    resp.headers['X-Slack-No-Retry'] = '1'
    return resp
