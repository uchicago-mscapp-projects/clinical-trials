'''
Dashboard app
Authors:
    Visualizations: Kristy Kwon
    Dashboard: David Steffen
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
import pathlib

plt.switch_backend('Agg') 

# Import visualization functions
# from visualization import by_drug, by_manufacturer
# from visualization import summary_statistics_table, summary_statistics_manuf_table

# Read in data: connect to the SQL database
pth = pathlib.Path(__file__).parent / f"../../data/trials.db"
connection = sqlite3.connect(pth)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()


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

# table columns
tblcols= [{'name': 'Statistic', 'id': 'Stat'}, {'name': 'Value', 'id': 'Val'}]

# table rows
df_table = pd.DataFrame([{'Stat': 0, 'Val': 0}], columns=[col['name'] for col in tblcols])


if __name__ == '__main__':
    app.run_server(debug=True)

# Header
header_and_intro = html.Div([html.H1(children='Racial and Ethnic Representation in Clinical Trials',
                                style={'textAlign': 'center','color': colors['text']}),
                        html.Div(children='''Pharmaceutical companies use clinical trials to test the effectiveness of their products. 
                                 Clinical trials are required by the Food and Drug Administration (FDA) before new treatments are approved for use, 
                                 and their results are routinely used to determine which treatments patients should take to treat their medical conditions. ''',
                                style={'textAlign': 'left','color': colors['text'],'width' : '100%','padding' :5}),
                         html.Div(children='''The clinical trials implemented by pharmaceutical companies are crucial to ensure the effectiveness of their products and 
                                 determine the appropriate drugs for patients. However, many clinical trials do not enroll subjects who accurately 
                                 reflect the general population. In particular, there has been frequent underrepresentation of racial and ethnic minority 
                                 groups in clinical trials. The public has pushed for pharmaceutical companies to address these disparities through changes 
                                 in how they select participants to test their products. Affirming this importance, over 500 pharmaceutical organizations 
                                 have recently committed to increasing diversity in clinical trials.''',
                                style={'textAlign': 'left','color': colors['text'],'width' : '100%','padding' :5}),
                        html.Div(children='''Analysis of racial representation in the clinical trials data can shed light on the extent to 
                                 which companies have been successful in accounting for different identities and characteristics in their dataset over time.
                                 In this dashboard, we analyze representation in clinical trials for different treatments and identify trends over time. ''',
                                style={'textAlign': 'left','color': colors['text'],'width' : '100%','padding' :5})                               
                                ])

# Search by treatment section
search_treatment = html.Div([html.H2(children='Race and ethnicity representation in trials by treatment and condition',
                                      style={'textAlign': 'center','color': colors['text']}),
                            html.Div(children='''Users can select a treatment of interest by generic drug name, and information on that 
                                     drug will be populated, including a list of conditions the treatment has been tested for use in during
                                     clinical trials. After selecting one of those treatments, a visualization and summary table of racial
                                    and ethnic representation in trials for that treatment in that condition will be displayed.''',
                                     style={'textAlign': 'left','color': colors['text'],'width':'100%','padding' :10}),
                            html.Br(),
                            html.Div(children='''Please note that this data is limited to treatment-condition combinations with at least
                                     two trials reporting participant race/ethnicity data, and reporting participant race/ethnicity data 
                                     was not mandatory before 2017. Therefore, not all treatments may be 
                                     searchable, and not all conditions a treatment is indicated for may be searchable.''',
                                     style={'textAlign': 'left','color': colors['text'],'width':'100%','padding' :10}),
                            html.Br(),
                            html.Div(children='Choose a treatment of interest (generic name)', 
                                     style={'textAlign': 'left','color': colors['text'],'width':'100%','padding' :10}),
                        dcc.Dropdown(id='treatment-dropdown',
                            placeholder="Select a treatment", style={'width': '100%'}),
                        html.H3(id = 'generic_name',style={'textAlign': 'left','color': colors['text']}),
                        html.H3(id = 'brand_name',style={'textAlign': 'left','color': colors['text']}),
                        html.H3(id = 'manufacturer',style={'textAlign': 'left','color': colors['text']}),
                        html.H3(id = 'submission_year',style={'textAlign': 'left','color': colors['text']}),
                        html.H3(id = 'app_number',style={'textAlign': 'left','color': colors['text']}),
                        # Dropdown of the conditions for the treatment selected above
                        dcc.Dropdown(id='conditions-dropdown', 
                            placeholder="Select a condition the selected treatment is used for", style={'width': '100%'}),
                        html.Br(),
                        html.Div(children=[html.Iframe(
                            id="stacked-bar", srcDoc=None,
                            style={"border-width":"0","width":"100%","height":"600px"}
                            )]),
                        # Table of stats from visualization.py
                        dash_table.DataTable(id = "table-by-treatment", data = df_table.to_dict('records'))
                            ],
                            className = 'five columns')

# By manufacturer section
search_manufacturer = html.Div([html.H2(children='Trends in race and ethnicity representation over time by trial sponsor',
                                 style={'textAlign': 'center','color': colors['text']}),
                            html.Div(children='''Users can select a study sponsor of interest by generic drug name. After selecting a
                                     study sponsor, a visualization and summary table of racial
                                    and ethnic representation in trials sponsored by that company will be displayed.''',
                                     style={'textAlign': 'left','color': colors['text'],'width':'100%','padding' :10}),
                            html.Br(),
                            html.Div(children='''Please note that this data is limited to study sponsors with at least five trials
                                     reporting participant race/ethnicity data, and reporting participant race/ethnicity data 
                                     was not mandatory before 2017. As a result, not all study sponsors may be searchable.''',
                                     style={'textAlign': 'left','color': colors['text'],'width':'100%','padding' :10}),
                            html.Br(),
                            html.Div(children='''Choose the sponsor of interest''', 
                                     style={'textAlign': 'left','color': colors['text'],'width':'100%','padding' :10}),
                        dcc.Dropdown(id='manufacturer-dropdown',
                            placeholder="Select a study sponsor", style={'width': '100%'}),
                        html.Br(),
                        html.Div(children=[html.Iframe(
                            id="line-graph", srcDoc=None,
                            style={"border-width":"5","width":"100%","height":"600px", 'color': colors['text']}
                            )]),
                        dash_table.DataTable(id = "table-by-manufacturer", data = df_table.to_dict('records'))
                            ],
                        className = 'five columns')

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
    connection = sqlite3.connect(pth)
    connection.row_factory = sqlite3.Row

    trts_query = "SELECT DISTINCT TRIAL_INTERVENTIONS.intervention_name \
            from TRIAL_INTERVENTIONS INNER JOIN TRIAL_RACE \
            ON TRIAL_INTERVENTIONS.nct_id = TRIAL_RACE.nct_id \
            INNER JOIN TRIAL_CONDITIONS \
            ON TRIAL_INTERVENTIONS.nct_id = TRIAL_CONDITIONS.nct_id \
            WHERE TRIAL_RACE.WHITE IS NOT NULL \
            AND TRIAL_INTERVENTIONS.intervention_name NOT LIKE '%placebo%' \
            GROUP BY TRIAL_INTERVENTIONS.intervention_name, \
            TRIAL_CONDITIONS.condition \
            HAVING count(*) >= 2"

    trt_list = pd.read_sql_query(trts_query, connection)
    if not search_value:
        raise PreventUpdate

    return_vals = []
    for _, val in enumerate(trt_list.values):
        if val[0].startswith(search_value.lower()):
            return_vals.append(val[0])
    return return_vals


# Callback function for printing the generic name
@app.callback(
        Output(component_id = 'generic_name', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_generic(selected_trt):
    connection = sqlite3.connect(pth)
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
    connection = sqlite3.connect(pth)
    connection.row_factory = sqlite3.Row

    query = "SELECT distinct FDA_FULL.brand_name \
    FROM FDA_FULL \
    WHERE generic_name like ?"
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
    connection = sqlite3.connect(pth)
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


# Callback function for printing the submission year(s)
@app.callback(
        Output(component_id = 'submission_year', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_sub(selected_trt):
    connection = sqlite3.connect(pth)
    connection.row_factory = sqlite3.Row

    query = "SELECT distinct \
    CAST(SUBSTR(FDA_FULL.submission_status_date, 1, 4) AS integer) as Year \
    FROM FDA_FULL \
    WHERE generic_name like ?"
    if not selected_trt:
        raise PreventUpdate
    submission_year = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt,))
    
    return "Submission year(s): {}".format(', '.join(str(x) for x in submission_year["Year"]))


# Callback function for printing the application number(s)
@app.callback(
        Output(component_id = 'app_number', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_app(selected_trt):
    connection = sqlite3.connect(pth)
    connection.row_factory = sqlite3.Row

    query = "SELECT distinct FDA_FULL.application_number \
    FROM FDA_FULL \
    WHERE generic_name like ?"
    if not selected_trt:
        raise PreventUpdate
    app_number = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt,))
    
    return "Application number(s): {}".format(', '.join(app_number["application_number"]))


# Callback function for pulling list of conditions for the treatment
    # https://community.plotly.com/t/callback-interaction-between-2-core-components/24161
    # https://dash.plotly.com/basic-callbacks
@app.callback(
            Output('conditions-dropdown', 'options'),
        Input(component_id="treatment-dropdown", component_property='value')
        )
def update_output_conditions(selected_trt):
    connection = sqlite3.connect(pth)
    connection.row_factory = sqlite3.Row

    query = "SELECT distinct TRIAL_CONDITIONS.condition \
    FROM TRIAL_CONDITIONS \
    INNER JOIN TRIAL_INTERVENTIONS \
    ON TRIAL_CONDITIONS.nct_id = TRIAL_INTERVENTIONS.nct_id \
    INNER JOIN TRIAL_RACE \
    ON TRIAL_CONDITIONS.nct_id = TRIAL_RACE.nct_id \
    WHERE TRIAL_INTERVENTIONS.intervention_name = ? \
    AND TRIAL_RACE.WHITE IS NOT NULL \
    GROUP BY TRIAL_CONDITIONS.condition HAVING count(*) >=2"

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
    connection = sqlite3.connect(pth)
    connection.row_factory = sqlite3.Row

    query = "SELECT TRIAL_INTERVENTIONS.intervention_name, \
    TRIAL_CONDITIONS.condition, \
	COALESCE(SUM(TRIAL_RACE.asian), 0) AS Asian, \
	COALESCE(SUM(TRIAL_RACE.black), 0) AS Black, \
	COALESCE(SUM(TRIAL_RACE.white), 0) AS White, \
	COALESCE(SUM(TRIAL_RACE.hispanic_or_latino), 0) AS Hispanic, \
    COALESCE(SUM(TRIAL_RACE.american_indian_or_alaska_native + \
        TRIAL_RACE.hawaiian_or_pacific_islander + \
        TRIAL_RACE.multiple + TRIAL_RACE.unknown), 0) AS Other \
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
@app.callback(Output('table-by-treatment', 'data'),
        Input(component_id="treatment-dropdown", component_property='value'),
        Input(component_id="conditions-dropdown", component_property='value'))
def update_table_by_treatment(selected_trt, selected_cond):
    connection = sqlite3.connect(pth)
    connection.row_factory = sqlite3.Row

    query = "SELECT TRIAL_INTERVENTIONS.intervention_name, \
    TRIAL_CONDITIONS.condition, \
	COALESCE(SUM(TRIAL_RACE.asian), 0) AS Asian, \
	COALESCE(SUM(TRIAL_RACE.black), 0) AS Black, \
	COALESCE(SUM(TRIAL_RACE.white), 0) AS White, \
	COALESCE(SUM(TRIAL_RACE.hispanic_or_latino), 0) AS Hispanic, \
    COALESCE(SUM(TRIAL_RACE.american_indian_or_alaska_native + \
        TRIAL_RACE.hawaiian_or_pacific_islander + \
        TRIAL_RACE.multiple + TRIAL_RACE.unknown), 0) AS Other \
	FROM TRIAL_RACE INNER JOIN TRIAL_INTERVENTIONS \
	on TRIAL_RACE.nct_id = TRIAL_INTERVENTIONS.nct_id \
	INNER JOIN TRIAL_CONDITIONS \
	on TRIAL_RACE.nct_id = TRIAL_CONDITIONS.nct_id \
	WHERE TRIAL_INTERVENTIONS.intervention_name LIKE ? \
	AND TRIAL_CONDITIONS.CONDITION LIKE ? \
	GROUP BY TRIAL_INTERVENTIONS.intervention_name, TRIAL_CONDITIONS.condition"

    trt_trials = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt, selected_cond))

    if not selected_cond:
        raise PreventUpdate

    table_by_drug = summary_statistics_table(trt_trials, \
                                    selected_trt, selected_cond)

    title_first_part = 'Racial Diversity in Clinical Trials Conducted for '
    title_second_part = ' in '

    return table_by_drug.to_dict('records')


# Callback function for searching manufacturers
@app.callback(
        Output(component_id='manufacturer-dropdown', component_property='options'),
        Input(component_id="manufacturer-dropdown", component_property='search_value')
        )
def update_options(search_value):
    connection = sqlite3.connect(pth)
    connection.row_factory = sqlite3.Row

    manu_query = "SELECT DISTINCT lead_sponsor FROM TRIALS \
    INNER JOIN TRIAL_RACE \
    ON TRIALS.nct_id = TRIAL_RACE.nct_id \
    WHERE TRIAL_RACE.WHITE IS NOT NULL \
    GROUP BY lead_sponsor HAVING count(*) >= 5"

    manu_list = pd.read_sql_query(manu_query, connection)
    if not search_value:
        raise PreventUpdate
    return_vals = []
    for _, val in enumerate(manu_list.values):
        if val[0].startswith(search_value.upper()):
            return_vals.append(val[0])
    return return_vals


# Callback function for updating the line graph
@app.callback(
        Output(component_id='line-graph', component_property='srcDoc'),
        Input(component_id="manufacturer-dropdown", component_property='value')
        )
def update_linegraph(selected_manu):
    connection = sqlite3.connect(pth)
    connection.row_factory = sqlite3.Row

    query = "SELECT distinct TRIALS.lead_sponsor as Manufacturer, \
    CAST(SUBSTR(TRIAL_STATUS.start_date, 1, 4) AS integer) as Year, \
	COALESCE(SUM(TRIAL_RACE.asian), 0) AS Asian, \
	COALESCE(SUM(TRIAL_RACE.black), 0) AS Black, \
	COALESCE(SUM(TRIAL_RACE.white), 0) AS White, \
	COALESCE(SUM(TRIAL_RACE.hispanic_or_latino), 0) AS Hispanic, \
    COALESCE(SUM(TRIAL_RACE.american_indian_or_alaska_native + \
        TRIAL_RACE.hawaiian_or_pacific_islander + \
        TRIAL_RACE.multiple + TRIAL_RACE.unknown), 0) AS Other\
	FROM TRIALS INNER JOIN TRIAL_STATUS \
	on TRIALS.nct_id = TRIAL_STATUS.nct_id \
    INNER JOIN TRIAL_RACE \
	on TRIALS.nct_id = TRIAL_RACE.nct_id \
	WHERE TRIALS.lead_sponsor LIKE ? \
    and TRIAL_RACE.WHITE IS NOT NULL \
	GROUP BY Year"

    manu_trials = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_manu,))

    if not selected_manu:
        raise PreventUpdate

    fig = by_manufacturer(manu_trials, selected_manu)

    return fig


# Callback for updating the table underneath the line graph by manufacturer
    # https://community.plotly.com/t/display-tables-in-dash/4707/13
@app.callback(Output('table-by-manufacturer', 'data'), 
        Input(component_id="manufacturer-dropdown", component_property='value'))
def update_table_by_manufacturer(selected_manu):
    connection = sqlite3.connect(pth)
    connection.row_factory = sqlite3.Row

    query = "SELECT TRIALS.lead_sponsor as Manufacturer, \
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
	WHERE TRIALS.lead_sponsor LIKE ? \
	GROUP BY TRIALS.lead_sponsor"

    manu_trials = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_manu,))
    
    if not selected_manu:
        raise PreventUpdate

    table_by_manu = summary_statistics_manuf_table(manu_trials, selected_manu)

    title_first_part_manuf = 'Racial Diversity in Clinical Trials Conducted By Manufacturers for '

    return table_by_manu.to_dict('records')


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
