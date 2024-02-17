#TODO: Handle relative filepath
import sqlite3

import pandas as pd


def load_data(filepath):
    """
    Loads returned trials data into a pandas dataframe
    """

    # Load as a series to handle nested data
    from_file = pd.read_json(filepath, typ='series')

    return pd.json_normalize(from_file)