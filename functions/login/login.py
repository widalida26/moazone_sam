import os
import json
import boto3

def handler(event, context):
    print(event)
    queryStr = event['queryStringParameters']
    email = queryStr['email']

    client = boto3.client('cognito-idp', region_name='ap-northeast-2')
    response = client.initiate_auth(
        AuthFlow = 'CUSTOM_AUTH',
        ClientId = os.environ.get('CLIENT_ID'),
        AuthParameters = {
            'USERNAME': email
        }
    )
    response["message"] = "login success"
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
        },
        'body': json.dumps(response)
    }