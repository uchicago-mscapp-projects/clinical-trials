import requests
import json
import time
import os.path
import pathlib

# TODO: Examine data
# TODO: Implement API call class function?


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


def make_fda_api_call(skip, limit=1000, start_date="2003-01-01", end_date="2024-02-19"):
    """
    Makes an API call to FDA's Drugs@FDA API.

    Args:
        - skip: (int) value initially sent to 0. used to paginate.
        - limit: (int) the maximum number of results that can be returned from
        each API query. The API sets this to 1000.
        -start_date: (str) the start date of submission_status_date used in 
        results. For the project, this is set to the start of 2003 to align with
        the clinical trials data (this is approximately when clinical trials
        data is first available from)
        -end_date: (str) the end date of submission_status_date used in 
        results. For the project, this is set to 2/19/2024 to align with our 
        final data collection.

    Returns:
        - response.json(): the json file for that specific page and query.
    """

    base_url = "https://api.fda.gov/drug/drugsfda.json?search=submissions.submission_status_date"
    # FDA API has trouble parsing parameters, which is why the url is being input
    # into requests as a string.
    second_part_url = "%5B" + start_date + "%20TO%20" + end_date + "%5D"
    third_part_url = "&skip=" + str(skip) + "&limit=" + str(limit)
    url = base_url + second_part_url + third_part_url
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


def pull_fda_api_data(
    skip=0, limit=1000, start_date="2003-01-01", end_date="2024-02-19"
):
    """
    Pull data for the given time frame from the Drugs@FDA API.

    Args:
        - skip: (int) value initially sent to 0. used to paginate.
        - limit: (int) the maximum number of results that can be returned from
        each API query. The API sets this to 1000.
        -start_date: (str) the start date of submission_status_date used in 
        results. For the project, this is set to the start of 2003 to align with
        the clinical trials data (this is approximately when clinical trials 
        data is first available from)
        -end_date: (str) the end date of submission_status_date used in 
        results. For the project, this is set to 2/19/2024 to align with our 
        final data collection.

    Returns:
        - Writes data from the API out to a json file.
    """
    results = []
    while True:
        next_results = skip + 1000

        print(f"Pulling FDA trial results {skip} to {next_results}")
        
        time.sleep(2)
        
        apicall = make_fda_api_call(
            skip, limit=1000, start_date=start_date, end_date=end_date
        )
        if apicall is None:
            break
        results.append(apicall)
        skip += limit
        write_data(results, "fda", append=False)


if __name__ == "__main__":
    pull_fda_api_data()
    pull_trials_data()
