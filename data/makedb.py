import sqlite3
import pathlib
import os.path
import pandas as pd
from . import extract_trials_data

FILES = [
    'trial_conditions.csv',
    'trial_interventions.csv',
    'trial_locations.csv',
    'trial_race.csv',
    'trial_sex.csv',
    'fda_full.csv',
    'trials.csv',
    'trial_status.csv'

]

#TODO: Handle pathing better

def makedb():

    conn = sqlite3.connect('data/trials.db')
    c = conn.cursor()

    for file in FILES:
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
