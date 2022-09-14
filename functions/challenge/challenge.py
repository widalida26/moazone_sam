import os
import json
import boto3
from connection import connect_engine
from models import Customers

engine = connect_engine()
session = engine.sessionmaker()

def handler(event, context):
    body_data = json.loads(event['body'])
    challenge_data = body_data['challengeData']
    username = challenge_data['username']

    client = boto3.client('cognito-idp', region_name='ap-northeast-2')
    response = client.respond_to_auth_challenge (
        ChallengeName = 'CUSTOM_CHALLENGE',
        ClientId = os.environ.get('CLIENT_ID'),
        ChallengeResponses = {
            'USERNAME': username,
            'ANSWER': challenge_data['answer'],
        },
        Session = challenge_data['session']
    )
    authResult = response['AuthenticationResult']

    existed = session.query(Customers).filter(Customers.user_id == username).all()
    consented = session.query(Customers).filter(Customers.user_id == username, Customers.consent == 1).all()
    session.close()

    if len(existed) < 1: 
        print('existed')
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
            },
            'body': json.dumps({ "message" : "not targeted" })
        }
    elif len(consented) > 0:
        print('consented')
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
            },
            'body': json.dumps({ "message" : "already participated" })
        }
    else:
        print('success')
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
            },
            'body': json.dumps({"accessToken" : authResult['IdToken'], "username" : challenge_data['username']}) 
        }