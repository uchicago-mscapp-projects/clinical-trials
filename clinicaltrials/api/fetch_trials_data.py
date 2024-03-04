## Written by Caitlin Pratt

import requests
import json
import time
import pathlib

API_URL = 'https://www.clinicaltrials.gov/api/v2/studies'

API_FIELDS = ['NCTId', 'BriefTitle', 'OfficialTitle', 'Condition',
              'StatusModule', 'InterventionName', 'InterventionOtherName',
              'Phase', 'BriefSummary', 'Keyword', 'ArmGroupLabel',
              'InterventionDescription', 'ArmGroupDescription',
              'LeadSponsorName', 'LocationCity', 'LocationCountry',
              'StudyType', 'BaselineCharacteristicsModule']


def make_trials_api_call(
    fields, limit_per_call,
        pageToken=None,
) -> {json, str}:
    """
    Makes an API call to NIH's clinical trials API.

    Args:
        - Fields, list: A list of fields to be returned from the API

    Returns:
        - Dict: The returned JSON payload from the API call, and the
        string value of the next page token
    """

    fields = '|'.join(fields)
    payload = {'fields': fields, 'query.intr': 'AREA[InterventionType]DRUG',
               'pageToken': pageToken, 'pageSize': limit_per_call,
               'postFilter.advanced':
               'AREA[IsFDARegulatedDrug]true AND AREA[Phase](PHASE3 OR PHASE4)',
               'query.locn': 'AREA[LocationCountry]United States'}

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
        None. Creates or appends to the file specified.
    """

    if append:
        mode = 'a'
    else:
        mode = 'w'

    pth = pathlib.Path(__file__).parent / f"../../data/{source}.json"

    with open(pth, mode=mode) as f:
        f.write(json.dumps(data))


def pull_trials_data(limit_per_call=1000, limit_total=float('inf'),
                     fields=API_FIELDS):
    """
    Pulls trials data, and writes it to a JSON file.
    Args:
        limit_per_call (int): The maximum number of calls to return per
            call to the api. Cannot be more than 1000.
        limit_total (int): The maximum total number of records to return.
    """

    print(
        f"Making initial API call for records between 0 and {limit_per_call}"
    )

    # Make initial API call, grab next page token to handle in for loop
    results = []

    response = make_trials_api_call(
        limit_per_call=limit_per_call, fields=fields).json()

    results = response['studies']

    count_results = limit_per_call

    next_page_token = response['nextPageToken']

    while next_page_token and count_results + limit_per_call <= limit_total:
        time.sleep(2)

        try:
            next_results = count_results + limit_per_call

            print(f"Pulling clinical trial records {count_results} to {next_results}")

            response = make_trials_api_call(limit_per_call=limit_per_call,
                                            fields=fields, pageToken=next_page_token).json()

            next_page_token = response['nextPageToken']

            results.extend(response['studies'])

            count_results += limit_per_call

        except KeyError:
            print("API pull complete.")
            results.extend(response['studies'])
            break

    write_data(results, 'trials', append=False)

if __name__ == "__main__":
    pull_trials_data()
