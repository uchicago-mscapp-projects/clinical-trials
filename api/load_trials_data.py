#TODO: Handle relative filepath
import sqlite3
import re
import pandas as pd


def load_data(filepath):
    """
    Loads returned trials data into a pandas dataframe
    """

    # Load as a series to handle nested data
    from_file = pd.read_json(filepath, typ='series')

    return pd.json_normalize(from_file)

def generate_trials_data(raw_df, module):
    """
    Takes raw data dataframe and groups it into separate tables
    to be loaded to the sqlite3 schema
    """

    columns = raw_df.columns.values.tolist()

    if re.search('identificationModule', module):
        module_cols = []
    
    # Add the unique key if not present in specified module
    else:
        module_cols = ['protocolSection.identificationModule.nctId']
    
    for column in columns:
        if re.search(module, column):
            module_cols.append(column)
    
    return raw_df.filter(module_cols, axis=1)

def generate_baseline_data(filtered_df):
    """
    Takes a filtered df with the baseline characteristics module
    and normalizes the json rows within it, returns a normalized
    dataframe to be used for loading to 
    resultsSection.baselineCharacteristicsModule.measures
    """



    