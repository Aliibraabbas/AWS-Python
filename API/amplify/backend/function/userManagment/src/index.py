import json
import os

from requests import HTTPError
from http import HTTPStatus
from functools import wraps
import boto3

#from src.utils.wrapper import exception_handler

def exception_handler(func):
  @wraps(func)
  def wrapper(event, context):
    print(event)

    response = {}

    try:
      
      if event['headers'].get('x-api-key'):
        raise PermissionError('x-api-key is missing')
      
      res = func(event, context)
      if res:
        response['body'] = res

      response['statusCode'] = HTTPStatus.OK

    except HTTPError as error:
      response['error'] = str(error)
      response['statusCode'] = error.response.status_code

    except PermissionError as error:
      response['error'] = str(error)
      response['statusCode'] = HTTPStatus.FORBIDDEN

    except Exception as error:
        response['error'] = str(error)
        response['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR

    return response
  return wrapper



@exception_handler
def handler(event, context):

  user_table_name = os.environ.get('STORAGE_USER_NAME')
  dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
  table = dynamodb.Table(user_table_name)

  user_id= event['headers']['x-api-key']

  res = table.get_item(
    key={'id': user_id}
  )
  data = res.get('Item')
  if not data:
    raise ValueError('User not found')
  
  return data['email']




