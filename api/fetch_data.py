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

    fields = '|'.join(fields)
    payload = {'fields': fields, 'query.intr': 'DRUG', 'pageToken':pageToken,
               'pageSize': limit}
    
    r = requests.get(
        'https://www.clinicaltrials.gov/api/v2/studies', params=payload)
    
    r.raise_for_status()

    print(r.url)

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

def pull_trials_data(limit_per_call, limit_total):
    """
    Pulls trials data, and writes it to a JSON file.
    Args:
        limit_per_call (int): The maximum number of calls to return per
            call to the api. Cannot be more than 1000.
        limit_total (int): The maximum total number of records to return.
    """


    print(f"Making initial API call for records between 0 and {limit_per_call}")

    # Make initial API call, grab next page token to handle in for loop
    results = make_trials_api_call().json()
    
    count_results = limit_per_call
    
    next_page_token = results['nextPageToken']

    # Overwrite pre-existing data for this first call, append for later calls
    # in the loop
    
    write_data(results, 'trials', append=False)

    # Counter set for testing purposes

    while next_page_token and count_results + limit_per_call <= limit_total:
        time.sleep(2)
        
        next_results = count_results + limit_per_call

        print(f"Making API call for records {count_results} through \
              {next_results}")
        
        results = make_trials_api_call(
             limit=limit_per_call, pageToken=next_page_token).json()
        
        count_results += limit_per_call
        
        write_data(results, 'trials')

