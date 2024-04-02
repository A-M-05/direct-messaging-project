# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Abraham Manu
# apmanu@uci.edu
# 26411611

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type','message', 'token'])

def extract_json(json_msg:str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object
    '''

    try:
        json_obj = json.loads(json_msg)
        type = json_obj['response']['type']
        message = json_obj['response']['message']
        try:
            token = json_obj['response']['token']
        except KeyError:
            token = None
    except KeyError:
        try:
            json_obj = json.loads(json_msg)
            type = json_obj['response']['type']
            message = json_obj['response']['messages']
            try:
                token = json_obj['response']['token']
            except KeyError:
                token = None
        except json.JSONDecodeError:
            print("Json cannot be decoded.")
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(type, message, token)
