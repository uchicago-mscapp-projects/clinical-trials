import pandas as pd
import jellyfish
import pandas_dedupe
import pathlib

def create_canonical_drugs(fda_filename):
    """
    Creates a canonical list of drugs from the fda data using fuzzy deduping.

    Args:
    -- fda_filename (str): Filepath to a csv containing fda drug data returned
    from the fda api

    Returns:
    None. Saves a csv of FDA drug records deduped on brand name.
    
    """
    fda = pd.read_csv(fda_filename)

    fda['brand_name'] = fda['brand_name'].str.lower()
    fda_deduped = pandas_dedupe.dedupe_dataframe(fda, ['brand_name'])
    fda_canonical = fda_deduped.drop_duplicates(subset=['brand_name'])

    filename = pathlib.Path(__file__).parent / f"../../data/csvs/canonical_drugs.csv"
    fda_canonical.to_csv(filename, columns=['brand_name'], 
                         index=False)

def get_probable_matches(canonical_data, raw_trials_filename, tolerance=.85):
    """
    Loads a csv of fda data containing drug names, and clincal trials data
    containing intervention names, and attempts to fuzzy match them
    using the jaro-winkler similarity score.

    Args:
    -- canonical drugs (dataframe): A deduped pandas dataframe canonical drugs
    -- interventions_filename (str): The path to the file of clinical trials
    data to be recoded
    """
    raw = pd.read_csv(raw_trials_filename)

    raw_unique = raw['intervention_name'].str.lower().unique()
    
    recoded = {}
    for raw_entry in raw_unique:
        for canon_entry in canonical_data:
                # Block on the first letter to speed up computation
                if raw_entry.startswith(canon_entry[0]):
                    sim_score = jellyfish.jaro_similarity(canon_entry, raw_entry)
                    if sim_score >= tolerance:
                        recoded[raw_entry] = canon_entry
                        break

    return recoded


def recode_trial_drugs(canonical_filename, raw_filename):
    """
    Recodes drug names returned by the clinical trials API to match
    their canonical names in the FDA dataset.

    Args:
    -- Canonical drugs filename (str): The path to the file of canonical drugs.
        Should be generated using the create_canonical_drugs function.
    -- interventions_filename (str): The path to the file of clinical trials
    data to be recoded

    Returns:
    None. Writes a csv to the csvs folder for uploading to the database.
    """
    drugs = pd.read_csv(canonical_filename)['brand_name']
    probable_matches = get_probable_matches(drugs, raw_filename)
    trial_interventions = pd.read_csv(raw_filename)
    trial_interventions['intervention_name'] = trial_interventions['intervention_name'].str.lower()
    trial_interventions['intervention_name'].replace(probable_matches)
    
    # Recoding introduces duplicates
    trials = trial_interventions.drop_duplicates()

    filename = pathlib.Path(__file__).parent / f"../../data/csvs/trial_interventions.csv"
    trials.to_csv(filename, index=None)
    