import json
import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import getConfig


#Load our configuration
config = getConfig()

# Azure Setup
credentials = CognitiveServicesCredentials(config.azure_key)
text_analytics = TextAnalyticsClient(endpoint=config.text_analytics_url, credentials=credentials)

'''
documents = [{
    "id": "1",
    "language": "en",
    "text": "im happy, fuck you"
}]

response = text_analytics.sentiment(documents=documents)
for document in response.documents:
    print("Document Id: ", document.id, ", Sentiment Score: ",
          "{:.2f}".format(document.score))
'''


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://qa:qatest@localhost:5432/mediator'
CORS(app)


from models import db
from routes.slackapi import slackapi
app.register_blueprint(slackapi, url_prefix='/slackapi')

migrate = Migrate(app, db)