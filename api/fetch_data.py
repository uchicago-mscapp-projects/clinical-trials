import requests
import json
import time
import pandas as pd
import os.path


# TODO: Handle creating/overwriting files
# TODO: Handle converting JSON to readable/searchable type
# TODO: Examine data
# TODO: Implement API call class function?


API_URL = 'https://www.clinicaltrials.gov/api/v2/studies'

def make_trials_api_call(
        fields=['BaselineMeasure', 'StatusModule', 'ConditionSearch', 
                'InterventionType'], limit=10,
                         pageToken = None) -> {json, str}:
    """
    Makes an API call to NIH's clinical trials API.

    Args:
        - Fields, list: A list of fields to be returned from the API

    Returns:
        - Dict: The returned JSON payload from the API call, and the 
        string value of the next page token
    """

    FIELDS = '|'.join(fields)
    payload = {'fields': FIELDS, 'query.intr': 'DRUG', 'pageToken':pageToken}
    
    r = requests.get(
        'https://www.clinicaltrials.gov/api/v2/studies', params=payload)
    
    r.raise_for_status()

    return r

def write_data(data, source, append=True):
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
    
    filename = os.path.join('./data', source + '.json')
    with open(filename, mode=mode) as f:
            f.write(json.dumps(data))

def pull_trials_data(limit):
    """
    Pulls trials data, and writes it to a JSON file.
    """
    count_results = 0
    print(f"Making initial API call for records between 0 and {limit}")
    results = make_trials_api_call().json()
    count_results += len(results)
    next_page_token = results['nextPageToken']

    count = 0
    while next_page_token and count < 3:
        time.sleep(2)
        count += 1
        print('Making API call')
        results = make_trials_api_call(
             limit=limit, pageToken=next_page_token).json()
        write_data(results, 'trials')

