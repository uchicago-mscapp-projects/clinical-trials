import pandas as pd
import json

def get_distinct_race_categories(filepath):
    """
    Finds distinct values for race used in the returned CDC trial data.
    Not called in the final app, but used in the process of development
    to generate the dictionary in recode.py
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

