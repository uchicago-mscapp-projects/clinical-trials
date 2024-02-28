# TODO: Handle relative filepath
import sqlite3
import re
import json
import pandas as pd
import csv

def load_data(filepath):
    """
    Loads returned trials data into a pandas dataframe
    """

    # Load as a series to handle nested data
    from_file = pd.read_json(filepath, typ='series')

    return pd.json_normalize(from_file)

def extract_fields(row):
        """
        Extracts all needed fields from one JSON record returned by the API
        """

        protocol_section = row.get('protocolSection', {})
        identification_module = protocol_section.get('identificationModule', {})
        status_module = protocol_section.get('statusModule', {})
        conditions_module = protocol_section.get('conditionsModule', {})

        fields = {'nct_id': identification_module.get('nctId', {}),
                  
        'brief_title': identification_module.get('briefTitle', {}),

        'official_title': identification_module.get('officialTitle', {}),

        'lead_sponsor': protocol_section.get('sponsorCollaboratorsModule', {})\
            .get('leadSponsor', {}).get('name', {}),

        'overall_status': status_module.get('overallStatus', {}),

        'start_date': status_module.get('startDate', {}),

        'completion_date': status_module.get('completionDate', {}),

        'why_stopped': status_module.get('whyStopped', {}),

        'locations': protocol_section.get('contactsLocationsModule', {})\
            .get('locations', {}),

        'intervention_name': protocol_section.get('armsInterventionsModule', {})\
            .get('interventions', {}),

        'conditions': conditions_module.get('conditions', {}),

        'keywords': conditions_module.get('keywords', {}),
        
        'measures': row.get('resultsSection', {})\
            .get('baselineCharacteristicsModule', {}).get('measures', {})
}
        
        return fields

def filter_nas(value):
    try:
        return(int(value))
    except ValueError:
        return 0 

def get_sex_counts(row):
    counts = {}
    total = 0

    for measure in row:
        if measure.get('title', {}) == 'Sex: Female, Male' and measure.get('paramType', {}) == 'COUNT_OF_PARTICIPANTS':

            for measure_class in measure.get('classes', {}):

                for category in measure_class.get('categories', {}):

                    count = filter_nas(
                        max(
                            category['measurements'], \
                                key=lambda count: filter_nas(count['value']))\
                                    ['value']
                        )

    total += count
    counts['title'] = total

    return counts

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
        'trial_counts_sex': {'nct_id': [], 'Female': [], 'Male': [], 'total': []}
    }

    # TODO: Is there a way to handle this more eloquently?
    for row in loaded:

        # Extract all fields
        fields =  extract_fields(row)

        for dict_name, dictionary in trial_dicts.items():
            if dict_name == 'trial_counts_sex':
                dictionary['nct_id'] = fields['nct_id']
                
                if fields.get('measures', {}):
                    measures = fields.get('measures', {})
                    sex_counts = get_sex_counts(fields.get('measures', {}))
                    
                    for key in sex_counts.keys():
                        dictionary[key].append(sex_counts[key])
            
            else:
                for key in dictionary.keys():
                    dictionary[key].append(fields[key])


    # Create trials csvs
                    
        for dict_name, dictionary in trial_dicts.items():
            print(f"Lengths in {dict_name}:")
            for key, value in dictionary.items():
                print(f"  {key}: {len(value)}")

    # for dict_name, dictionary in trial_dicts.items():
    #     df_of_dictionary = pd.DataFrame(dictionary)
    #     df_of_dictionary.to_csv(f'data/{dict_name}.csv', index=None)