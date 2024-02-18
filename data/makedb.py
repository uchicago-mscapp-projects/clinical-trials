import json
import sqlite3
import pathlib
import load_trials_data
import trial_headers

#TODO: Handle pathing better

# Code adapted from PA3
def schema():
    return """
    CREATE TABLE TRIALS (
    nct_id VARCHAR PRIMARY KEY
    , brief_title VARCHAR
    , official_title VARCHAR
    );

    CREATE TABLE TRIAL_STATUS (
    nct_id VARCHAR PRIMARY KEY
    , status_verified_date DATE
    , overall_status VARCHAR
    , has_expanded_access BOOLEAN
    , start_date DATE
    , primary_completion_date DATE
    , primary_completion_date_type VARCHAR
    , completion_date DATE
    , completion_date_type VARCHAR
    , first_submit_date DATE
    , first_submit_qc_date DATE
    , first_post_date DATE
    , first_post_date_type VARCHAR
    , results_first_submit_date DATE
    , results_first_submit_qc_date DATE
    , results_first_post_date DATE
    , results_first_post_date_type VARCHAR
    , last_update_submit_date DATE
    , last_update_post_date DATE
    , last_update_post_date_type VARCHAR
    , start_date_type VARCHAR
    , disp_first_submit_date DATE
    , disp_first_submit_qc_date DATE
    , disp_first_post_date DATE
    , disp_first_post_date_type VARCHAR
    , last_known_status VARCHAR
    , why_stopped VARCHAR
    );
    
    """

# TODO: This feels a bit unsustainable for the extremely nested JSON we have, either
# figure out a more officient way to handle this or pull fewer fields from the API
def makedb():

    path = pathlib.Path("data/trials.db")
    path.unlink()

    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.executescript(schema())

    raw_data = load_trials_data.load_data('data/trials.json')

    trials_data = load_trials_data.generate_trials_data(raw_data, 
            'identificationModule', trial_headers.trials_headers)
    
    trials_data.to_sql('TRIALS', con=conn, if_exists='append', index=False)

    status_data = load_trials_data.generate_trials_data(raw_data, 
            'statusModule', trial_headers.status_headers)
    
    status_data.to_sql(
        'TRIAL_STATUS', con=conn, if_exists='append', index=False)
    
    # conditions_data = load_trials_data.generate_trials_data(raw_data,
    #         'condition', trial_headers.conditions_headers)
    
    # conditions_data.to_sql(
    #     'CONDITIONS', con=conn, if_exists='append', index=False)
    
    # baseline_measures = load_trials_data.generate_trials_data(raw_data,
    #         'baselineCharacteristicsModule', trial_headers.baseline_headers)
    
    # baseline_measures.to_sql(
    #     'BASELINE_MEASURES', con=conn, if_exists='append', index=False
    # )
    
    c.close()

if __name__ == "__main__":
    makedb()