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

def generate_trials_data(raw_df, module, headers):
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
    
    filtered = raw_df.filter(module_cols, axis=1)
    return filtered.rename(columns=headers)

def generate_interventions_data(filtered_df):
    """
    Takes a filtered df with the interventions module and normalizes the
    json rows within it, returns a normalized dataframe to be used for
    loading to the database
    """
    exploded = filtered_df.explode(
        'interventions')\
            ['interventions']
    
    # Method for parsing nested JSON data derived from stackoverflow: 
    # https://stackoverflow.com/questions/65942337/how-to-parse-json-column-in-pandas-dataframe-and-concat-the-new-dataframe-to-the
    
    merged = filtered_df.merge(pd.DataFrame(exploded.tolist(), 
        index = exploded.index), left_index=True, right_index=True)
    
    return merged.filter(['nct_id', 'name'])
                        
def generate_baseline_data(filtered_df):
    """
    Takes a filtered df with the baseline characteristics module
    and normalizes the json rows within it, returns a normalized
    dataframe to be used for loading to the database
    """
    pass




    ### CONSIDER: Loops, helper functions ie:
    ##stmod2trials tatus
        ## for all trials ...turn dict to sql rows
        ## 