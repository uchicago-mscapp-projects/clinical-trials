"""
Collapses unnormalized race categories from the clinical trials data into
a set of standardized categories.

Written by Caitlin Pratt
"""

import re
import json

WHITE = 'white'
BLACK = 'black'
ASIAN = 'asian'
AI_AN = 'american_indian_or_alaska_native'
HI_PI = 'hawaiian_or_pacific_islander'
LATINO = 'hispanic_or_latino'
NOT_LATINO = 'not_hispanic_or_latino'
MUL = 'multiple'
UNK = 'unknown'

def get_distinct_race_categories(filepath):
    """
    Finds distinct values for race used in the returned clinical trials data.

    Args:
    -- filepath (str): The filepath of the json file returned by the API

    Returns:
        list: Distinct values for race in the json file
    """
    distinct = []
    loaded = json.load(open(filepath))

    for row in loaded:
        measures = row.get('resultsSection', {})\
                .get('baselineCharacteristicsModule', {}).get('measures', {})
        for measure in measures:
            if measure.get('title') in ('Race/Ethnicity, Customized', 'Race (NIH/OMB)') \
                and measure.get('paramType') == 'COUNT_OF_PARTICIPANTS':
                for cls in measure.get('classes', {}):
                    for cat in cls.get('categories', {}):
                        if cat.get('title') not in distinct:
                            distinct.append(cat.get('title'))
    return distinct

def collapse_race_data(filepath, recode_all=False):
    """
    Attempts to apply recoded values based on return distinct fields.
    If recode_all is set to true, applies 'unknown' to all fields it was unable to match.

    Returns: Dict of applied fields, list of keys of fields that were unmatched.
    """

    recoding_dict = {}
    unmatched = []

    distinct_data = get_distinct_race_categories(filepath)

    for category in distinct_data:

        # Attempt to match values in json to keywords
        string_cat = str(category)
        if re.search('multiple|more than one|multi', string_cat, flags=re.IGNORECASE):
            recoding_dict[category] = MUL
        elif re.search('white|caucasian', string_cat, flags=re.IGNORECASE):
            recoding_dict[category] = WHITE
        elif re.search('asian', string_cat, flags=re.IGNORECASE):
            recoding_dict[category] = ASIAN
        elif re.search('black|african', string_cat, flags=re.IGNORECASE):
            recoding_dict[category] = BLACK
        elif re.search('hawaiian', string_cat, flags=re.IGNORECASE):
            recoding_dict[category] = HI_PI
        elif re.search('latin|hispanic|mexican', string_cat, flags=re.IGNORECASE):
            recoding_dict[category] = LATINO
        elif re.search('not latin', string_cat, flags=re.IGNORECASE):
            recoding_dict[category] = NOT_LATINO
        elif re.search('american indian|alaska|native', string_cat, flags=re.IGNORECASE):
            recoding_dict[category] = AI_AN
        elif re.search('other|unknown|refused|not applicable|none|declined|chose not|no response|missing|prefer not|not report',\
                        string_cat, flags=re.IGNORECASE):
            recoding_dict[category] = UNK
        elif re.search('multiple|more than one|multi|mixed', string_cat, flags=re.IGNORECASE):
            recoding_dict[category] = MUL
        elif recode_all:
            recoding_dict[category] = UNK
        else:
            unmatched.append(category)

    if recode_all:
        return recoding_dict

    else:
        return (recoding_dict, unmatched)