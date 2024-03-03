'''
Dashboard app
Authors:
    Table function: Kristy Kwon
    Rest of dashboard: David Steffen
'''

##################################
### Setup and data import  #######
##################################

# Import statements
import pandas as pd
import sqlite3
import dash
from dash import html, dcc, Dash, dash_table, State, callback
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash import dcc
from dash import html
import numpy as np
import matplotlib.pyplot as plt
import mpld3

plt.switch_backend('Agg') 

# Import visualization functions
# from visualization import by_drug, by_manufacturer
# from visualization import summary_statistics_table, summary_statistics_manuf_table

# Read in data: connect to the SQL database
connection = sqlite3.connect("data/trials.db")
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

# Define lists of possible treatments and of possible manufacturers
# Pull interventions tested in at least 5 trials
# trts_query = "SELECT DISTINCT intervention_name from TRIAL_INTERVENTIONS \
#         GROUP BY INTERVENTION_NAME HAVING count(*) >= 5"
# trt_list = pd.read_sql_query(trts_query, connection)

# Pull manufacturers who have sponsored at least 5 trials
# manu_query = "SELECT DISTINCT sponsor_name FROM FDA_FULL \
#     GROUP BY sponsor_name HAVING count(*) >= 5"
# manu_list = pd.read_sql_query(manu_query, connection)



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


##################################
### App structure  ###############
##################################

# App formatting inputs
colors = {
    'background': '#111885',
    'text': '#accdf2'
}

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# App call
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

if __name__ == '__main__':
    app.run_server(debug=True)

# Header
header_and_intro = html.Div([html.H1(children='Racial and Ethnicity Representation in Clinical Trials',
                                style={'textAlign': 'center','color': colors['text']}),
                        html.Div(children='''Placeholder ''',
                                style={'textAlign': 'left','color': colors['text'],'width' : '100%','padding' :5})])

# Search by treatment section
search_treatment = html.Div([html.H2(children='Search by treatment',
                                      style={'textAlign': 'center','color': colors['text']}),
                            html.Div(children='Placeholder',
                                     style={'textAlign': 'left','color': colors['text'],'width':'100%','padding' :10}),
                            html.Br(),
                            html.Div(children='Choose the treatment of interest'),
                        dcc.Dropdown(id='treatment-dropdown', #options=trt_list, 
                            placeholder="Select a treatment", style={'width': '100%'}),
                        html.H3(id = 'generic_name',style={'textAlign': 'left','color': colors['text']}),
                        html.H3(id = 'brand_name',style={'textAlign': 'left','color': colors['text']}),
                        html.H3(id = 'manufacturer',style={'textAlign': 'left','color': colors['text']}),
                        # Dropdown of the conditions for the treatment selected above
                        dcc.Dropdown(id='conditions-dropdown', 
                            placeholder="Select a condition the treatment is used for", style={'width': '100%'}),
                        html.Br(),
                        html.Div(children=[html.Iframe(
                            id="stacked-bar", srcDoc=None,
                            style={"border-width":"0","width":"100%","height":"600px"}
                            )]) ],
                        #dcc.Graph(id='stacked-bar', style={'width': '100%'})],
                        # Table of stats from visualization.py
                        # dash_table.DataTable(
                        #     id='table-by-treatment',
                        #     columns=[
                        #     {'name': 'Stat', 'id': 'Statistic'},
                        #     {'name': 'Val', 'id': 'Value'}]) ],
                        #html.Div(id='table-by-treatment')],
                        #html.Div([dash_table.DataTable(id='table-by-treatment')])],
                            className = 'five columns')

# By manufacturer section
search_manufacturer = html.Div([html.H2(children='Search by manufacturer',
                                 style={'textAlign': 'center','color': colors['text']}),
                            html.Div(children='Placeholder',
                                     style={'textAlign': 'left','color': colors['text'],'width':'100%','padding' :10}),
                            html.Br(),
                            html.Div(children='Choose the manufacturer of interest'),
                        dcc.Dropdown(id='manufacturer-dropdown', #options=manu_list,
                            placeholder="Select a manufacturer", style={'width': '100%'}),
                        html.Br(),
                        html.Div(children=[html.Iframe(
                            id="line-graph", srcDoc=None,
                            style={"border-width":"5","width":"100%","height":"600px"}
                            )]) ],
                        #dcc.Graph(id='line-graph', style={'width': '100%'})],
                         className = 'five columns'
                        # Table of stats from visualization.py
                        #html.Div([dash_table.DataTable(id='table-by-manufacturer')])],
                        # dash_table.DataTable(
                        #     id='table-by-manufacturer',
                        #     columns=[
                        #     {'name': 'Stat', 'id': 'Statistic'},
                        #     {'name': 'Val', 'id': 'Value'}]) ],
                        #html.Div(id='table-by-manufacturer')],
                      )

# Define app layout
app.layout = html.Div(children=[
    html.Div(header_and_intro, style={"grid-area":"header"}),
    html.Div(search_treatment, style={"grid-area":"graph_1"}),
    html.Div(search_manufacturer, style={"grid-area":"graph_2"})],
                      style={
                          'backgroundColor': colors['background'],
                          'display': 'grid',
                          'grid-template-areas': """
                          'header header'
                          'graph_1 graph_2'
                          """,
                          'grid-gap': '10px',
                          'grid-template-columns': 'minmax(300px, 1000px) minmax(300px, 1000px)',
                          'grid-template-rows': 'auto 1fr 1fr'
                      })


##################################
### Callback functions ###########
##################################

# Callback function for searching treatments
    # https://dash.plotly.com/dash-core-components/dropdown
@app.callback(
        Output(component_id = 'treatment-dropdown', component_property ='options'),
        Input(component_id="treatment-dropdown", component_property='search_value')
        )
def update_options(search_value):
    connection = sqlite3.connect("data/trials.db")
    connection.row_factory = sqlite3.Row
    
    trts_query = "SELECT DISTINCT intervention_name from TRIAL_INTERVENTIONS \
            GROUP BY INTERVENTION_NAME HAVING count(*) >= 5"
    trt_list = pd.read_sql_query(trts_query, connection)
    if not search_value:
        raise PreventUpdate
    return_vals = []
    for _, val in enumerate(trt_list.values):
        if val[0].startswith(search_value):
            return_vals.append(val[0])
    return return_vals


# Callback function for printing the generic name
@app.callback(
        Output(component_id = 'generic_name', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_generic(selected_trt):
    connection = sqlite3.connect("data/trials.db")
    connection.row_factory = sqlite3.Row

    query = "SELECT distinct TRIAL_INTERVENTIONS.intervention_name \
    FROM TRIAL_INTERVENTIONS \
    WHERE intervention_name = ?"    
    if not selected_trt:
        raise PreventUpdate
    generic_name = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt,))

    return "Generic name: {}".format(', '.join(generic_name["intervention_name"]))


# Callback function for printing the brand name(s)
@app.callback(
        Output(component_id = 'brand_name', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_brand(selected_trt):
    connection = sqlite3.connect("data/trials.db")
    connection.row_factory = sqlite3.Row

    query = "SELECT distinct FDA_FULL.brand_name \
    FROM FDA_FULL \
    WHERE generic_name = ?"
    if not selected_trt:
        raise PreventUpdate
    brand_name = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt,))
    
    return "Brand name(s): {}".format(', '.join(brand_name["brand_name"]))


# Callback function for printing the manufacturer name
@app.callback(
        Output(component_id = 'manufacturer', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

# Pull manufacturers who have sponsored at least 2 trials
def update_output_manufacturer(selected_trt):
    connection = sqlite3.connect("data/trials.db")
    connection.row_factory = sqlite3.Row

    query = "SELECT DISTINCT trials.lead_sponsor \
    FROM TRIALS \
    INNER JOIN TRIAL_INTERVENTIONS \
    ON TRIAL_INTERVENTIONS.nct_id = TRIALS.nct_id \
    WHERE TRIAL_INTERVENTIONS.intervention_name  = ? \
    GROUP BY TRIALS.lead_sponsor \
    HAVING count(*) >=2"

    if not selected_trt:
        raise PreventUpdate
    manufacturer = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt,))

    return "Manufacturer(s): {}".format(', '.join(manufacturer["lead_sponsor"]))


# Callback function for pulling list of conditions for the treatment
    # https://community.plotly.com/t/callback-interaction-between-2-core-components/24161
    # https://dash.plotly.com/basic-callbacks
@app.callback(
            Output('conditions-dropdown', 'options'),
        Input(component_id="treatment-dropdown", component_property='value')
        )
def update_output_conditions(selected_trt):
    connection = sqlite3.connect("data/trials.db")
    connection.row_factory = sqlite3.Row

    query = "SELECT distinct TRIAL_CONDITIONS.condition \
    FROM TRIAL_CONDITIONS \
    INNER JOIN TRIAL_INTERVENTIONS \
    ON TRIAL_CONDITIONS.nct_id = TRIAL_INTERVENTIONS.nct_id \
    INNER JOIN TRIAL_RACE \
    ON TRIAL_CONDITIONS.nct_id = TRIAL_RACE.nct_id \
    WHERE TRIAL_INTERVENTIONS.intervention_name = ? \
    AND TRIAL_RACE.WHITE IS NOT NULL"

    conditions = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt,))
    if not selected_trt:
        raise PreventUpdate
    return_vals = []
    for _, val in enumerate(conditions.values):
        return_vals.append(val[0])
    return return_vals

# Callback function for updating the stacked bar chart
@app.callback(
        Output(component_id='stacked-bar', component_property='srcDoc'),
        Input(component_id="treatment-dropdown", component_property='value'),
        Input(component_id="conditions-dropdown", component_property='value')
        )
def update_stackedbar(selected_trt, selected_cond):
    connection = sqlite3.connect("data/trials.db")
    connection.row_factory = sqlite3.Row

    query = "SELECT TRIAL_INTERVENTIONS.intervention_name, \
    TRIAL_CONDITIONS.condition, \
	COALESCE(SUM(TRIAL_RACE.asian), 0) AS Asian, \
	COALESCE(SUM(TRIAL_RACE.black), 0) AS Black, \
	COALESCE(SUM(TRIAL_RACE.white), 0) AS White, \
	COALESCE(SUM(TRIAL_RACE.hispanic_or_latino), 0) AS Hispanic, \
    COALESCE(SUM(TRIAL_RACE.american_indian_or_alaska_native + \
        TRIAL_RACE.hawaiian_or_pacific_islander + \
        TRIAL_RACE.multiple + TRIAL_RACE.unknown), 0) AS Other, \
	SUM(TRIAL_RACE.american_indian_or_alaska_native) AS AIAN, \
	SUM(TRIAL_RACE.hawaiian_or_pacific_islander) AS HPI, \
	SUM(TRIAL_RACE.multiple) AS multi_race, \
	SUM(TRIAL_RACE.unknown) AS unknown \
	FROM TRIAL_RACE INNER JOIN TRIAL_INTERVENTIONS \
	on TRIAL_RACE.nct_id = TRIAL_INTERVENTIONS.nct_id \
	INNER JOIN TRIAL_CONDITIONS \
	on TRIAL_RACE.nct_id = TRIAL_CONDITIONS.nct_id \
	WHERE TRIAL_INTERVENTIONS.intervention_name LIKE ? \
	AND TRIAL_CONDITIONS.CONDITION LIKE ? \
	GROUP BY TRIAL_INTERVENTIONS.intervention_name, TRIAL_CONDITIONS.condition"

    if not selected_cond:
        raise PreventUpdate

    trt_trials = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt, selected_cond))

    fig = by_drug(trt_trials, selected_trt, selected_cond)

    return fig


# Callback for updating the table underneath the stacked bar chart
    # https://community.plotly.com/t/display-tables-in-dash/4707/13
# @app.callback(Output('table-by-treatment', 'data'), 
#         Input(component_id="treatment-dropdown", component_property='value'),
#         Input(component_id="conditions-dropdown", component_property='value'))
# def update_table_by_treatment(selected_trt, selected_cond):
#     connection = sqlite3.connect("data/trials.db")
#     connection.row_factory = sqlite3.Row

#     query = "SELECT TRIAL_INTERVENTIONS.intervention_name, \
#     TRIAL_CONDITIONS.condition, \
# 	COALESCE(SUM(TRIAL_RACE.asian), 0) AS Asian, \
# 	COALESCE(SUM(TRIAL_RACE.black), 0) AS Black, \
# 	COALESCE(SUM(TRIAL_RACE.white), 0) AS White, \
# 	COALESCE(SUM(TRIAL_RACE.hispanic_or_latino), 0) AS Hispanic, \
#     COALESCE(SUM(TRIAL_RACE.american_indian_or_alaska_native + \
#         TRIAL_RACE.hawaiian_or_pacific_islander + \
#         TRIAL_RACE.multiple + TRIAL_RACE.unknown), 0) AS Other,\
# 	SUM(TRIAL_RACE.american_indian_or_alaska_native) AS AIAN, \
# 	SUM(TRIAL_RACE.hawaiian_or_pacific_islander) AS HPI, \
# 	SUM(TRIAL_RACE.multiple) AS multi_race, \
# 	SUM(TRIAL_RACE.unknown) AS unknown \
# 	FROM TRIAL_RACE INNER JOIN TRIAL_INTERVENTIONS \
# 	on TRIAL_RACE.nct_id = TRIAL_INTERVENTIONS.nct_id \
# 	INNER JOIN TRIAL_CONDITIONS \
# 	on TRIAL_RACE.nct_id = TRIAL_CONDITIONS.nct_id \
# 	WHERE TRIAL_INTERVENTIONS.intervention_name LIKE ? \
# 	AND TRIAL_CONDITIONS.CONDITION LIKE ? \
# 	GROUP BY TRIAL_INTERVENTIONS.intervention_name, TRIAL_CONDITIONS.condition"

#     trt_trials = pd.read_sql_query(sql = query, 
#                       con = connection,
#                       params = (selected_trt, selected_cond))

#     table_by_drug = summary_statistics_table(trt_trials, \
#                                     selected_trt, selected_cond)

#     title_first_part = 'Racial Diversity in Clinical Trials Conducted for '
#     title_second_part = ' in '

#     return table_by_drug.to_dict()
    # return generate_table(table_by_drug, 
    #         title = title_first_part + '{}'.format(selected_trt) + \
    #             title_second_part + '{}'.format(selected_cond))


# Callback function for searching manufacturers
@app.callback(
        Output(component_id='manufacturer-dropdown', component_property='options'),
        Input(component_id="manufacturer-dropdown", component_property='search_value')
        )
def update_options(search_value):
    connection = sqlite3.connect("data/trials.db")
    connection.row_factory = sqlite3.Row

    manu_query = "SELECT DISTINCT lead_sponsor FROM TRIALS \
        GROUP BY lead_sponsor HAVING count(*) >= 5"
    manu_list = pd.read_sql_query(manu_query, connection)
    if not search_value:
        raise PreventUpdate
    return_vals = []
    for _, val in enumerate(manu_list.values):
        if val[0].startswith(search_value):
            return_vals.append(val[0])
    return return_vals


# Callback function for updating the line graph
@app.callback(
        Output(component_id='line-graph', component_property='srcDoc'),
        Input(component_id="manufacturer-dropdown", component_property='value')
        )
def update_linegraph(selected_manu):
    connection = sqlite3.connect("data/trials.db")
    connection.row_factory = sqlite3.Row

    query = "SELECT TRIALS.lead_sponsor as Manufacturer, \
    CAST(SUBSTR(TRIAL_STATUS.start_date, 1, 4) AS integer) as Year, \
	COALESCE(SUM(TRIAL_RACE.asian), 0) AS Asian, \
	COALESCE(SUM(TRIAL_RACE.black), 0) AS Black, \
	COALESCE(SUM(TRIAL_RACE.white), 0) AS White, \
	COALESCE(SUM(TRIAL_RACE.hispanic_or_latino), 0) AS Hispanic, \
    COALESCE(SUM(TRIAL_RACE.american_indian_or_alaska_native + \
        TRIAL_RACE.hawaiian_or_pacific_islander + \
        TRIAL_RACE.multiple + TRIAL_RACE.unknown), 0) AS Other,\
	SUM(TRIAL_RACE.american_indian_or_alaska_native) AS AIAN, \
	SUM(TRIAL_RACE.hawaiian_or_pacific_islander) AS HPI, \
	SUM(TRIAL_RACE.multiple) AS multi_race, \
	SUM(TRIAL_RACE.unknown) AS unknown \
	FROM TRIAL_RACE INNER JOIN TRIALS \
	on TRIAL_RACE.nct_id = TRIALS.nct_id \
    INNER JOIN TRIAL_STATUS \
	on TRIAL_RACE.nct_id = TRIALS.nct_id \
	WHERE TRIALS.lead_sponsor LIKE ? \
	GROUP BY TRIALS.lead_sponsor, \
    CAST(SUBSTR(TRIAL_STATUS.start_date, 1, 4) AS integer)"

    manu_trials = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_manu,))

    if not selected_manu:
        raise PreventUpdate

    fig = by_manufacturer(manu_trials, selected_manu)

    return fig


# Callback for updating the table underneath the line graph by manufacturer
    # https://community.plotly.com/t/display-tables-in-dash/4707/13
# @app.callback(Output('table-by-manufacturer', 'data'), 
#         Input(component_id="manufacturer-dropdown", component_property='value'))
# def update_table_by_manufacturer(selected_manu):
#     connection = sqlite3.connect("data/trials.db")
#     connection.row_factory = sqlite3.Row

#     query = "SELECT TRIALS.lead_sponsor as Manufacturer, \
# 	COALESCE(SUM(TRIAL_RACE.asian), 0) AS Asian, \
# 	COALESCE(SUM(TRIAL_RACE.black), 0) AS Black, \
# 	COALESCE(SUM(TRIAL_RACE.white), 0) AS White, \
# 	COALESCE(SUM(TRIAL_RACE.hispanic_or_latino), 0) AS Hispanic, \
#     COALESCE(SUM(TRIAL_RACE.american_indian_or_alaska_native + \
#         TRIAL_RACE.hawaiian_or_pacific_islander + \
#         TRIAL_RACE.multiple + TRIAL_RACE.unknown), 0) AS Other,\
# 	SUM(TRIAL_RACE.american_indian_or_alaska_native) AS AIAN, \
# 	SUM(TRIAL_RACE.hawaiian_or_pacific_islander) AS HPI, \
# 	SUM(TRIAL_RACE.multiple) AS multi_race, \
# 	SUM(TRIAL_RACE.unknown) AS unknown \
# 	FROM TRIAL_RACE INNER JOIN TRIALS \
# 	on TRIAL_RACE.nct_id = TRIALS.nct_id \
# 	WHERE TRIALS.lead_sponsor LIKE ? \
# 	GROUP BY TRIALS.lead_sponsor"
#     # query = "SELECT * FROM trials WHERE manufacturer = ?"

#     manu_trials = pd.read_sql_query(sql = query, 
#                       con = connection,
#                       params = (selected_manu,))
    
#     table_by_manu = summary_statistics_manuf_table(manu_trials, selected_manu)

#     title_first_part_manuf = 'Racial Diversity in Clinical Trials Conducted By Manufacturers for '

#     return table_by_manu.to_dict()
    # return generate_table(table_by_manu, 
    #         title = title_first_part_manuf + '{}'.format(selected_manu))


def by_drug(data_drug, treatment_of_interest, condition_of_interest):
    """
    Filter race/ethnicity breakdown by treatment and condition 
    """
    # SOURCE: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.
    # html
    f = plt.figure(figsize = (10,6))
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
        title_treatment_of_interest = f' {treatment_of_interest}'
    else:
        title_treatment_of_interest = ''
    if condition_of_interest:
        title_condition_of_interest = f' {condition_of_interest}'
    else:
        title_condition_of_interest = ''
    title = title_first_part + title_treatment_of_interest + ' in ' + title_condition_of_interest

    plt.title(title)
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

    total_participants_by_drug = data_drug.sum(axis = 1)
    max_participants_by_drug = data_drug.max(axis = 1)
    min_participants_by_drug = data_drug.min(axis = 1)
    ave_participants_by_drug = data_drug.mean(axis = 1)
    median_participants_by_drug = data_drug.median(axis = 1)
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
                # 'Percentage of Participants By Drug', 
                # 'Average Participants By Drug For Each Race', 
                # 'Interquartile Range of Participants By Drug',
                'Missing Observations'],
        'Val': [total_participants_by_drug, max_participants_by_drug,
                min_participants_by_drug, ave_participants_by_drug, 
                median_participants_by_drug,
                range_participants_by_drug, 
                # perc_participants_by_drug,
                # ave_participants_by_drug_each_race, iqr_by_drug, 
                na_drug]
    })

    return df_manuf



# Racial Diversity in Clinical Trials Conducted By Manufacturers: Line Graph

def by_manufacturer(data_manuf, manuf):
    """
    Filter race/ethnicity breakdown by manufacturer
    """
    # SOURCE: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.
    # html
    f = plt.figure(figsize = (10,6))

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

    title_first_part_manuf = 'Racial Diversity in Clinical Trials Conducted By '
    title_manuf = title_first_part_manuf + '{}'.format(manuf)
    plt.title(title_manuf)
    
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

    total_participants_by_manufacturer = data_manuf.sum(axis = 1)
    max_participants_by_manufacturer = data_manuf.max(axis = 1)
    min_participants_by_manufacturer = data_manuf.min(axis = 1)
    ave_participants_by_manufacturer = data_manuf.mean(axis = 1)
    median_participants_by_manufacturer = data_manuf.median(axis = 1)
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
    #print(na_manufacturer)

    # Put Summary Statistics in a dataframe to be used for dashboard viz
    df_manuf = pd.DataFrame({
        'Stat': ['Total Participants By Manufacturer', 
                'Maximum Participants By Manufacturer', 
                'Minimum Participants By Manufacturer',
                'Average Participants By Manufacturer',
                'Median Participants By Manufacturer', 
                'Range of Participants By Manufacturer',
                # 'Percentage of Participants By Manufacturer', 
                # 'Average Participants Each Year', 
                # 'Interquartile Range of Participants By Manufacturer',
                'Missing Observations'],
        'Val': [total_participants_by_manufacturer, 
                max_participants_by_manufacturer,
                min_participants_by_manufacturer, 
                ave_participants_by_manufacturer,
                median_participants_by_manufacturer, 
                range_participants_by_manufacturer, 
                # perc_participants_by_manufacturer,
                # ave_participants_by_manufacturer_each_race, 
                # iqr_by_manufacturer, 
                na_manufacturer]
    })

    return df_manuf
