import sqlite3
import pathlib
import os.path
import pandas as pd
from . import load_trials_data

#TODO: Handle pathing better
# TODO: Group by for drug, condition, participant diversity counts
# YEAR, MANUFACTURER, DEMOGRAPHICS, DRUG, CONDITION, DRUG TYPE

# Code adapted from PA3
def schema():
    return """
    CREATE TABLE TRIALS (
    nct_id VARCHAR PRIMARY KEY
    , brief_title VARCHAR
    , official_title VARCHAR
    , lead_sponsor
    );

    CREATE TABLE TRIAL_STATUS (
    nct_id VARCHAR PRIMARY KEY
    , status_verified_date DATE
    , overall_status VARCHAR
    , start_date DATE
    , completion_date
    , last_known_status VARCHAR
    , why_stopped VARCHAR
    );

    CREATE TABLE TRIAL_LOCATIONS (
    nct_id VARCHAR
    , city VARCHAR
    , country VARCHAR
    );

    CREATE TABLE TRIAL_INTERVENTIONS (
    nct_id VARCHAR
    , intervention_name
    );

    CREATE TABLE TRIAL_CONDITIONS (
    nct_id VARCHAR
    , condition
    , keywords
    );

    CREATE TABLE TRIAL_COUNTS_RACE (
    nct_id VARCHAR PRIMARY KEY
    , race
    , total
    );

    CREATE TABLE TRIAL_COUNTS_SEX (
    nct_id VARCHAR PRIMARY KEY
    , female
    , male
    , total
    );
    """

def makedb():

    path = pathlib.Path("data/trials.db")
    path.unlink()

    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.executescript(schema())

    load_trials_data.generate_trial_csvs('data/trials.json')

    for file in os.listdir('data/csvs'):
        df = pd.read_csv(f'data/csvs/{file}')
        table_name = file.split('.')[0]

        df.to_sql(table_name, con=conn, if_exists='append', index=False)
    
    c.close()

if __name__ == "__main__":
    makedb()