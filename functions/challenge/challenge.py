import os
import json
import boto3

def handler(event, context):
    body_data = json.loads(event['body'])
    challenge_data = body_data['challengeData']

    client = boto3.client('cognito-idp', region_name='ap-northeast-2')
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
    authResult = response['AuthenticationResult']
    print(authResult)
    try:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET',
            },
            'body': json.dumps({"accessToken" : authResult['AccessToken'], "username" : challenge_data['username']}) 
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