import requests
from requests import HTTPError


from requests import Session
class TEST():
    def __init__(self):
        self.session = Session()
        self.session.headers={
            'x-api-key': '2ad88799-6ab2-4756-8929-077f97958d2e'
        }

        self.base_url = "https://5ze43vn695.execute-api.eu-west-1.amazonaws.com/dev"

    def get_user(self):
        res= self.session.get(
            url=f"{self.base_url}/manageUser"
        )
        print(res.text)
        res.raise_for_status()
        
 
    
test = TEST()
test.get_user()