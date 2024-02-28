import requests
import json
import pandas as pd
import time
import urllib.parse
import os.path

import sqlite3
import re
import pandas as pd

def load_data(filepath):
    """
    Loads returned trials data into a pandas dataframe
    """

    # Load as a series to handle nested data
    with open('data/fda.json') as json_file:
        data = json.load(json_file)
    results_list_of_dct = []
    for i in range(len(data)):
        #data[i]['results'] is a list of dictionaries
        page_i_result = data[i]['results']
        for dct in page_i_result:
            submission_status_date = dct.get('submissions',{})
            if submission_status_date:
                submission_status_date = submission_status_date[0].get('submission_status_date',{})
            submission_status = dct.get('submissions',{})
            if submission_status:
                submission_status = submission_status[0].get('submission_status',{})
            application_number = dct.get('application_number',{})
            print("DCT IS",dct)
            print("app number",application_number)
            if 'products' in dct:
                brand_name =  dct.get('products',{})[0].get('brand_name',{})
            sponsor_name = dct.get('sponsor_name',{})
            generic_name = None
            substance_name = None
            manufacturer_name = None
            generic_name = dct.get('openfda',{}).get('generic_name',{})
            if generic_name:
                generic_name = generic_name[0]
            substance_name = dct.get('openfda',{}).get('substance_name',{})
            if substance_name:
                substance_name = substance_name[0]
            manufacturer_name = dct.get('openfda',{}).get('manufacturer_name',{})
            if manufacturer_name:
                manufacturer_name = manufacturer_name[0]
            openfda_brand_name = dct.get('openfda',{}).get('brand_name',{})


            drug_dct = {}
            var_lst = ['submission_status_date','submission_status','application_number',\
                   'brand_name','sponsor_name','generic_name','substance_name','manufacturer_name']
            for var in var_lst:
                drug_dct[var] = locals()[var]
            results_list_of_dct.append(drug_dct)
    return results_list_of_dct

    

                

    
    # from_file = pd.read_json(filepath, typ='series')

    # df = pd.json_normalize(from_file)
    # df['new_results'] = df['results'][0]

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