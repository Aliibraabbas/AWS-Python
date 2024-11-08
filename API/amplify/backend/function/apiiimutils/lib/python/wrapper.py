from requests import HTTPError
from http import HTTPStatus
from functools import wraps

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