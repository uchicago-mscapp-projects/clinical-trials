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
data = pd.read_csv("filename1.csv")

def by_drug(drug, condition_of_interest = None):
    """
    Filter race/ethnicity breakdown by treatment and condition 
    """
    # ULTIM, DATA_DRUG WON'T BE NEC CUZ WE WILL READ A FILTERED DATA INSTEAD
    data_drug = data[data['Drug Name'] == drug]
    if condition_of_interest:
        data_drug = data_drug[data_drug['Condition'] == condition_of_interest]

    # SOURCE: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.
    # html
    plt.figure(figsize = (10,6))
    plt.bar(data_drug['Year'], data_drug['White'], color = 'red', label= 'White')
    plt.bar(data_drug['Year'], data_drug['Black'], color = 'orange', label= 'Black')
    plt.bar(data_drug['Year'], data_drug['Asian'], color = 'yellow', label= 'Asian')
    plt.bar(data_drug['Year'], data_drug['Hispanic'], color = 'green', label= 'Hispanic')
    plt.bar(data_drug['Year'], data_drug['Other'], color = 'blue', label= 'Other')
    
    plt.xlabel('Year')
    plt.ylabel('Number of Participants')
    
    #plt.title('Race/Ethnicity Breakdown of Clinical Trials for {}'.format(drug))
    title_first_part = 'Race/Ethnicity Breakdown of Clinical Trials for '

    # SOURCE: https://peps.python.org/pep-0498/
    # String Interpolation Using F-Strings
    if condition_of_interest:
        title_condition_of_interest = f' ({condition_of_interest})'
    else:
        title_condition_of_interest = ''
    title = title_first_part + title_condition_of_interest
    plt.title(title)
    plt.legend()
    plt.show()

drug_for_analysis = 'X Drug'
by_drug(drug_for_analysis)


# Race/Ethnicity Breakdown of Clinical Trials: Data Analysis
def summary_statistics_table(drug, data):
    '''
    Summary Statistics table of race/ethnicity breakdown of clinical
    trials.
    '''
    data_drug = data[data['Drug Name'] == drug]

    total_participants_by_race = data_drug.sum()
    max_participants_by_race = data_drug.max()
    min_participants_by_race = data_drug.min()
    median_participants_by_race = data_drug.median()
    range_participants_by_race = max_participants_by_race - min_participants_by_race

    # SOURCE: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Data
    # Frame.div.html
    #perc_participants_by_race = data.div(data.sum(axis = 1), axis = 0) * 100
    perc_participants_by_race = (data_drug[['White','Black', 'Asian', 'Hispanic', 
                                'Other']] / total_participants_by_race) * 100
    ave_participants_each_year = data_drug.groupby('Year').mean()

    # SOURCE: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.
    # DataFrame.quantile.html
    iqr_by_race = data_drug.quantile(0.75) - data_drug.quantile(0.25)

    # NA Values
    na_drug = data_drug[data_drug.isna().any(axis = 1)]
    print(na_drug)

    # Put Summary Statistics in a dataframe to be used for dashboard viz
    df = pd.DataFrame({
        'Stat': ['Total Participants', 'Maximum Participants', 
                'Minimum Participants',
                'Median Participants', 'Range of Participants By Race',
                'Percentage of Participants By Race', 
                'Average Participants Each Year', 
                'Interquartile Range of Participants By Race',
                'Missing Observations']
        'Val': [total_participants_by_race, max_participants_by_race,
                min_participants_by_race, median_participants_by_race,
                range_participants_by_race, perc_participants_by_race,
                ave_participants_each_year, iqr_by_race, na_drug]
    })

    return df


# Racial Diversity in Clinical Trials Conducted By Manufacturers: Line Graph
data_manufacturer = pd.read_csv("filename2.csv")

def by_manufacturer(manuf):
    """
    Filter race/ethnicity breakdown by manufacturer
    """
    # ULTIM, DATA_MANUF WON'T BE NEC CUZ WE WILL READ A FILTERED DATA INSTEAD
    data_manuf = data_manufacturer[data_manufacturer['Manufacturer'] == manuf]

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
            data_manuf['Year'] == year][['Manufacturer_A',
                                         'Manufacturer_B']].sum(axis=1)
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
    
    plt.plot(data_manuf['Year'], perc_white, marker = 'o', label = 'White')
    plt.plot(data_manuf['Year'], perc_black, marker = 'o', label = 'Black')
    plt.plot(data_manuf['Year'], perc_asian, marker = 'o', label = 'Asian')
    plt.plot(data_manuf['Year'], perc_hispanic, marker = 'o', 
             label = 'Hispanic')
    plt.plot(data_manuf['Year'], perc_other, marker = 'o', label = 'Other')

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
def summary_statistics_manuf_table(manuf, data):
    '''
    Summary Statistics table of race/ethnicity breakdown of clinical
    trials.
    '''
    perc_participants_by_manufacturer = {}
    ave_participants_manuf_each_year = {}
    iqr_by_manufacturer = {}
    na_manufacturer = {}

    for manufacturer in data_manufacturer['Manufacturer'].unique():
        data_manuf = data_manufacturer[
            data_manufacturer['Manufacturer'] == manuf]

        total_participants_by_manufacturer = data_manuf.sum()
        max_participants_by_manufacturer = data_manuf.max()
        min_participants_by_manufacturer = data_manuf.min()
        median_participants_by_manufacturer = data_manuf.median()
        range_participants_by_manufacturer = max_participants_by_manufacturer - min_participants_by_manufacturer

        perc_participants_by_manufacturer[manufacturer] = (data_manuf
                                                        [['White','Black', 
                                                            'Asian', 'Hispanic', 
                                                            'Other']] / 
                                        total_participants_by_manufacturer) * 100
        ave_participants_manuf_each_year[manufacturer] = data_manuf.groupby(
            'Year').mean()
        # SOURCE: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.
        # DataFrame.quantile.html
        iqr_by_manufacturer[manufacturer] = data_manuf.quantile(
            0.75) - data_manuf.quantile(0.25)
        na_manufacturer[manufacturer] = data_manuf[data_manuf.isna().any(axis=1)]
        print(na_manufacturer)

    # Put Summary Statistics in a dataframe to be used for dashboard viz
    df_manuf = pd.DataFrame({
        'Stat': ['Total Participants By Manufacturer', 
                'Maximum Participants By Manufacturer', 
                'Minimum Participants By Manufacturer',
                'Median Participants By Manufacturer', 
                'Range of Participants By Manufacturer',
                'Percentage of Participants By Manufacturer', 
                'Average Participants Each Year', 
                'Interquartile Range of Participants By Manufacturer',
                'Missing Observations']
        'Val': [total_participants_by_manufacturer, max_participants_by_manufacturer,
                min_participants_by_manufacturer, 
                median_participants_by_manufacturer,
                range_participants_by_manufacturer, 
                perc_participants_by_manufacturer,
                ave_participants_manuf_each_year, iqr_by_manufacturer, 
                na_manufacturer]
    })

    return df_manuf



#### title in generate_table():

# Table function from https://dash.plotly.com/layout

# Including certain headers in the input for generate_table()
# SOURCE 0: https://community.plotly.com/t/formatting-table-headers/29942

# html.Div([]): Create HTML table using Table feature from Dash
# SOURCE 1: https://community.plotly.com/t/dataframe-to-html-table-using-dash/5009

# html.H1(object): Type of style in HTML
# SOURCE 2: https://www.w3schools.com/tags/tag_hn.asp

# Putting an object inside <div> tag
# SOURCE 3: https://www.digitalocean.com/community/tutorials/how-to-style-the-
# html-div-element-with-css

def generate_table(dataframe, title = "None", max_rows=10):
    summary_stat_table = html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
    return html.Div([
        html.H1(title),
        summary_stat_table
    ])

# For example:
generate_table(dataframe_manuf, title = "*manuf title*")
