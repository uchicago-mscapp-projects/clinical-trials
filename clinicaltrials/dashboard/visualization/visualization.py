# Kristy Kwon
# "Let's Get Clinical" CAPP 122 Team
# Skeleton Code: Visualization
# 2/19/24

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mpld3

# Race/Ethnicity Breakdown of Clinical Trials: Stacked Bar Chart

def by_drug(data_drug, treatment_of_interest, condition_of_interest):
    """
    Filter race/ethnicity breakdown by treatment and condition 
    """
    # SOURCE: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.
    # html
    data_drug['intervention_name'] = data_drug['intervention_name'].astype('category')

    f = plt.figure(figsize = (8,6))
    plt.bar(data_drug['intervention_name'], data_drug['White'], color = 'red', label= 'White')
    plt.bar(data_drug['intervention_name'], data_drug['Black'], color = 'orange', label= 'Black', 
            bottom=data_drug['White'])
    plt.bar(data_drug['intervention_name'], data_drug['Asian'], color = 'yellow', label= 'Asian', 
            bottom=data_drug['Black'] + data_drug['White'])
    plt.bar(data_drug['intervention_name'], data_drug['Hispanic'], color = 'green', label= 'Hispanic', 
            bottom=data_drug['Asian'] + data_drug['Black'] + data_drug['White'])
    plt.bar(data_drug['intervention_name'], data_drug['Other'], color = 'blue', label= 'Other', 
            bottom=data_drug['Hispanic'] + data_drug['Asian'] + \
                data_drug['Black'] + data_drug['White'])

    plt.xlabel('Treatment Intervention', color = '#accdf2')
    plt.ylabel('Number of Participants', color = '#accdf2')

    title_first_part = 'Race/Ethnicity Breakdown of Clinical Trials for '

    # SOURCE: https://peps.python.org/pep-0498/
    # String Interpolation Using F-Strings
    if treatment_of_interest:
        title_treatment_of_interest = f' {treatment_of_interest.capitalize()}'
    else:
        title_treatment_of_interest = ''
    if condition_of_interest:
        title_condition_of_interest = f' {condition_of_interest}'
    else:
        title_condition_of_interest = ''
    title = title_first_part + title_treatment_of_interest + ' in ' + title_condition_of_interest

    plt.tick_params(labelbottom = False, bottom = False, \
                    labeltop = False, top = False, colors = '#accdf2')

    plt.title(title, color = '#accdf2')
    plt.legend()

    html_matplotlib = mpld3.fig_to_html(f)
    return html_matplotlib


# Race/Ethnicity Breakdown of Clinical Trials: Data Analysis
def summary_statistics_table(data_drug, treatment_of_interest, condition_of_interest):
    '''
    Summary Statistics table of race/ethnicity breakdown of clinical
    trials.
    '''
    data_drug = data_drug[["Asian", "Black", "White", "Hispanic", "Other"]] # DS added
    perc_participants_by_drug = {}
    ave_participants_by_drug_each_race = {}
    iqr_by_drug = {}
    na_drug = {}

    total_participants_by_drug = data_drug.sum(axis = 1)[0]
    max_participants_by_drug = data_drug.max(axis = 1)[0]
    min_participants_by_drug = data_drug.min(axis = 1)[0]
    ave_participants_by_drug = data_drug.mean(axis = 1)[0]
    median_participants_by_drug = data_drug.median(axis = 1)[0]
    range_participants_by_drug = max_participants_by_drug - min_participants_by_drug

    white_perc_drug = '{:.1%}'.format(((data_drug['White'] / 
                    total_participants_by_drug))[0])
    black_perc_drug = '{:.1%}'.format(((data_drug['Black'] / 
                    total_participants_by_drug))[0])
    asian_perc_drug = '{:.1%}'.format(((data_drug['Asian'] / 
                    total_participants_by_drug))[0])
    hispanic_perc_drug = '{:.1%}'.format(((data_drug['Hispanic'] / 
                    total_participants_by_drug))[0])
    other_perc_drug = '{:.1%}'.format(((data_drug['Other'] / 
                    total_participants_by_drug))[0])

    perc_participants_by_drug[treatment_of_interest] = {
        'Percentage of Whites By Drug': white_perc_drug,
        'Percentage of Blacks By Drug': black_perc_drug,
        'Percentage of Asians By Manufacturer': asian_perc_drug,
        'Percentage of Hispanics By Manufacturer': hispanic_perc_drug,
        'Percentage of Others By Manufacturer': other_perc_drug,
    }

    # ave_participants_by_drug_each_race[treatment_of_interest] = {
    #     'Average Number of White Participants': data_drug['White'].mean(),
    #     'Average Number of Black Participants': data_drug['Black'].mean(),
    #     'Average Number of Asian Participants': data_drug['Asian'].mean(),
    #     'Average Number of Hispanic Participants': data_drug['Hispanic'].mean(),
    #     'Average Number of Other Participants': data_drug['Other'].mean(),
    # }

    # SOURCE: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.
    # DataFrame.quantile.html

    # iqr_by_drug[treatment_of_interest] = {
    #     'Interquartile Range of White Participants': data_drug[
    #         'White'].quantile(0.75) - data_drug['White'].quantile(0.25),
    #     'Interquartile Range of Black Participants': data_drug[
    #         'Black'].quantile(0.75) - data_drug['Black'].quantile(0.25),
    #     'Interquartile Range of White Participants': data_drug[
    #         'Asian'].quantile(0.75) - data_drug['Asian'].quantile(0.25),
    #     'Interquartile Range of White Participants': data_drug[
    #         'Hispanic'].quantile(0.75) - data_drug['Hispanic'].quantile(0.25),
    #     'Interquartile Range of White Participants': data_drug[
    #         'Other'].quantile(0.75) - data_drug['Other'].quantile(0.25)
    # }
    
    # SOURCE 1: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.any.html
    # SOURCE 2: https://stackoverflow.com/questions/52870728/pandas-check-if
    # -any-of-the-values-in-a-subset-of-a-column-respect-condition

    # Look for any element with NAs through .any() within rows, then filter 
    # rows of data

    na_drug[treatment_of_interest] = data_drug[data_drug.isna().any(axis=1)]

    # Put Summary Statistics in a dataframe to be used for dashboard viz
    df_drug = pd.DataFrame({
        'Stat': ['Total Participants in Trials for the Drug in the Condition', 
                'Maximum Race/Ethnicity Group Size in Trials for the Drug in the Condition', 
                'Minimum Race/Ethnicity Group Size in Trials for the Drug in the Condition',
                'Average Race/Ethnicity Group Size in Trials for the Drug in the Condition',
                'Median Race/Ethnicity Group Size in Trials for the Drug in the Condition', 
                'Range of Race/Ethnicity Group Sizes in Trials for the Drug in the Condition',
                'Percentage of White Participants in Trials for the Drug in the Condition',
                'Percentage of Black Participants By Drug in Trials for the Drug in the Condition',
                'Percentage of Asian Participants in Trials for the Drug in the Condition',
                'Percentage of Hispanic Participants in Trials for the Drug in the Condition',
                'Percentage of Participants of Other Races in Trials for the Drug in the Condition',
                # 'Percentage of Participants By Drug', 
                # 'Average Participants By Drug For Each Race', 
                # 'Interquartile Range of Participants By Drug',
                #'Missing Observations'
                ],
        'Val': [total_participants_by_drug, max_participants_by_drug,
                min_participants_by_drug, ave_participants_by_drug, 
                median_participants_by_drug,
                range_participants_by_drug, 
                white_perc_drug,
                black_perc_drug,
                asian_perc_drug,
                hispanic_perc_drug,
                other_perc_drug
                # perc_participants_by_drug,
                # ave_participants_by_drug_each_race, iqr_by_drug, 
               #na_drug
               ]
    })

    return df_drug


# Racial Diversity in Clinical Trials Conducted By Manufacturers: Line Graph

def by_manufacturer(data_manuf, manuf):
    """
    Filter race/ethnicity breakdown by manufacturer
    """
    # SOURCE: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.
    # html
    data_manuf.dropna(subset = ['Year'], inplace=True)

    f = plt.figure(figsize = (10,6))

    white_perc = []
    black_perc = []
    asian_perc = []
    hispanic_perc = []
    other_perc = []

    for year in data_manuf['Year']:
        total_participants_by_manufacturer = data_manuf[
            data_manuf['Year'] == year].drop(['Manufacturer', 'Year'], axis=1).sum(axis=1)
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

    plt.xlabel('Year', color = '#accdf2')
    plt.ylabel('Number of Participants', color = '#accdf2')

    title_first_part_manuf = 'Race/Ethnicity Breakdown of Clinical Trials Sponsored By '
    title_manuf = title_first_part_manuf + '{}'.format(manuf)
    plt.title(title_manuf, color = '#accdf2')

    plt.legend()
    plt.grid(True)

    html_matplotlib = mpld3.fig_to_html(f)
    return html_matplotlib


# Racial Diversity in Clinical Trials Conducted By Manufacturers: Data Analysis
def summary_statistics_manuf_table(data_manuf, manufacturer):
    '''
    Summary Statistics table of race/ethnicity breakdown of clinical
    trials.
    '''
    data_manuf = data_manuf[["Asian", "Black", "White", "Hispanic", "Other"]] # DS added
    perc_participants_by_manufacturer = {}
    ave_participants_by_manufacturer_each_race = {}
    iqr_by_manufacturer = {}
    na_manufacturer = {}

    total_participants_by_manufacturer = data_manuf.sum(axis = 1)[0]
    max_participants_by_manufacturer = data_manuf.max(axis = 1)[0]
    min_participants_by_manufacturer = data_manuf.min(axis = 1)[0]
    ave_participants_by_manufacturer = data_manuf.mean(axis = 1)[0]
    median_participants_by_manufacturer = data_manuf.median(axis = 1)[0]
    range_participants_by_manufacturer = max_participants_by_manufacturer - min_participants_by_manufacturer

    white_perc_manuf = '{:.1%}'.format(((data_manuf['White'] / 
                    total_participants_by_manufacturer) )[0])
    black_perc_manuf = '{:.1%}'.format(((data_manuf['Black'] / 
                    total_participants_by_manufacturer))[0])
    asian_perc_manuf = '{:.1%}'.format(((data_manuf['Asian'] / 
                    total_participants_by_manufacturer))[0])
    hispanic_perc_manuf = '{:.1%}'.format(((data_manuf['Hispanic'] / 
                    total_participants_by_manufacturer))[0])
    other_perc_manuf = '{:.1%}'.format(((data_manuf['Other'] / 
                    total_participants_by_manufacturer) )[0])
    
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

    # Put Summary Statistics in a dataframe to be used for dashboard viz
    df_manuf = pd.DataFrame({
        'Stat': ['Total Participants in Trials Conducted by the Sponsor', 
                'Maximum Race/Ethnicity Group Size in Trials Conducted by the Sponsor', 
                'Minimum Race/Ethnicity Group Size in Trials Conducted by the Sponsor',
                'Average Race/Ethnicity Group Size in Trials Conducted by the Sponsor',
                'Median Race/Ethnicity Group Size in Trials Conducted by the Sponsor', 
                'Range of Race/Ethnicity Group Sizes in Trials Conducted by the Sponsor',
                'Percentage of White Participants in Trials Conducted by the Sponsor',
                'Percentage of Black Participants By Drug in Trials Conducted by the Sponsor',
                'Percentage of Asian Participants in Trials Conducted by the Sponsor',
                'Percentage of Hispanic Participants in Trials Conducted by the Sponsor',
                'Percentage of Participants of Other Races in Trials Conducted by the Sponsor',
                # 'Percentage of Participants By Manufacturer', 
                # 'Average Participants Each Year', 
                # 'Interquartile Range of Participants By Manufacturer',
                #'Missing Observations'
                ],
        'Val': [total_participants_by_manufacturer, 
                max_participants_by_manufacturer,
                min_participants_by_manufacturer, 
                ave_participants_by_manufacturer,
                median_participants_by_manufacturer, 
                range_participants_by_manufacturer, 
                white_perc_manuf,
                black_perc_manuf,
                asian_perc_manuf,
                hispanic_perc_manuf,
                other_perc_manuf
                # perc_participants_by_manufacturer,
                # ave_participants_by_manufacturer_each_race, 
                # iqr_by_manufacturer, 
                # na_manufacturer
                ]
    })

    return df_manuf
