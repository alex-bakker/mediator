import boto3
import json
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)

CORS(app)

migrate = Migrate(app, db)

comprehend = boto3.client(service_name='comprehend', region_name='ca-central-1')

text = 'Analfungus'

print('Calling DetectSentiment')
print(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectSentiment\n')