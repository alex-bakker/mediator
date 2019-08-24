import os

class Config():
    DATABASE_URL = 'postgres+psycopg2://qa:qatest@localhost:5432/mediator'
    text_analytics_url = "https://mediator-text-analytics.cognitiveservices.azure.com/"
    azure_key = os.environ["TA_ANALYTICS"]
    slack_token = os.environ["SLACK_TOKEN"]
    slack_api = "https://slack.com/api/"

def getConfig():
    return Config()