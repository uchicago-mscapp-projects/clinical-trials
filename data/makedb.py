import sqlite3
import pathlib
import os.path
import pandas as pd
from . import extract_trials_data

#TODO: Handle pathing better
# TODO: Group by for drug, condition, participant diversity counts
# YEAR, MANUFACTURER, DEMOGRAPHICS, DRUG, CONDITION, DRUG TYPE

# Code adapted from PA3
def schema():
    return """
    CREATE TABLE trials (
    nct_id VARCHAR PRIMARY KEY
    , brief_title VARCHAR
    , official_title VARCHAR
    , lead_sponsor VARCHAR
    );

    CREATE TABLE trial_status (
    nct_id VARCHAR PRIMARY KEY
    , status_verified_date DATE
    , overall_status VARCHAR
    , start_date DATE
    , completion_date DATE
    , last_known_status VARCHAR
    , why_stopped VARCHAR
    );

    CREATE TABLE trial_locations (
    nct_id VARCHAR
    , city VARCHAR
    , country VARCHAR
    );

    CREATE TABLE trial_interventions (
    nct_id VARCHAR
    , intervention_name VARCHAR
    );

    CREATE TABLE trial_conditions (
    nct_id VARCHAR
    , condition VARCHAR
    , keywords VARCHAR
    );

    CREATE TABLE trial_race (
    nct_id VARCHAR PRIMARY KEY
    , american_indian_or_alaska_native INTEGER
    , asian INTEGER
    , black INTEGER
    , hawaiian_or_pacific_islander INTEGER
    , white INTEGER
    , multiple INTEGER
    , hispanic_or_latino INTEGER
    , not_hispanic_or_latino INTEGER
    , unknown INTEGER
    , total INTGER
    );

    CREATE TABLE trial_sex (
    nct_id VARCHAR PRIMARY KEY
    , female INTEGER
    , male INTEGER
    , total INTEGER
    );
    
    CREATE TABLE fda_full (
    application_number VARCHAR PRIMARY KEY
   , submission_status_date VARCHAR
   , submission_status VARCHAR
   , brand_name VARCHAR
   , sponsor_name VARCHAR
   , substance_name VARCHAR
   , generic_name VARCHAR
   , manufacturer_name VARCHAR
   );

    """

def makedb():

    conn = sqlite3.connect('data/trials.db')
    c = conn.cursor()

    extract_trials_data.generate_trial_csvs_func('data/trials.json')

    for file in os.listdir('data/csvs'):
        df = pd.read_csv(f'data/csvs/{file}')
        table_name = file.split('.')[0]

        df.to_sql(table_name, con=conn, if_exists='replace', index=False)
    

    #Read transformations SQL script
    with open ('data/transformations.sql', 'r') as sql:
        sql = sql.read()
        c.executescript(sql)

    c.close()

if __name__ == "__main__":
    makedb()
