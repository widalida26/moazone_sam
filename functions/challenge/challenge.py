import os
import json
import boto3

def handler(event, context):
    body_data = json.loads(event['body'])
    print(body_data)
    challenge_data = body_data['challengeData']
    print(challenge_data)

    client = boto3.client('cognito-idp', region_name='ap-northeast-2')
    try:  
        response = client.respond_to_auth_challenge (
            ChallengeName = 'CUSTOM_CHALLENGE',
            ClientId = os.environ.get('CLIENT_ID'),
            ChallengeResponses = {
                'USERNAME': challenge_data['username'],
                'ANSWER': challenge_data['answer'],
            },
            Session = challenge_data['session']
        )
        print(response)
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
            },
            'body': json.dumps({ "message" : "challenge success" })
        }
    except:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
            },
            'body': json.dumps({ "message" : "challenge fail" })
        }