# Kristy Kwon
# "Let's Get Clinical" CAPP 122 Team
# Skeleton Code: Visualization
# 2/19/24

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Race/Ethnicity Breakdown of Clinical Trials: Stacked Bar Chart
data = pd.read_csv("filename1.csv")

def by_drug(drug):
    """
    Filter race/ethnicity breakdown by drug
    """
    data_drug = data[data['Drug Name'] == drug]

    plt.figure(figsize = (10,6))
    plt.bar(data_drug['Year'], data_drug['White'], color = 'red', label= 'White')
    plt.bar(data_drug['Year'], data_drug['Black'], color = 'orange', label= 'Black')
    plt.bar(data_drug['Year'], data_drug['Asian'], color = 'yellow', label= 'Asian')
    plt.bar(data_drug['Year'], data_drug['Hispanic'], color = 'green', label= 'Hispanic')
    plt.bar(data_drug['Year'], data_drug['Other'], color = 'blue', label= 'Other')
    plt.xlabel('Year')
    plt.ylabel('Number of Participants')
    plt.title('Race/Ethnicity Breakdown of Clinical Trials for {}'.format(drug))
    plt.legend()
    plt.show()

drug_for_analysis = 'X Drug'
by_drug(drug_for_analysis)

# Race/Ethnicity Breakdown of Clinical Trials: Data Analysis
total_participants_by_race = data.sum()
max_participants_by_race = data.max()
min_participants_by_race = data.min()
median_participants_by_race = data.median()
range_participants_by_race = max_participants_by_race - min_participants_by_race
perc_participants_by_race = data.div(data.sum(axis = 1), axis = 0) * 100
ave_participants_each_year = data.mean()
iqr_by_race = data.quantile(0.75) - data.quantile(0.25)

# Racial Diversity in Clinical Trials Conducted By Manufacturers: Line Graph
data_manufacturer = pd.read_csv("filename2.csv")

def by_manufacturer(manuf):
    """
    Filter race/ethnicity breakdown by manufacturer
    """
    data_manuf = data[data['Manufacturer'] == manuf]

    plt.figure(figsize = (10,6))
    plt.plot(data_manuf['Year'], data_manuf['Manufacturer_A'],
            marker = 'o', label = 'Manufacturer A')
    plt.plot(data_manuf['Year'], data_manuf['Manufacturer_B'],
            marker = 'o', label = 'Manufacturer B')
    plt.xlabel('Year')
    plt.ylabel('Number of Participants')
    plt.title(
        'Racial Diversity in Clinical Trials Conducted By Manufacturers for {}'.format(manuf))
    plt.legend()
    plt.grid(True)
    plt.show()

manuf_for_analysis = 'X Manufacturer'
by_manufacturer(manuf_for_analysis)

# Racial Diversity in Clinical Trials Conducted By Manufacturers: Data Analysis
total_participants_by_manufacturer = data_manufacturer.sum()
max_participants_by_race = data_manufacturer.max()
min_participants_by_race = data_manufacturer.min()
median_participants_by_race = data_manufacturer.median()
range_participants_by_race = max_participants_by_race - min_participants_by_race

# data.div(): Performs division on dataframe elements
# SOURCE: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.
# DataFrame.div.html
perc_participants_by_race = data_manufacturer.div(data.sum(axis = 1), 
                                                  axis = 0) * 100
ave_participants_each_year = data_manufacturer.mean()
iqr_by_race = data_manufacturer.quantile(0.75) - data_manufacturer.quantile(
    0.25)

# np.polyfit(): Calculates the least squares polynomial fit; slope
# SOURCE: https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html
slope_manufacturer_a = np.polyfit(data_manufacturer['Year'],
                                     data_manufacturer['Manufacturer_A'], 1)
slope_manufacturer_b = np.polyfit(data_manufacturer['Year'],
                                     data_manufacturer['Manufacturer_B'], 1)