import requests
import json
import pandas as pd
import time

API_URL = 'https://www.clinicaltrials.gov/api/v2/studies'

def make_trials_api_call(
        fields=['BaselineMeasure', 'StatusModule', 'ConditionSearch'], 
                         next_page = False) -> {json, str}:
    """
    Makes an API call to NIH's clinical trials API.

    Args:
        - Fields, list: A list of fields to be returned from the API

    Returns:
        - Dict: The returned JSON payload from the API call, and the 
        string value of the next page token
    """
    FIELDS = '?fields=BaselineMeasure|StatusModule|ConditionSearch'
    token = ''

    
    r = requests.get(
        'https://www.clinicaltrials.gov/api/v2/studies' + f'{{FIELDS}}')

##TODO: Handle waits, next page token
##TODO: Handle adding to json file, not overrwriting
nextPageToken = ''
while nextPageToken:
