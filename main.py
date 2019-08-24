import boto3
import json

comprehend = boto3.client(service_name='comprehend', region_name='ca-central-1')

text = 'Analfungus'

print('Calling DetectSentiment')
print(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectSentiment\n')