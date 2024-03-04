"""
Code for cleaning data from the FDA API and outputting to a CSV file.
Written by Alison Spencer.
"""
import json
import pandas as pd
import pathlib

def load_fda_data(filepath):
    """
    Cleans JSON data from FDA API into a list of dictionaries.
    
    Args:
        filepath (str): Filepath for the JSON data from API

    
    Returns:
        List of dictionaries, one dictionary for each FDA drug entry of interest.
    """

    # Load as a series to handle nested data
    with open(filepath) as json_file:
        data = json.load(json_file)
    results_list_of_dct = []
    for i, _ in enumerate(data):
        # data[i]['results'] is a list of dictionaries
        page_i_result = data[i]["results"]
        for dct in page_i_result:
            submission_status_date = dct.get("submissions", {})
            if submission_status_date:
                submission_status_date = submission_status_date[0].get(
                    "submission_status_date", {}
                )
            submission_status = dct.get("submissions", {})
            if submission_status:
                submission_status = submission_status[0].get("submission_status", {})
            application_number = dct.get("application_number", {})

            if "products" in dct:
                brand_name = dct.get("products", {})[0].get("brand_name", {})
            sponsor_name = dct.get("sponsor_name", {})
            generic_name = None
            substance_name = None
            manufacturer_name = None
            generic_name = dct.get("openfda", {}).get("generic_name", {})
            if generic_name:
                generic_name = generic_name[0]
            substance_name = dct.get("openfda", {}).get("substance_name", {})
            if substance_name:
                substance_name = substance_name[0]
            manufacturer_name = dct.get("openfda", {}).get("manufacturer_name", {})
            if manufacturer_name:
                manufacturer_name = manufacturer_name[0]
            openfda_brand_name = dct.get("openfda", {}).get("brand_name", {})

            drug_dct = {}
            #var_lst is list of variables we will include in the dictionary
            #for each drug
            var_lst = [
                "submission_status_date",
                "submission_status",
                "application_number",
                "brand_name",
                "sponsor_name",
                "generic_name",
                "substance_name",
                "manufacturer_name",
            ]
            for var in var_lst:
                drug_dct[var] = locals()[var]
            for key in dct:
                if dct[key] == {}:
                    dct[key] is None
            results_list_of_dct.append(drug_dct)
    return results_list_of_dct


def generate_fda_csv(filepath, filename):
    """
    Takes JSON data from API, cleans it, and converts to a csv file.
    
    Args:
        filepath (str): Filepath for the JSON data from API
        filename (str): The name of the file to write the CSV to

    
    Returns:
        CSV of cleaned FDA API data.
    """

    data = load_fda_data(filepath)
    df = pd.DataFrame.from_dict(data)
    df.to_csv(filename, sep=",", index=False, encoding="utf-8")

if __name__ == "__main__":
    pth = pathlib.Path(__file__).parent / f"../../data/fda.json"
    out_filename = pathlib.Path(__file__).parent / f"../../data/csvs/fda_full.csv"
    generate_fda_csv(pth, out_filename)

