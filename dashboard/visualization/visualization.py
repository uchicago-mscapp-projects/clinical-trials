# Kristy Kwon
# "Let's Get Clinical" CAPP 122 Team
# Skeleton Code: Visualization
# 2/19/24

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import dash
from dash import doc, html, dash_table

# Race/Ethnicity Breakdown of Clinical Trials: Stacked Bar Chart

def by_drug(data_drug, treatment_of_interest, condition_of_interest):
    """
    Filter race/ethnicity breakdown by treatment and condition 
    """
    # SOURCE: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.
    # html
    plt.figure(figsize = (10,6))
    plt.bar(data_drug['intervention_name'], data_drug['White'], color = 'red', label= 'White')
    plt.bar(data_drug['intervention_name'], data_drug['Black'], color = 'orange', label= 'Black')
    plt.bar(data_drug['intervention_name'], data_drug['Asian'], color = 'yellow', label= 'Asian')
    plt.bar(data_drug['intervention_name'], data_drug['Hispanic'], color = 'green', label= 'Hispanic')
    plt.bar(data_drug['intervention_name'], data_drug['Other'], color = 'blue', label= 'Other')
    
    plt.xlabel('Treatment Intervention')
    plt.ylabel('Number of Participants')
    
    #plt.title('Race/Ethnicity Breakdown of Clinical Trials for {}'.format(drug))
    title_first_part = 'Race/Ethnicity Breakdown of Clinical Trials for '

    # SOURCE: https://peps.python.org/pep-0498/
    # String Interpolation Using F-Strings
    if treatment_of_interest:
        title_treatment_of_interest = f' ({treatment_of_interest})'
    else:
        title_treatment_of_interest = ''
    if condition_of_interest:
        title_condition_of_interest = f' ({condition_of_interest})'
    else:
        title_condition_of_interest = ''
    title = title_first_part + title_treatment_of_interest + 'in' + title_condition_of_interest

    plt.title(title)
    plt.legend()
    plt.show()


# Race/Ethnicity Breakdown of Clinical Trials: Data Analysis
def summary_statistics_table(data_drug, treatment_of_interest, condition_of_interest):
    '''
    Summary Statistics table of race/ethnicity breakdown of clinical
    trials.
    '''
    perc_participants_by_drug = {}
    ave_participants_by_drug_each_race = {}
    iqr_by_drug = {}
    na_drug = {}

    total_participants_by_drug = data_drug.sum()
    max_participants_by_drug = data_drug.max()
    min_participants_by_drug = data_drug.min()
    ave_participants_by_drug = data_drug.mean()
    median_participants_by_drug = data_drug.median()
    range_participants_by_drug = max_participants_by_drug - min_participants_by_drug

    white_perc_drug = (data_drug['White'] / 
                    total_participants_by_drug) * 100
    black_perc_drug = (data_drug['Black'] / 
                    total_participants_by_drug) * 100
    asian_perc_drug = (data_drug['Asian'] / 
                    total_participants_by_drug) * 100
    hispanic_perc_drug = (data_drug['Hispanic'] / 
                    total_participants_by_drug) * 100
    other_perc_drug = (data_drug['Other'] / 
                    total_participants_by_drug) * 100
    
    perc_participants_by_drug[treatment_of_interest] = {
        'Percentage of Whites By Drug': white_perc_drug,
        'Percentage of Blacks By Drug': black_perc_drug,
        'Percentage of Asians By Manufacturer': asian_perc_drug,
        'Percentage of Hispanics By Manufacturer': hispanic_perc_drug,
        'Percentage of Others By Manufacturer': other_perc_drug,
    }

    ave_participants_by_drug_each_race[treatment_of_interest] = {
        'Average Number of White Participants': data_drug['White'].mean(),
        'Average Number of Black Participants': data_drug['Black'].mean(),
        'Average Number of Asian Participants': data_drug['Asian'].mean(),
        'Average Number of Hispanic Participants': data_drug['Hispanic'].mean(),
        'Average Number of Other Participants': data_drug['Other'].mean(),
    }

    # SOURCE: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.
    # DataFrame.quantile.html

    iqr_by_drug[treatment_of_interest] = {
        'Interquartile Range of White Participants': data_drug[
            'White'].quantile(0.75) - data_drug['White'].quantile(0.25),
        'Interquartile Range of Black Participants': data_drug[
            'Black'].quantile(0.75) - data_drug['Black'].quantile(0.25),
        'Interquartile Range of White Participants': data_drug[
            'Asian'].quantile(0.75) - data_drug['Asian'].quantile(0.25),
        'Interquartile Range of White Participants': data_drug[
            'Hispanic'].quantile(0.75) - data_drug['Hispanic'].quantile(0.25),
        'Interquartile Range of White Participants': data_drug[
            'Other'].quantile(0.75) - data_drug['Other'].quantile(0.25)
    }
    
    # SOURCE 1: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.any.html
    # SOURCE 2: https://stackoverflow.com/questions/52870728/pandas-check-if
    # -any-of-the-values-in-a-subset-of-a-column-respect-condition

    # Look for any element with NAs through .any() within rows, then filter 
    # rows of data

    na_drug[treatment_of_interest] = data_drug[data_drug.isna().any(axis=1)]
    print(na_drug)

    # Put Summary Statistics in a dataframe to be used for dashboard viz
    df_manuf = pd.DataFrame({
        'Stat': ['Total Participants By Drug', 
                'Maximum Participants By Drug', 
                'Minimum Participants By Drug',
                'Average Participants By Drug',
                'Median Participants By Drug', 
                'Range of Participants By Drug',
                'Percentage of Participants By Drug', 
                'Average Participants By Drug For Each Race', 
                'Interquartile Range of Participants By Drug',
                'Missing Observations']
        'Val': [total_participants_by_drug, max_participants_by_drug,
                min_participants_by_drug, ave_participants_by_drug, 
                median_participants_by_drug,
                range_participants_by_drug, 
                perc_participants_by_drug,
                ave_participants_by_drug_each_race, iqr_by_drug, 
                na_drug]
    })

    return df_manuf



# Racial Diversity in Clinical Trials Conducted By Manufacturers: Line Graph

def by_manufacturer(data_manuf):
    """
    Filter race/ethnicity breakdown by manufacturer
    """
    # SOURCE: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.
    # html
    plt.figure(figsize = (10,6))

    white_perc = []
    black_perc = []
    asian_perc = []
    hispanic_perc = []
    other_perc = []

    for year in data_manuf['Year']:
        total_participants_by_manufacturer = data_manuf[
            data_manuf['Year'] == year].sum(axis=1)
        white_perc.append((data_manuf[data_manuf['Year'] == year]['White'] /
                           total_participants_by_manufacturer) * 100)
        black_perc.append((data_manuf[data_manuf['Year'] == year]['Black'] /
                           total_participants_by_manufacturer) * 100)
        asian_perc.append((data_manuf[data_manuf['Year'] == year]['Asian'] /
                           total_participants_by_manufacturer) * 100)
        hispanic_perc.append((data_manuf[data_manuf['Year'] == 
                                         year]['Hispanic'] /
                           total_participants_by_manufacturer) * 100)
        other_perc.append((data_manuf[data_manuf['Year'] == year]['Other'] /
                           total_participants_by_manufacturer) * 100)
    
    plt.plot(data_manuf['Year'], white_perc, marker = 'o', label = 'White')
    plt.plot(data_manuf['Year'], black_perc, marker = 'o', label = 'Black')
    plt.plot(data_manuf['Year'], asian_perc, marker = 'o', label = 'Asian')
    plt.plot(data_manuf['Year'], hispanic_perc, marker = 'o', 
             label = 'Hispanic')
    plt.plot(data_manuf['Year'], other_perc, marker = 'o', label = 'Other')

    plt.xlabel('Year')
    plt.ylabel('Number of Participants')
    
    title_first_part_manuf = 'Racial Diversity in Clinical Trials Conducted By Manufacturers for '
    title_manuf = title_first_part_manuf + '{}'.format(manuf)
    plt.title(title_manuf)
    
    plt.legend()
    plt.grid(True)
    plt.show()

manuf_for_analysis = 'X Manufacturer'
by_manufacturer(manuf_for_analysis)


# Racial Diversity in Clinical Trials Conducted By Manufacturers: Data Analysis
def summary_statistics_manuf_table(data_manuf, manufacturer):
    '''
    Summary Statistics table of race/ethnicity breakdown of clinical
    trials.
    '''
    perc_participants_by_manufacturer = {}
    ave_participants_by_manufacturer_each_race = {}
    iqr_by_manufacturer = {}
    na_manufacturer = {}

    total_participants_by_manufacturer = data_manuf.sum()
    max_participants_by_manufacturer = data_manuf.max()
    min_participants_by_manufacturer = data_manuf.min()
    ave_participants_by_manufacturer = data_manuf.mean()
    median_participants_by_manufacturer = data_manuf.median()
    range_participants_by_manufacturer = max_participants_by_manufacturer - min_participants_by_manufacturer

    white_perc_manuf = (data_manuf['White'] / 
                    total_participants_by_manufacturer) * 100
    black_perc_manuf = (data_manuf['Black'] / 
                    total_participants_by_manufacturer) * 100
    asian_perc_manuf = (data_manuf['Asian'] / 
                    total_participants_by_manufacturer) * 100
    hispanic_perc_manuf = (data_manuf['Hispanic'] / 
                    total_participants_by_manufacturer) * 100
    other_perc_manuf = (data_manuf['Other'] / 
                    total_participants_by_manufacturer) * 100
    
    perc_participants_by_manufacturer[manufacturer] = {
        'Percentage of Whites By Manufacturer': white_perc_manuf,
        'Percentage of Blacks By Manufacturer': black_perc_manuf,
        'Percentage of Asians By Manufacturer': asian_perc_manuf,
        'Percentage of Hispanics By Manufacturer': hispanic_perc_manuf,
        'Percentage of Others By Manufacturer': other_perc_manuf,
    }

    ave_participants_by_manufacturer_each_race[manufacturer] = {
        'Average Number of White Participants': data_manuf['White'].mean(),
        'Average Number of Black Participants': data_manuf['Black'].mean(),
        'Average Number of Asian Participants': data_manuf['Asian'].mean(),
        'Average Number of Hispanic Participants': data_manuf['Hispanic'].mean(),
        'Average Number of Other Participants': data_manuf['Other'].mean(),
    }

    # SOURCE: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.
    # DataFrame.quantile.html

    iqr_by_manufacturer[manufacturer] = {
        'Interquartile Range of White Participants': data_manuf[
            'White'].quantile(0.75) - data_manuf['White'].quantile(0.25),
        'Interquartile Range of Black Participants': data_manuf[
            'Black'].quantile(0.75) - data_manuf['Black'].quantile(0.25),
        'Interquartile Range of White Participants': data_manuf[
            'Asian'].quantile(0.75) - data_manuf['Asian'].quantile(0.25),
        'Interquartile Range of White Participants': data_manuf[
            'Hispanic'].quantile(0.75) - data_manuf['Hispanic'].quantile(0.25),
        'Interquartile Range of White Participants': data_manuf[
            'Other'].quantile(0.75) - data_manuf['Other'].quantile(0.25)
    }
    
    # SOURCE 1: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.any.html
    # SOURCE 2: https://stackoverflow.com/questions/52870728/pandas-check-if
    # -any-of-the-values-in-a-subset-of-a-column-respect-condition

    # Look for any element with NAs through .any() within rows, then filter 
    # rows of data

    na_manufacturer[manufacturer] = data_manuf[data_manuf.isna().any(axis=1)]
    print(na_manufacturer)

    # Put Summary Statistics in a dataframe to be used for dashboard viz
    df_manuf = pd.DataFrame({
        'Stat': ['Total Participants By Manufacturer', 
                'Maximum Participants By Manufacturer', 
                'Minimum Participants By Manufacturer',
                'Average Participants By Manufacturer',
                'Median Participants By Manufacturer', 
                'Range of Participants By Manufacturer',
                'Percentage of Participants By Manufacturer', 
                'Average Participants Each Year', 
                'Interquartile Range of Participants By Manufacturer',
                'Missing Observations']
        'Val': [total_participants_by_manufacturer, 
                max_participants_by_manufacturer,
                min_participants_by_manufacturer, 
                ave_participants_by_manufacturer,
                median_participants_by_manufacturer, 
                range_participants_by_manufacturer, 
                perc_participants_by_manufacturer,
                ave_participants_by_manufacturer_each_race, 
                iqr_by_manufacturer, 
                na_manufacturer]
    })

    return df_manuf
