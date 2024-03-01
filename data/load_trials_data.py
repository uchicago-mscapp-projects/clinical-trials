# TODO: Handle relative filepath
import sqlite3
import re
import json
import pandas as pd
import csv
from .recode import RECODE

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

def get_sex_counts(nct_id, row):
    """TODO: Doc string"""
    counts_dict = {'nct_id': nct_id, 'female': None, 'male': None, 'total': None}

    measures = row.get('resultsSection', {})\
            .get('baselineCharacteristicsModule', {}).get('measures', {})

    for measure in measures:
        if measure.get('title') == 'Sex: Female, Male' \
            and measure.get('paramType') == 'COUNT_OF_PARTICIPANTS':

            for cls in measure.get('classes', {}):
                for denom in cls.get('denoms', {}):
                    counts_dict['total'] = denom.get('counts', {})[-1]['value']

            for category in cls.get('categories', {}):
                if category['title'] == 'Female':
                    counts_dict['female'] = \
                        category.get('measurements', {})[-1]['value']
                if category['title'] == 'Male':
                    counts_dict['male'] = \
                        category.get('measurements', {})[-1]['value']
                    
    return counts_dict

def get_race_counts(nct_id, row):
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
                        code = RECODE[cat.get('title')]
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
        sex_counts = get_sex_counts(nct_id, row)
    
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
        race_counts = get_race_counts(nct_id, row)

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
        'TRIAL_LOCATIONS': {'nct_id': [], 'locations': []},
        'TRIAL_INTERVENTIONS': {'nct_id': [], 'intervention_name': []},
        'TRIAL_CONDITIONS': {'nct_id': [], 'conditions': [], 'keywords': []},
    }

    for row in loaded:

        fields =  extract_fields(row)

        for dict_name, dictionary in trial_dicts.items():
                
                for key in dictionary.keys():
                    dictionary[key].append(fields[key])

        
    for dict_name, dictionary in trial_dicts.items():
        df_of_dictionary = pd.DataFrame(dictionary)
        df_of_dictionary.to_csv(f'data/csvs/{dict_name}.csv', index=None)

