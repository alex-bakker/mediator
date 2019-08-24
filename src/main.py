import json
import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import getConfig


#Load our configuration
config = getConfig()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://qa:qatest@localhost:5432/mediator'
CORS(app)


from models import db
from routes.slackapi import slackapi
app.register_blueprint(slackapi, url_prefix='/slackapi')

migrate = Migrate(app, db)