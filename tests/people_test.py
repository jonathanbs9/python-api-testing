from pprint import pprint
import pytest
import requests
import random

from assertpy.assertpy import assert_that
from jsonpath_ng import parse
from json import dumps, loads
from requests import status_codes
from utils.read_file import read_file

from requests.models import Response
from config import BASE_URI
from utils.print_helpers import pretty_print
from uuid import uuid4

# Test 'Jonathan' exists
def test_read_all_has_jonathan():
    response = client.read_all_persons()
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(response_text).extracting('fname').is_not_empty().contains('Jonathan')

# Test if a person can be added
def test_new_person_can_be_added():
    unique_last_name = f'User {str(uuid4())}'

    payload = dumps({
        'fname' : 'New',
        'lname' : unique_last_name
    })

    headers = {
        'Content-Type' : 'application/json',
        'Accept' : 'application/json'
    }

    response = requests.post(url=BASE_URI, data=payload, headers=headers)
    assert_that(response.status_code).is_equal_to(204)

    peoples = requests.get(BASE_URI).json()
    
    # is_new_user_created = filter(lambda person: person['lname'] == unique_last_name, peoples)

    new_users = [person for person in peoples if person['lname'] == unique_last_name]
    # assert_that(is_new_user_created).is_true()
    assert_that(new_users).is_not_empty()

def get_all_users():
    response = requests.get(BASE_URI)
    peoples = response.json()
    return peoples, response

def create_new_unique_person():
    unique_last_name = f'User {str(uuid4())}'

    payload = dumps({
        'fname' : 'New',
        'lname' : unique_last_name
    })

    headers = {
        'Content-Type' : 'application/json',
        'Accept' : 'application/json'
    }

    response = requests.post(url=BASE_URI, data=payload, headers=headers)
    assert_that(response.status_code).is_equal_to(204)
    return unique_last_name    

def search_users_by_last_name(peoples, unique_last_name):
    return [person for person in peoples if person['lname'] == unique_last_name]

# Test a person can be deleted
def test_person_can_be_deleted():
    new_user_last_name = create_new_unique_person()
    all_users , _ = get_all_users()
    new_user = search_users_by_last_name(peoples=all_users, unique_last_name=new_user_last_name)[0]
    
    print(new_user)
    person_to_be_deleted = new_user['person_id']

    url = f'{BASE_URI}/{person_to_be_deleted}'
    response = requests.delete(url)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)

@pytest.fixture
def create_data():
    payload = read_file('create_person.json')
    random_nro = random.randint(0,1000)
    last_name = f'Lastname{random_nro}'

    payload['lname'] = last_name
    yield payload

def create_person_with_unique_last_name(body=None):
    if body is None:
        # Ensure a user with a unique last name is created everytime the test runs
        # Note: json.dumps() is used to convert python dict to json string
        unique_last_name = f'User {str(uuid4())}'
        payload = dumps({
            'fname' : 'New',
            'lname' : unique_last_name
        })
    else:
        unique_last_name = body['lname']
        payload = dumps(body)
    
    # Setting default headers to show the client accept
    # and will send json in the headers
    headers = {
        'Content-Type' : 'application/json',
        'Accept' : 'application/json'
    }

# Test person with json template
def test_person_can_be_added_with_a_json_template(create_data):
    create_person_with_unique_last_name(create_data)

    response = requests.get(BASE_URI)
    peoples = loads(response.text)

    # Get All last names for any object in the root array
    # Here $ = root, [*] represents any element in the array
    jsonpath_expr =  parse("$.[*].lname")
    result = [match.value for match in jsonpath_expr.find(peoples)]
