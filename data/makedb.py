import json
import sqlite3
import pathlib

# Code adapted from PA3
def schema():
    return """
    CREATE TABLE trials (
    nct_id VARCHAR PRIMARY_KEY
    , brief_title VARCHAR
    , official_title VARCHAR
    );    
    """

# TODO: This feels a bit unsustainable for the extremely nested JSON we have, either
# figure out a more officient way to handle this or pull fewer fields from the API
def makedb():
    """ (re)create database from a normalized_parks.json from PA #2 """
    
    # remove database if it exists already
    path = pathlib.Path("data/trials.db")
    path.unlink()
    
    # connect to fresh database & create tables
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.executescript(schema())

    with open("data/trials.json") as f:
        trials = json.load(f)
        
    # need id_ for generate_times & easy access to foreign key
    for _, trial in enumerate(trials):

        
        # TODO: Is there a more efficient way to do this?
        c.execute(
            "INSERT INTO trials (nct_id, brief_title, official_title) VALUES (?, ?, ?)",
            (
                trial['protocolSection']['identificationModule']['nctId'],
                trial['protocolSection']['identificationModule']['briefTitle'],
                trial['protocolSection']['identificationModule'].get('officialTitle', None)
            ),
        )

        c.execute("COMMIT")
    c.close()


if __name__ == "__main__":
    makedb()