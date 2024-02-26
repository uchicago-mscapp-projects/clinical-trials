# TODO: Handle relative filepath
import sqlite3
import re
import json
import pandas as pd

def load_data(filepath):
    """
    Loads returned trials data into a pandas dataframe
    """

    # Load as a series to handle nested data
    from_file = pd.read_json(filepath, typ='series')

    return pd.json_normalize(from_file)

#TODO: This is very slow. How can this be improved?

def generate_trial_csvs(filepath):
    """
    Takes the filpath of the raw data JSON file, extracts fields, 
    and saves them to separate csvs for loading and manipulation.
    """

    loaded = json.load(open(filepath))

    trial_dicts = {
        'trials': {'nct_id': [], 'brief_title': [], 'official_title': [], 'lead_sponsor': []},
        'trial_status': {'nct_id': [], 'overall_status': [], 'start_date': [], 'completion_date': [], 'why_stopped': []},
        'trial_locations': {'nct_id': [], 'locations': []},
        'trial_interventions': {'nct_id': [], 'intervention_name': []},
        'trial_conditions': {'nct_id': [], 'conditions': [], 'keywords': []},
        'trial_baseline_measures': {'nct_id': [], 'measures': []}
    }

    for row in loaded:

        # Extract all fields
        protocol_section = row.get('protocolSection')
        identification_module = protocol_section.get('identificationModule')
        status_module = protocol_section.get('statusModule')
        conditions_module = protocol_section.get('conditionsModule')

        fields = {'nct_id': identification_module.get('nctId'),
        'brief_title': identification_module.get('briefTitle'),
        'official_title': identification_module.get('officialTitle'),
        'lead_sponsor': protocol_section.get('sponsorCollaboratorsModule')\
            .get('leadSponsor').get('name'),
        'overall_status': status_module.get('overallStatus'),
        'start_date': status_module.get('startDate'),
        'completion_date': status_module.get('completionDate'),
        'why_stopped': status_module.get('whyStopped'),
        'locations': protocol_section.get('contactsLocationsModule')\
            .get('locations'),
        'intervention_name': protocol_section.get('armsInterventionsModule')\
            .get('interventions'),
        'conditions': conditions_module.get('conditions'),
        'keywords': conditions_module.get('keywords'),
        'measures': row.get('resultsSection', {})\
            .get('baselineCharacteristicsModule', {}).get('measures')
                  }
    
        for dict_name, dictionary in trial_dicts.items():
            for key in dictionary.keys():
                dictionary[key].append(fields[key])

    # Create trials csvs
                
    for dict_name, dictionary in trial_dicts.items():
        df_of_dictionary = pd.DataFrame(dictionary)
        df_of_dictionary.to_csv(f'data/{dict_name}.csv', sep='|')