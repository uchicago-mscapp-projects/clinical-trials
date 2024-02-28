import requests
import json
import pandas as pd
import time
import urllib.parse
import os.path
from requests_toolbelt.utils import dump

api_url = "https://api.fda.gov/drug/drugsfda.json?api_key=mj3bDfPjrlj49rzSSdysD5pGaKvB6dOEzLSkIfT6&"

def make_fda_api_call(skip, limit=1000):
    """
    #TODO: add URL and search_param back in as parameters?
    Makes an API call to FDA's Drugs@FDA API.

    Args:
        - Fields, list: A list of fields to be returned from the API

    Returns:
        - Dict: The returned JSON payload from the API call, and the 
        string value of the next page token
    """
    #count=openfda.generic_name.exact
    #fields = '|'.join(fields)
    # payload = {'fields': fields, 'query.intr': 'DRUG', 'pageToken':pageToken,
    #            'pageSize': limit  
    #            }
    print("in make, skip is", skip)
    #payload = {'search': search_param, 'limit': limit, 'skip': skip}
    #The FDA API has issues with special characters. Line below ensures it 
    #doesn't misinterpret the url.
    base_url = 'https://api.fda.gov/drug/drugsfda.json?api_key=mj3bDfPjrlj49rzSSdysD5pGaKvB6dOEzLSkIfT6&search=submissions.submission_status_date%5B2003-01-01%20TO%202024-02-19%5D'
    second_part_url = '&skip=' + str(skip) + '&limit=1000'
    url = base_url + second_part_url
    #payload_str = urllib.parse.urlencode(payload, safe=':+')
    response = requests.get(url) 
    if response.status_code != 200:
        print(response.content)
        data = dump.dump_all(response)
        print(data.decode('utf-8'))
        return None 
    return response.json()


def pull_api_trials_data(skip, limit=1000):
    results = []
    while True:
        print("got back here")
        time.sleep(2)
        fxcall = make_fda_api_call(skip, limit=1000)
        if fxcall is None:
            print("in the none")
            break
        # if not response.status_code == 200:
        #     print("in the first not")
        #     break
        # if not mydict:
        #     print("in the second not")
        #     break
        results.append(fxcall)
        skip += limit
        # if skip >= 10000:
        #     write_data(results, 'fda', append=False)
        #     break
        print("we incremented skip", skip)
        write_data(results, 'fda', append=False)
    #return results
    #     else:
    #         print("got to else")
    #         break
    #     print("skip is", skip)
    # return results

# def fetch_page_results(url, search_param, skip=0, limit=1000):
#     params = {'search': search_param, 'skip': skip, 'limit': limit}
#     response = requests.get(url, params=params)
    
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Failed to fetch page: {response.status_code}")
#         return None








    #put skip and limit and submission date in payload. 
    #check for none found and then 
    #by 21st get json, then 21-24 filter etc. get into sql.
    
    
    # r.raise_for_status()

    # return r

    #on when to stop: said could also do while loop and then when don't see total
#in that top dictionary anymore, stop. or when do see error. etc.

    #https://api.fda.gov/drug/drugsfda.json?search=submissions.submission_status_date[2004-01-01+TO+2005-01-01]


# try:
#     r = requests.get("https://api.fda.gov/drug/drugsfda.json?search=submissions.submission_status_date[2003-01-01+TO+2024-02-19]&skip=19855&limit=1000")
#     r.raise_for_status()

# ##find way to break out of loop. incorporate when to stop is when we find error. 
# except HTTPError:
#     print(r)
        
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
    
    #filename = os.path.join('./data', source + '.json')
    #filename = datatest.json
    filename = os.path.join('./data', source + '.json')
    with open(filename, mode=mode) as f:
            f.write(json.dumps(data))