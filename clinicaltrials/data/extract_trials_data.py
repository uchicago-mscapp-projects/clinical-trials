import json
import pathlib
import pandas as pd
from collapse_race_data import collapse_race_data, \
    WHITE, BLACK, ASIAN, AI_AN, HI_PI, LATINO, NOT_LATINO, MUL, UNK
from collapse_drug_data import recode_trial_drugs

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

        'start_date': status_module.get('startDateStruct', {}).get('date', None),

        'completion_date': status_module.get('primaryCompletionDateStruct', {}).get('date', None),

        'why_stopped': status_module.get('whyStopped', None),

        'locations': protocol_section.get('contactsLocationsModule', {})\
            .get('locations', None),

        'intervention_name': protocol_section.get('armsInterventionsModule', None)\
            .get('interventions', None),

        'conditions': conditions_module.get('conditions', None),

        'keywords': conditions_module.get('keywords', None)
}
        
        return fields

def extract_trial_sex(nct_id, row):
    """
    Extracts race data from a single entry in the json returned by the
    Clinical Trials API.

    Args:
        -- nct_id (str): The nct_id of the row used in extraction.
        -- row (json object): One row in the clinical trials json
        -- recoded_data (dict): A dict of recoded race fields used for
            collapsing race data
    Returns:
        -- dict: A dictionary of extracted race data for one trial
    """
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

def extract_trial_race(nct_id, row, recoded_data):
    """
    Extracts race data from a single entry in the json returned by the
    Clinical Trials API.

    Args:
        -- nct_id (str): The nct_id of the row used in extraction.
        -- row (json object): One row in the clinical trials json
        -- recoded_data (dict): A dict of recoded race fields used for
            collapsing race data
    Returns:
        -- dict: A dictionary of extracted race data for one trial
    """
    
    race_dict = {'nct_id': nct_id,
        AI_AN: None, 
        ASIAN: None, 
        BLACK: None, 
        HI_PI: None, 
        WHITE: None, 
       MUL: None, 
        LATINO: None, 
        NOT_LATINO: None,
       UNK: None}

    measures = row.get('resultsSection', {})\
            .get('baselineCharacteristicsModule', {}).get('measures', {})
    for measure in measures:
        if measure.get('title') in ('Race/Ethnicity, Customized', 'Race (NIH/OMB)') \
            and measure.get('paramType') == 'COUNT_OF_PARTICIPANTS':
            for cls in measure.get('classes', {}):
                for cat in cls.get('categories', {}):
                    if cat.get('title'):
                        code = recoded_data[cat.get('title')]
                        if cat.get('measurements', []):
                            race_dict[code] = cat.get('measurements')[-1]['value']
    return race_dict

## Function written by James Turk
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

## Function written by James Turk
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

## Function written by James Turk
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

## Function written by James Turk
def generate_iv_loc_cond_csvs(filepath):
    """
    Takes the filpath of the raw data JSON file, extracts fields,
    and saves them to separate csvs for loading and manipulation.
    """

    loaded = json.load(open(filepath))

    extraction_functions = {
        "trial_interventions_raw": extract_interventions,
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

        filename = pathlib.Path(__file__).parent / f"../../data/csvs/{dict_name}.csv"
        df.to_csv(filename, index=None)
    
    ## Create recoded file from trial interventions data
    fda_filename = pathlib.Path(__file__).parent / f"../../data/csvs/fda_full.csv"
    interventions_filename =  pathlib.Path(__file__).parent / f"../../data/csvs/trial_interventions_raw.csv"
    recode_trial_drugs(fda_filename, interventions_filename)

def generate_sex_csv(filepath):
    """
    Generates a csv of extracted sex data from the Clinical Trials API.
    """
    sex_counts_final = {'nct_id': [], 'female': [], 'male': [], 'total': []}
    loaded = json.load(open(filepath))

    for row in loaded:
        nct_id = extract_fields(row)['nct_id']
        sex_counts = extract_trial_sex(nct_id, row)
    
        for key in sex_counts.keys():
            sex_counts_final[key].append(sex_counts[key])
    
    filename = pathlib.Path(__file__).parent / f"../../data/csvs/trial_sex.csv"
    df_of_dictionary = pd.DataFrame(sex_counts_final)
    df_of_dictionary.to_csv(filename, index=None)
    
def generate_race_csv(filepath):
    """
    Generates a csv of extracted race data from the Clinical Trials API.
    """
    race_counts_final = {'nct_id': [], AI_AN: [], ASIAN: [], BLACK: [], 
        HI_PI: [], WHITE: [], MUL: [], LATINO: [], NOT_LATINO: [], UNK: []}
    
    loaded = json.load(open(filepath))

    recoded_data = collapse_race_data('data/trials.json', recode_all=True)

    for row in loaded:
        nct_id = extract_fields(row)['nct_id']
        race_counts = extract_trial_race(nct_id, row, recoded_data)

        for key in race_counts.keys():
            race_counts_final[key].append(race_counts[key])
    
    filename = pathlib.Path(__file__).parent / f"../../data/csvs/trial_race.csv"
    df_of_dictionary = pd.DataFrame(race_counts_final)
    df_of_dictionary.to_csv(filename, index=None)

def generate_trial_csvs(filepath):
    """
    Takes the filpath of the raw data JSON file, extracts fields, 
    and saves them to separate csvs for loading and manipulation.
    """

    loaded = json.load(open(filepath))

    trial_dicts = {
        'trials': {'nct_id': [], 'brief_title': [], 'official_title': [], 'lead_sponsor': []},
        'trial_status': {'nct_id': [], 'overall_status': [], 'start_date': [], 'completion_date': [], 'why_stopped': []},
    }

    for row in loaded:
        fields = extract_fields(row)

        for dict_name, dictionary in trial_dicts.items():
            for key in dictionary.keys():
                dictionary[key].append(fields[key])

    for dict_name, dictionary in trial_dicts.items():
        filename = pathlib.Path(__file__).parent / f"../../data/csvs/{dict_name}.csv"
        df_of_dictionary = pd.DataFrame(dictionary)
        df_of_dictionary.to_csv(filename, index=None)

if __name__ == "__main__":
    # generate all five CSVs
    pth = pathlib.Path(__file__).parent / f"../../data/trials.json"
    generate_trial_csvs(pth)
    generate_iv_loc_cond_csvs(pth)
    generate_race_csv(pth)
    generate_sex_csv(pth)
