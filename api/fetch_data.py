import requests
import json
import pandas as pd
import os.path
import time

API_URL = 'https://www.clinicaltrials.gov/api/v2/studies'

def make_trials_api_call(
        fields=['BaselineMeasure', 'StatusModule', 'ConditionSearch', 
                'InterventionType'], limit=10,
                         next_page = False) -> {json, str}:
    """
    Makes an API call to NIH's clinical trials API.

    Args:
        - Fields, list: A list of fields to be returned from the API

    Returns:
        - Dict: The returned JSON payload from the API call, and the 
        string value of the next page token
    """

    FIELDS = '|'.join(fields)
    pageToken = None
    payload = {'fields': FIELDS, 'query.intr': 'DRUG', 'pageToken':pageToken}
    
    r = requests.get(
        'https://www.clinicaltrials.gov/api/v2/studies', params=payload)

    return r

def write_data(data, filename, append=True):
    """
    Writes data returned by an API call to a JSON file format.
    
    Args:
        data (JSON): Data returned from an API call
        filename ('str'): The name of the file to write to
        append (bool): Default to true. If true, will append to the filename
        wrather than overwrite it.
    
    Returns:
        Creates or appends to the file specified.
    """
    if append:
        mode = 'a'
    else:
        mode = 'w'
    
    with open(filename, mode=mode) as f:
            f.write(json.dumps(data))

def pull_trials_data():
    """
    Pulls trials data, and writes it to a JSON file.
    """
    pass 

##TODO: Handle waits, next page token
##TODO: Handle adding to json file, not overrwriting
#nextPageToken = ''
#while nextPageToken:

