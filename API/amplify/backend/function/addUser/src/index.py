import os
import boto3
from http import HTTPStatus

def handler(event, context):
    # Configuration de DynamoDB
    user_table_name = os.environ.get('STORAGE_USERS_NAME')
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table(user_table_name)

    # Récupération des données de event
    user_email = event.get('email')
    user_id = event.get('user_id')
    hash_value = event.get('hash_value')

    # Validation des données
    if not user_email or not user_id:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "Missing user_id or email in the request body"
        }

    try:
        # Insertion des données dans DynamoDB
        table.put_item(Item={
            'id': user_id,
            'email': user_email,
            'hash_value': hash_value
        })
        return {
            "statusCode": HTTPStatus.OK,
            "body": "User added successfully"
        }
    except Exception as e:
        return {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": f"Error adding user: {str(e)}"
        }
