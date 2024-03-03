import pandas as pd
import jellyfish
import pandas_dedupe

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
    fda_deduped = pandas_dedupe.dedupe_dataframe(fda, ['brand_name', 'generic_name'])
    fda_deduped[['brand_name']].to_csv('data/csvs/canonical_drugs.csv')

def get_probable_matches(canonical_drugs, interventions_filename, tolerance=.85, block_on_first_letter=True):
    """
    Loads a csv of fda data containing drug names, and clincal trials data
    containing intervention names, and attempts to fuzzy match them
    using the jaro-winkler similarity score.

    -- Args:
    """
    ivs = pd.read_csv(interventions_filename)

    ivs_unique = ivs['intervention_name'].str.lower().unique()
    
    drugs = {}
    for i_drug in ivs_unique:
        for f_drug in canonical_drugs:
            if block_on_first_letter:
                if i_drug.startswith(f_drug[0]):
                    sim_score = jellyfish.jaro_similarity(f_drug, i_drug)
                    if sim_score >= tolerance:
                        drugs[i_drug] = f_drug
                        break
            else:
                sim_score = jellyfish.jaro_similarity(f_drug, i_drug)
                if sim_score >= tolerance:
                    drugs[i_drug] = f_drug
                    break
    return drugs


def recode_trial_drugs(canonical_drugs_filename, interventions_filename):
    """
    Recodes drug names returned by the clinical trials API to match
    their canonical names in the FDA dataset.

    Args:
    -- Canonical drugs filename (str): The path to the file of canonical drugs.
        Should be generated using the create_canonical_drugs function.
    -- interventions_filename (str): Te path to the file of clinical trials
    data to be recoded

    Returns:
    None. Writes a csv to the csvs folder for uploading to the database.
    """
    drugs = pd.read_csv(canonical_drugs_filename)['brand_name']
    probable_matches = get_probable_matches(drugs, interventions_filename)
    trial_interventions = pd.read_csv(interventions_filename)
    trial_interventions['intervention_name'] = trial_interventions['intervention_name'].str.lower()
    trial_interventions['intervention_name'].replace(probable_matches)
    
    # Recoding introduces duplicates
    trials = trial_interventions.drop_duplicates()
    trials.to_csv('data/csvs/trial_interventions.csv', index=None)
    