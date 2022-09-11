import json
import boto3

def handler(event, context):
    print(event)
    queryStr = event['queryStringParameters']
    email = queryStr['email']

    client = boto3.client('cognito-idp', region_name='ap-northeast-2')
    try:  
        response = client.initiate_auth(
            AuthFlow = 'CUSTOM_AUTH',
            ClientId='4mtc8aihivbsvf5ib1peg8d95',
            AuthParameters = {
                'USERNAME': email
            }
        )
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
            },
            'body': json.dumps({ "message" : "login success" })
        }
    except:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
            },
            'body': json.dumps({ "message" : "login error" })
        }