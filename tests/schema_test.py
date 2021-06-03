import json
from assertpy.assertpy import soft_assertions

import requests
from assertpy import assert_that
from cerberus import Validator, Validator

from config import BASE_URI

schema = {
    "fname" : {'type': 'string', 'required': True},
    "lname" : {'type': 'string'},
    "person_id" : {'type': 'number'},
    "timestamp" : {'type': 'string'}
}

def test_read_one_operation_has_expected_schema():
    response = requests.get(f'{BASE_URI}/4')
    print(response)
    person = json.loads(response.text)

    validator = Validator(schema, require_all=True)
    is_valid = validator.validate(person) # returns true/false 

    assert_that(is_valid, description=validator.errors).is_true() # if fails, write a description

def test_read_all_operations_has_expected_schema():
    response = requests.get(f'{BASE_URI}')
    print(response)
    persons = json.loads(response.text)
    validator = Validator(schema, require_all=True)
    
    with soft_assertions():
        for person in persons:
            is_valid = validator.validate(person) # returns true/false 
            assert_that(is_valid, description=validator.errors).is_true() # if fails, write a description