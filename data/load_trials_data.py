# TODO: Handle relative filepath
import sqlite3
import re
import json
import pandas as pd
import csv
from .recode import RECODED

def extract_fields(row):
        """
        Extracts all needed fields from one JSON record returned by the API
        """

        protocol_section = row.get('protocolSection', {})
        identification_module = protocol_section.get('identificationModule', {})
        status_module = protocol_section.get('statusModule', {})
        conditions_module = protocol_section.get('conditionsModule', {})

        fields = {'nct_id': identification_module.get('nctId', {}),
                  
        'brief_title': identification_module.get('briefTitle', None),

        'official_title': identification_module.get('officialTitle', None),

        'lead_sponsor': protocol_section.get('sponsorCollaboratorsModule', {})\
            .get('leadSponsor', {}).get('name', None),

        'overall_status': status_module.get('overallStatus', None),

        'start_date': status_module.get('startDate', None),

        'completion_date': status_module.get('completionDate', None),

        'why_stopped': status_module.get('whyStopped', None),

        'locations': protocol_section.get('contactsLocationsModule', {})\
            .get('locations', None),

        'intervention_name': protocol_section.get('armsInterventionsModule', None)\
            .get('interventions', None),

        'conditions': conditions_module.get('conditions', None),

        'keywords': conditions_module.get('keywords', None)
        
        # 'measures': row.get('resultsSection', {})\
        #     .get('baselineCharacteristicsModule', {}).get('measures', {})
}
        
        return fields

def filter_nas(value):
    try:
        return(int(value))
    except ValueError:
        return 0 

def extract_trial_sex(nct_id, row):
    """TODO: Doc string"""
    counts_dict = {'nct_id': nct_id, 'female': None, 'male': None, 'total': None}

    measures = row.get('resultsSection', {})\
            .get('baselineCharacteristicsModule', {}).get('measures', {})

    for measure in measures:
        if measure.get('title') == 'Sex: Female, Male' \
            and measure.get('paramType') == 'COUNT_OF_PARTICIPANTS':

            for cls in measure.get('classes', []):
                for denom in cls.get('denoms', {}):
                    counts_dict['total'] = denom.get('counts', {})[-1]['value']

            for category in cls.get('categories', {}):
                if category['title'] == 'Female':
                    if category.get('measurements'):
                        counts_dict['female'] = \
                            category.get('measurements')[-1]['value']
                if category['title'] == 'Male':
                    if category.get('measurements'):
                        counts_dict['male'] = \
                            category.get('measurements')[-1]['value']
                    
    return counts_dict

def extract_trial_race(nct_id, row):
    """TODO: Doc string"""
    
    race_dict = {'nct_id': nct_id,
        'american_indian_or_alaska_native': None, 
        'asian': None, 
        'black': None, 
        'hawaiian_or_pacific_islander': None, 
        'white': None, 
        'multiple': None, 
        'hispanic_or_latino': None, 
        'not_hispanic_or_latino': None,
        'unknown': None}

    measures = row.get('resultsSection', {})\
            .get('baselineCharacteristicsModule', {}).get('measures', {})
    for measure in measures:
        if measure.get('title') in ('Race/Ethnicity, Customized', 'Race (NIH/OMB)') \
            and measure.get('paramType') == 'COUNT_OF_PARTICIPANTS':
            for cls in measure.get('classes', {}):
                for cat in cls.get('categories', {}):
                    if cat.get('title'):
                        code = RECODED[cat.get('title')]
                        race_dict[code] = cat.get('measurements')[-1]['value']
    return race_dict

def generate_sex_csv(filepath):
    """
    TODO: Doc string
    """
    sex_counts_final = {'nct_id': [], 'female': [], 'male': [], 'total': []}
    loaded = json.load(open(filepath))

    for row in loaded:
        nct_id = extract_fields(row)['nct_id']
        sex_counts = extract_trial_sex(nct_id, row)
    
        for key in sex_counts.keys():
            sex_counts_final[key].append(sex_counts[key])
    
    df_of_dictionary = pd.DataFrame(sex_counts_final)
    df_of_dictionary.to_csv(f'data/csvs/TRIAL_COUNTS_SEX.csv', index=None)
    
def generate_race_csv(filepath):
    race_counts_final = {'nct_id': [],
    'american_indian_or_alaska_native': [], 
    'asian': [], 
    'black': [], 
    'hawaiian_or_pacific_islander': [], 
    'white': [], 
    'multiple': [], 
    'hispanic_or_latino': [], 
    'not_hispanic_or_latino': [],
        'unknown': []}
    
    loaded = json.load(open(filepath))

    for row in loaded:
        nct_id = extract_fields(row)['nct_id']
        race_counts = extract_trial_race(nct_id, row)

        for key in race_counts.keys():
            race_counts_final[key].append(race_counts[key])
    
    df_of_dictionary = pd.DataFrame(race_counts_final)
    df_of_dictionary.to_csv(f'data/csvs/TRIAL_COUNTS_RACE.csv', index=None)

def generate_trial_csvs(filepath):
    """
    Takes the filpath of the raw data JSON file, extracts fields, 
    and saves them to separate csvs for loading and manipulation.
    """

    loaded = json.load(open(filepath))

    trial_dicts = {
        'TRIALS': {'nct_id': [], 'brief_title': [], 'official_title': [], 'lead_sponsor': []},
        'TRIAL_STATUS': {'nct_id': [], 'overall_status': [], 'start_date': [], 'completion_date': [], 'why_stopped': []},
    }

    for row in loaded:
        fields = extract_fields(row)

        for dict_name, dictionary in trial_dicts.items():
            for key in dictionary.keys():
                dictionary[key].append(fields[key])

    for dict_name, dictionary in trial_dicts.items():
        df_of_dictionary = pd.DataFrame(dictionary)
        df_of_dictionary.to_csv(f'data/csvs/{dict_name}.csv', index=None)

"""
Explanation of below functions.

- extract_interventions
- extract_trial_locations
- extract_trial_conditions
- generate_trial_csvs_func

A given 'row' represented by fields sometimes needs to turn into one
output row, and sometimes many.

You could write this as:

output_rows = []
for sub_type in fields[sub_field]:
    output_rows.append({...})
return output_rows

Where, for example, in the case of locations, the {...}
would be a {nct_id, city, country} dictionary.

Then, in generate_trial_csvs_func
we use "extend" instead of "append" to grow our list of
results by as few as one (where output_rows would only be len==1 if a
single location (or intervention, etc.) occurred.

This is a very common pattern, and I am using generators to do it.
A generator function essentially returns multiple values, so the
code here is equivalent to building lists of output_rows and then
returning them, except for simplicity's stake, I just yield
them one at a time.

The "extend" calls in generate_trial_csvs_func still work as they
would have if lists were returned.
"""


def extract_interventions(fields):
    """
    Take a 'fields' object from extract_fields and build a
    nct,intervention_name dictionary.
    """
    for intervention in fields["intervention_name"]:
        yield {
            "nct_id": fields["nct_id"],
            "intervention_name": intervention["name"],
        }

def extract_trial_locations(fields):
    """
    Take a 'fields' object from extract_fields and build a
    nct_id, city, country dictionary
    """
    for loc in fields["locations"]:
        yield {
            "nct_id": fields["nct_id"],
            "city": loc["city"],
            "country": loc["country"],
        }

def extract_trial_conditions(fields):
    """
    Take a 'fields' object from extract fields and build a
    nct_id, condition, keywords dictionary
    """
    for cond in fields["conditions"]:
        keywords_flat = " ".join(fields["keywords"] or [])
        yield {
            "nct_id": fields["nct_id"],
            "condition": cond,
            "keywords": keywords_flat,
        }
    # TODO: what do you want to do with keywords & conditions here?
    # do you want one row for each condition and one row for each
    # keyword?
    # I wasn't sure, so for now I generate one row per condition
    # and flatten keywords into a single row.
    # You could change this, or let me know the intent and I can
    # suggest the right path forward.

def generate_trial_csvs_func(filepath):
    """
    Takes the filpath of the raw data JSON file, extracts fields,
    and saves them to separate csvs for loading and manipulation.
    """

    loaded = json.load(open(filepath))

    extraction_functions = {
        "trial_interventions": extract_interventions,
        "trial_locations": extract_trial_locations,
        "trial_conditions": extract_trial_conditions,
    }

    for dict_name, extraction_func in extraction_functions.items():
        ext_data = []
        for row in loaded:
            # API object 'row' -> nested dict 'fields'
            fields = extract_fields(row)
            # each fields object returns >=1 output row
            ext_data.extend(extraction_func(fields))
        df = pd.DataFrame(ext_data)
        df.to_csv(f'data/csvs/{dict_name}.csv', index=None)

if __name__ == "__main__":
    # generate all five CSVs
    generate_trial_csvs('data/trials.json')
    generate_trial_csvs_func('data/trials.json')
    generate_race_csv('data/trials.json')
    generate_sex_csv('data/trials.json')
