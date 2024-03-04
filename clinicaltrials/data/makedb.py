import sqlite3
import pathlib
import pandas as pd

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

def makedb():
    db_pth = pathlib.Path(__file__).parent / f"../../data/trials.db"
    conn = sqlite3.connect(db_pth)
    c = conn.cursor()

    for file in FILES:
        filepath = pathlib.Path(__file__).parent / f"../../data/csvs/{file}"
        df = pd.read_csv(f'data/csvs/{file}')
        table_name = file.split('.')[0]

        df.to_sql(table_name, con=conn, if_exists='replace', index=False)
    
    #Read transformations SQL script
    sql_file = pathlib.Path(__file__).parent / "transformations.sql"
    with open (sql_file, 'r') as sql:
        sql = sql.read()
        c.executescript(sql)

    c.close()

if __name__ == "__main__":
    makedb()
