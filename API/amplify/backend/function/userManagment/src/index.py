from requests import HTTPError
from http import HTTPStatus
from functools import wraps
import os
import boto3

class CustomException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.message = message
        self.code = code

    def to_dict(self):
        return {
            "statusCode": self.code,
            "body": self.message
        }


def exception_handler(func):
    @wraps(func)
    def wrapper(event, context):
        print("Événement reçu :", event)
        response = {}
        try:
            if not event['headers'].get('x-api-key'):
                raise CustomException('x-api-key is invalid', HTTPStatus.FORBIDDEN)
            
            res = func(event, context)
            if res:
                response['body'] = res
            response['statusCode'] = HTTPStatus.OK
        except HTTPError as e:
            response['body'] = e.response
            response['statusCode'] = e.response.status_code
        except CustomException as e:
            response = e.to_dict()
        except Exception as e:
            print("Erreur interne :", str(e))
            response['body'] = str(e)
            response['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
        return response
    return wrapper

# Fonction principale avec gestion des exceptions
@exception_handler
def handler(event, context):
    if event.get('httpMethod') != 'GET':
        raise CustomException('Method not allowed', HTTPStatus.METHOD_NOT_ALLOWED)
    
    # Configuration de DynamoDB
    user_table_name = os.environ.get('STORAGE_USERS_NAME')
    if not user_table_name:
        raise CustomException("DynamoDB table name not configured", HTTPStatus.INTERNAL_SERVER_ERROR)
    
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table(user_table_name)

    # Récupération de l'ID utilisateur à partir des en-têtes
    user_id = event['headers']['x-api-key']
    print(f"Recherche de l'utilisateur avec user_id : {user_id}")

    # Requête pour récupérer l'utilisateur dans DynamoDB
    try:
        res = table.get_item(Key={'id': user_id})
        print(f"Résultat de la requête DynamoDB : {res}")

        data = res.get('Item')
        if not data:
            print("Utilisateur non trouvé dans DynamoDB")
            raise CustomException("User not found", HTTPStatus.NOT_FOUND)

        print(f"Utilisateur trouvé : {data}")
        return data['email']
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur : {str(e)}")
        raise CustomException(f"Error retrieving user: {str(e)}", HTTPStatus.INTERNAL_SERVER_ERROR)
