import os
import boto3
import uuid
import json
import hashlib
from http import HTTPStatus
from boto3.dynamodb.conditions import Key

def handler(event, context):
    # Configuration de DynamoDB
    user_table_name = os.environ.get('STORAGE_USERS_NAME')
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table(user_table_name)


    body = event['body']
    if isinstance(body, str):
        body = json.loads(body)

    user_email = body.get('email')
    if not user_email:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "Missing email in the request body"
        }

    # Requête pour vérifier si l'utilisateur existe déjà
    res = table.query(
        IndexName='emails',
        KeyConditionExpression=Key('email').eq(user_email)
    )
    print(res)

    # Création de l'utilisateur si nécessaire
    if not res['Items']:
        user_id = str(uuid.uuid4())
        hash_value = hashlib.sha256((user_id + user_email).encode()).hexdigest()

        try:
            lambda_client = boto3.client('lambda', region_name='eu-west-1')
            lambda_client.invoke(
                FunctionName=os.environ.get('FUNCTION_ADDUSER_NAME'),
                InvocationType='Event',
                Payload=json.dumps({
                    'email': user_email,
                    'user_id': user_id,
                    'hash_value': hash_value
                })
            )
        except Exception as e:
            print(f"Error invoking addUser Lambda: {e}")
            return {
                "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                "body": f"Error invoking addUser Lambda: {str(e)}"
            }
    else:
        user_id = res['Items'][0].get('id')
        hash_value = res['Items'][0].get('hash_value')
        print("User already exists")

    # Retourne la réponse avec les informations de l'utilisateur
    return {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps({
            "user_id": user_id,
            "email": user_email,
            "hash_value": hash_value
        })
    }
