from json import dumps
from uuid import uuid4

from clients.people.base_client import BaseClient
from config import BASE_URI
#from utils.request import APIRequest


class PeopleClient(BaseClient):
    def __init__(self) :
        super().__init__()

        self.base_url = BASE_URI
        #self.request = APIRequest()

#    def create_person(self, body=None):
        
