import awsgi
import json
from app import app

def lambda_handler(event,context):
    response = awsgi.response(app,event,context)
    return {
        'statusCode': response['statusCode'],
        'headers': dict(response['headers']),
        'body': json.dumps(json.loads(response['body']))
    }

