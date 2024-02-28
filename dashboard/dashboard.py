'''
Dashboard app
Author: David Steffen
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
import numpy as np

# Import visualization functions
from .visualization import by_drug, by_manufacturer
from .visualization import summary_statistics_table, summary_statistics_manufacturer_table

# Read in data: connect to the SQL database
connection = sqlite3.connect("data/trials.db")
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

# Define lists of possible treatments and of possible manufacturers
trials_query = "SELECT DISTINCT INTERVENTION FROM TRIAL_INTERVENTIONS"
trt_list = pd.read_sql_query(trials_query, connection)
#trt_list = pd.read_sql_query("SELECT DISTINCT intervention FROM trials", connection)
# trt_list = []
# for i in data['generic_name']:
#         trt_list.append(i)

manu_list = pd.read_sql_query("SELECT DISTINCT lead_sponsor FROM TRIALS", connection)

# Table function
    # https://dash.plotly.com/layout
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


##################################
### App structure  ###############
##################################

# App formatting inputs
colors = {
    'background': '#333eee',
    'text': '#a2bfe0'
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

# Header
header_and_intro = html.Div([html.H1(children='Racial and Ethnicity Representation in Clinical Trials',
                                style={'textAlign': 'center','color': colors['text']}),
                        html.Div(children='''Placeholder ''',
                                style={'textAlign': 'left','color': colors['text'],'width' : '100%','padding' :5})])

# Search by treatment section
search_treatment = html.Div([html.H2(children='Search by treatment',
                                      style={'textAlign': 'center','color': colors['text']}),
                            html.Div(children='''Placeholder''',
                                     style={'textAlign': 'left','color': colors['text'],'width':'100%','padding' :10}),
                            html.Br(),
                            html.Div(children='''Choose the treatment of interest'''),
                        dcc.Dropdown(id='treatment-dropdown', options=trt_list, 
                            placeholder="Select a treatment", style={'width': '100%'}),
                        html.H3(id = 'generic_name',style={'textAlign': 'left','color': colors['text']}),
                        html.H3(id = 'brand_name',style={'textAlign': 'left','color': colors['text']}),
                        html.H3(id = 'manufacturer',style={'textAlign': 'left','color': colors['text']}),
                        # Dropdown of the conditions for the treatment selected above
                        dcc.Dropdown(id='conditions-dropdown', 
                            placeholder="Select a condition the treatment is used for", style={'width': '100%'}),
                        html.Br(),
                        dcc.Graph(id='stacked-bar', style={'width': '100%'})],
                        # Table of stats from visualization.py
                        html.Div(id='table-by-treatment'),
                        # dash_table.DataTable(),
                            className = 'five columns')

# By manufacturer section
search_manufacturer = html.Div([html.H2(children='Search by manufacturer',
                                 style={'textAlign': 'center','color': colors['text']}),
                            html.Div(children='''Placeholder''',
                                     style={'textAlign': 'left','color': colors['text'],'width':'100%','padding' :10}),
                            html.Br(),
                            html.Div(children='''Choose the manufacturer of interest'''),
                        dcc.Dropdown(id='manufacturer-dropdown', options=manu_list,
                            placeholder="Select a manufacturer", style={'width': '100%'}),
                        html.Br(),
                        dcc.Graph(id='line-graph', style={'width': '100%'})],
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
        input = Input(component_id="treatment-dropdown", component_property='search-value')
        )
def update_options(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in trt_list if search_value in o]

# Callback function for printing the generic name
@app.callback(
        Output(component_id = 'generic-name', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_generic(selected_trt):
    query = "SELECT distinct TRIAL_INTERVENTIONS.brand_name \
    FROM TRIAL_INTERVENTIONS \
    WHERE INTERVENTION = ?"    

    generic_name = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt))

    return "Generic name: {}".format(generic_name)

# Callback function for printing the brand name(s)
@app.callback(
        Output(component_id = 'brand-name', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_brand(selected_trt):
    query = "SELECT distinct TRIAL_INTERVENTIONS.brand_name \
    FROM TRIAL_INTERVENTIONS \
    WHERE INTERVENTION = ?"
    # query = "SELECT distinct brand_name FROM trials WHERE generic_name = ?"

    brand_name = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt))
    #row = data.loc[data['generic_name'] == selected_trt]
    #brand_name = row['brand_name']
    
    return "Brand name(s): {}".format(brand_name)

# Callback function for printing the manufacturer name
@app.callback(
        Output(component_id = 'manufacturer', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_manufacturer(selected_trt):
    query = "SELECT distinct TRIALS.lead_sponsor \
    FROM TRIAL_INTERVENTIONS \
    INNER JOIN TRIALS \
    ON TRIAL_INTERVENTIONS.nct_id = TRIALS.nct_id \
    WHERE TRIAL_INTERVENTIONS.INTERVENTION = ?"
    # query = "SELECT distinct manufacturer FROM trials WHERE generic_name = ?"

    manufacturer = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt))
    return "Manufacturer: {}".format(manufacturer)

# Callback function for pulling list of conditions for the treatment
    # https://community.plotly.com/t/callback-interaction-between-2-core-components/24161
    # https://dash.plotly.com/basic-callbacks
@app.callback(
        [Output('conditions-dropdown', 'options'),
            Output('conditions-dropdown', 'value')],
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_conditions(selected_trt):
    query = "SELECT distinct TRIAL_CONDITIONS.CONDITION \
    FROM TRIAL_INTERVENTIONS \
    INNER JOIN TRIAL_CONDITIONS \
    ON TRIAL_INTERVENTIONS.nct_id = TRIAL_CONDITIONS.nct_id \
    WHERE TRIAL_INTERVENTIONS.INTERVENTION = ?"
    # query = "SELECT distinct conditions FROM trial_conditions WHERE generic_name = ?"

    conditions = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt))
    return conditions


# Callback function for updating the stacked bar chart
@app.callback(
        Output(component_id='stacked-bar', component_property='figure'),
        Input(component_id="treatment-dropdown", component_property='value'),
        Input(component_id="conditions-dropdown", component_property='value')
        )

def update_stackedbar(selected_trt, selected_cond):
    # make sure the like is case insensitive
    query = "SELECT RACE_BY_TRIAL.RACE FROM RACE_BY_TRIAL \
    INNER JOIN TRIAL_INTERVENTIONS \
    on TRIALS.nct_id = TRIAL_INTERVENTIONS.nct_id \
    INNER JOIN TRIAL_CONDITIONS \
    on RACE_BY_TRIAL.nct_id = TRIAL_CONDITIONS.nct_id \
    WHERE TRIAL_INTERVENTIONS.INTERVENTION LIKE ? \
    AND TRIAL_CONDITIONS.CONDITION LIKE ?"
    # query = "SELECT * FROM trials WHERE generic_name = ? AND condition = ?"

    trt_trials = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt, selected_cond))

    fig = by_drug(trt_trials)

    return fig


# Callback for updating the table underneath the stacked bar chart
    # https://community.plotly.com/t/display-tables-in-dash/4707/13
@app.callback(Output('table-by-treatment', 'children'), 
        Input(component_id="treatment-dropdown", component_property='value'),
        Input(component_id="conditions-dropdown", component_property='value'))
def update_table(selected_trt, selected_cond):
    query = "SELECT RACE_BY_TRIAL.RACE FROM RACE_BY_TRIAL \
    INNER JOIN TRIAL_INTERVENTIONS \
    on TRIALS.nct_id = TRIAL_INTERVENTIONS.nct_id \
    INNER JOIN TRIAL_CONDITIONS \
    on RACE_BY_TRIAL.nct_id = TRIAL_CONDITIONS.nct_id \
    WHERE TRIAL_INTERVENTIONS.INTERVENTION LIKE ? \
    AND TRIAL_CONDITIONS.CONDITION LIKE ?"
    # query = "SELECT * FROM trials WHERE generic_name = ? AND condition = ?"

    trt_trials = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt, selected_cond))
    
    table_by_drug = summary_statistics_table(trt_trials)

    return generate_table(table_by_drug)


# Callback function for searching manufacturers
@app.callback(
        Output(component_id='manufacturer-dropdown', component_property='options'),
        Input(component_id="manufacturer-dropdown", component_property='search-value')
        )
def update_options(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in manu_list if search_value in o]

# Callback function for updating the line graph
@app.callback(
        Output(component_id='line-graph', component_property='figure'),
        Input(component_id="manufacturer-dropdown", component_property='value')
        )
def update_linegraph(selected_manu):
    query = "SELECT RACE_BY_TRIAL.RACE FROM RACE_BY_TRIAL \
    INNER JOIN TRIALS \
    on RACE_BY_TRIAL.nct_id = TRIALS.nct_id \
    WHERE TRIALS.lead_sponsor LIKE ? "
    # query = "SELECT * FROM trials WHERE manufacturer = ?"
    manu_trials = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_manu))

    fig = by_manufacturer(manu_trials)

    return fig

# Callback for updating the table underneath the line graph by manufacturer
    # https://community.plotly.com/t/display-tables-in-dash/4707/13
@app.callback(Output('table-by-manufacturer', 'children'), 
        Input(component_id="manufacturer-dropdown", component_property='value'))
def update_table(selected_manu):
    query = "SELECT RACE_BY_TRIAL.RACE FROM RACE_BY_TRIAL \
    INNER JOIN TRIALS \
    on RACE_BY_TRIAL.nct_id = TRIALS.nct_id \
    WHERE TRIALS.lead_sponsor LIKE ? "
    # query = "SELECT * FROM trials WHERE manufacturer = ?"

    manu_trials = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_manu))
    
    table_by_manu = summary_statistics_manufacturer_table(manu_trials)

    return generate_table(table_by_manu)
