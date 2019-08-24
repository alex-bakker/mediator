import json
import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

# Azure Setup
text_analytics_url = "https://mediator-text-analytics.cognitiveservices.azure.com/"
key = os.environ["TA_ANALYTICS"]
credentials = CognitiveServicesCredentials(key)
text_analytics = TextAnalyticsClient(endpoint=text_analytics_url, credentials=credentials)

documents = [{
    "id": "1",
    "language": "en",
    "text": "im happy, fuck you"
}]

response = text_analytics.sentiment(documents=documents)
for document in response.documents:
    print("Document Id: ", document.id, ", Sentiment Score: ",
          "{:.2f}".format(document.score))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://qa:qatest@localhost:5432/mediator'
CORS(app)

from models import db

migrate = Migrate(app, db)