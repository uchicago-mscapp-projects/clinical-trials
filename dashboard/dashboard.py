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
import numpy as np

# Import visualization functions
from .visualization import by_drug, by_manufacturer
from .visualization import summary_statistics_table, summary_statistics_manuf_table

# Read in data: connect to the SQL database
connection = sqlite3.connect("data/trials.db")
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

# Define lists of possible treatments and of possible manufacturers
# Pull interventions tested in at least 5 trials
trials_query = "SELECT DISTINCT intervention_name from TRIAL_INTERVENTIONS \
        GROUP BY INTERVENTION_NAME HAVING count(*) >= 5"
trt_list = pd.read_sql_query(trials_query, connection)

# Pull manufacturers who have sponsored at least 5 trials
manu_query = "SELECT DISTINCT lead_sponsor FROM TRIALS \
    GROUP BY lead_sponsor HAVING count(*) >= 5"
manu_list = pd.read_sql_query(manu_query, connection)



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
                        # Table of stats from visualization.py
                        html.Div(id='table-by-manufacturer'),
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
    query = "SELECT distinct TRIAL_INTERVENTIONS.generic_name \
    FROM TRIAL_INTERVENTIONS \
    WHERE intervention_name = ?"    

    generic_name = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt,))

    return "Generic name: {}".format(generic_name)


# Callback function for printing the brand name(s)
@app.callback(
        Output(component_id = 'brand-name', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_brand(selected_trt):
    query = "SELECT distinct TRIAL_INTERVENTIONS.brand_name \
    FROM TRIAL_INTERVENTIONS \
    WHERE intervention_name = ?"

    brand_name = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt,))
    
    return "Brand name(s): {}".format(brand_name)


# Callback function for printing the manufacturer name
@app.callback(
        Output(component_id = 'manufacturer', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

# Pull manufacturers who have sponsored at least 2 trials
def update_output_manufacturer(selected_trt):
    query = "SELECT DISTINCT trials.lead_sponsor \
    FROM TRIALS \
    INNER JOIN TRIAL_INTERVENTIONS \
    ON TRIAL_INTERVENTIONS.nct_id = TRIALS.nct_id \
    WHERE TRIAL_INTERVENTIONS.intervention_name  = ? \
    GROUP BY TRIALS.lead_sponsor \
    HAVING count(*) >=2"
    # query = "SELECT distinct manufacturer FROM trials WHERE generic_name = ?"

    manufacturer = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt,))

    return "Manufacturer(s): {}".format(', '.join(manufacturer["lead_sponsor"]))


# Callback function for pulling list of conditions for the treatment
    # https://community.plotly.com/t/callback-interaction-between-2-core-components/24161
    # https://dash.plotly.com/basic-callbacks
@app.callback(
        [Output('conditions-dropdown', 'options'),
            Output('conditions-dropdown', 'value')],
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_conditions(selected_trt):
    query = "SELECT distinct TRIAL_CONDITIONS.condition \
    FROM TRIAL_CONDITIONS \
    INNER JOIN TRIAL_INTERVENTIONS \
    ON TRIAL_CONDITIONS.nct_id = TRIAL_INTERVENTIONS.nct_id \
    WHERE TRIAL_INTERVENTIONS.intervention_name = ?"
    # query = "SELECT distinct conditions FROM trial_conditions WHERE generic_name = ?"

    conditions = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt,))
    return conditions


# Callback function for updating the stacked bar chart
@app.callback(
        Output(component_id='stacked-bar', component_property='figure'),
        Input(component_id="treatment-dropdown", component_property='value'),
        Input(component_id="conditions-dropdown", component_property='value')
        )

def update_stackedbar(selected_trt, selected_cond):
    # make sure the like is case insensitive
    query = "SELECT TRIAL_INTERVENTIONS.intervention_name, \
    TRIAL_CONDITIONS.condition, \
	SUM(TRIAL_RACE.asian) AS Asian, \
	SUM(TRIAL_RACE.black) AS Black, \
	SUM(TRIAL_RACE.white) AS White, \
	SUM(TRIAL_RACE.hispanic_or_latino) AS Hispanic, \
    SUM(TRIAL_RACE.american_indian_or_alaska_native + \
        TRIAL_RACE.hawaiian_or_pacific_islander + \
        TRIAL_RACE.multiple + TRIAL_RACE.unknown) AS Other,\
	SUM(TRIAL_RACE.american_indian_or_alaska_native) AS AIAN, \
	SUM(TRIAL_RACE.hawaiian_or_pacific_islander) AS HPI, \
	SUM(TRIAL_RACE.multiple) AS multi_race, \
	SUM(TRIAL_RACE.unknown) AS unknown, \
	SUM(TRIAL_RACE.total) AS total \
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

    fig = by_drug(trt_trials, selected_trt, selected_cond)

    return fig


# Callback for updating the table underneath the stacked bar chart
    # https://community.plotly.com/t/display-tables-in-dash/4707/13
@app.callback(Output('table-by-treatment', 'children'), 
        Input(component_id="treatment-dropdown", component_property='value'),
        Input(component_id="conditions-dropdown", component_property='value'))
def update_table_by_treatment(selected_trt, selected_cond):
    query = "SELECT TRIAL_INTERVENTIONS.INTERVENTION, \
    TRIAL_CONDITIONS.condition, \
	SUM(TRIAL_RACE.asian) AS Asian, \
	SUM(TRIAL_RACE.black) AS Black, \
	SUM(TRIAL_RACE.white) AS White, \
	SUM(TRIAL_RACE.hispanic_or_latino) AS Hispanic, \
    SUM(TRIAL_RACE.american_indian_or_alaska_native + \
        TRIAL_RACE.hawaiian_or_pacific_islander + \
        TRIAL_RACE.multiple + TRIAL_RACE.unknown) AS Other,\
	SUM(TRIAL_RACE.american_indian_or_alaska_native) AS AIAN, \
	SUM(TRIAL_RACE.hawaiian_or_pacific_islander) AS HPI, \
	SUM(TRIAL_RACE.multiple) AS multi_race, \
	SUM(TRIAL_RACE.unknown) AS unknown, \
	SUM(TRIAL_RACE.total) AS total \
	FROM TRIAL_RACE INNER JOIN TRIAL_INTERVENTIONS \
	on TRIAL_RACE.nct_id = TRIAL_INTERVENTIONS.nct_id \
	INNER JOIN TRIAL_CONDITIONS \
	on TRIAL_RACE.nct_id = TRIAL_CONDITIONS.nct_id \
	WHERE TRIAL_INTERVENTIONS.intervention_name LIKE ? \
	AND TRIAL_CONDITIONS.CONDITION LIKE ? \
	GROUP BY TRIAL_INTERVENTIONS.intervention_name, TRIAL_CONDITIONS.condition"
    # query = "SELECT * FROM trials WHERE generic_name = ? AND condition = ?"

    trt_trials = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_trt, selected_cond))

    table_by_drug = summary_statistics_table(trt_trials, \
                                    selected_trt, selected_cond)

    title_first_part = 'Racial Diversity in Clinical Trials Conducted for '
    title_second_part = ' in '

    return generate_table(table_by_drug, 
            title = title_first_part + '{}'.format(selected_trt) + \
                title_second_part + '{}'.format(selected_cond))


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
    query = "SELECT TRIALS.lead_sponsor as Manufacturer, \
    YEAR(TRIAL_STATUS.start_date) as Year, \
	SUM(TRIAL_RACE.asian) AS Asian, \
	SUM(TRIAL_RACE.black) AS Black, \
	SUM(TRIAL_RACE.white) AS White, \
	SUM(TRIAL_RACE.hispanic_or_latino) AS Hispanic, \
    SUM(TRIAL_RACE.american_indian_or_alaska_native + \
        TRIAL_RACE.hawaiian_or_pacific_islander + \
        TRIAL_RACE.multiple + TRIAL_RACE.unknown) AS Other,\
	SUM(TRIAL_RACE.american_indian_or_alaska_native) AS AIAN, \
	SUM(TRIAL_RACE.hawaiian_or_pacific_islander) AS HPI, \
	SUM(TRIAL_RACE.multiple) AS multi_race, \
	SUM(TRIAL_RACE.unknown) AS unknown, \
	SUM(TRIAL_RACE.total) AS total \
	FROM TRIAL_RACE INNER JOIN TRIALS \
	on TRIAL_RACE.nct_id = TRIALS.nct_id \
    INNER JOIN TRIAL_STATUS \
	on TRIAL_RACE.nct_id = TRIALS.nct_id \
	WHERE TRIALS.lead_sponsor LIKE ? \
	GROUP BY TRIALS.lead_sponsor, YEAR(TRIAL_STATUS.start_date)"
    # query = "SELECT TRIAL_RACE.RACE FROM TRIAL_RACE \
    # INNER JOIN TRIALS \
    # on TRIAL_RACE.nct_id = TRIALS.nct_id \
    # WHERE TRIALS.lead_sponsor LIKE ? "
    manu_trials = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_manu,))

    fig = by_manufacturer(manu_trials)

    return fig


# Callback for updating the table underneath the line graph by manufacturer
    # https://community.plotly.com/t/display-tables-in-dash/4707/13
@app.callback(Output('table-by-manufacturer', 'children'), 
        Input(component_id="manufacturer-dropdown", component_property='value'))
def update_table_by_manufacturer(selected_manu):
    query = "SELECT TRIALS.lead_sponsor as Manufacturer, \
	SUM(TRIAL_RACE.asian) AS Asian, \
	SUM(TRIAL_RACE.black) AS Black, \
	SUM(TRIAL_RACE.white) AS White, \
	SUM(TRIAL_RACE.hispanic_or_latino) AS Hispanic, \
    SUM(TRIAL_RACE.american_indian_or_alaska_native + \
        TRIAL_RACE.hawaiian_or_pacific_islander + \
        TRIAL_RACE.multiple + TRIAL_RACE.unknown) AS Other,\
	SUM(TRIAL_RACE.american_indian_or_alaska_native) AS AIAN, \
	SUM(TRIAL_RACE.hawaiian_or_pacific_islander) AS HPI, \
	SUM(TRIAL_RACE.multiple) AS multi_race, \
	SUM(TRIAL_RACE.unknown) AS unknown, \
	SUM(TRIAL_RACE.total) AS total \
	FROM TRIAL_RACE INNER JOIN TRIALS \
	on TRIAL_RACE.nct_id = TRIALS.nct_id \
	WHERE TRIALS.lead_sponsor LIKE ? \
	GROUP BY TRIALS.lead_sponsor"
    # query = "SELECT * FROM trials WHERE manufacturer = ?"

    manu_trials = pd.read_sql_query(sql = query, 
                      con = connection,
                      params = (selected_manu,))
    
    table_by_manu = summary_statistics_manuf_table(manu_trials, selected_manu)

    title_first_part_manuf = 'Racial Diversity in Clinical Trials Conducted By Manufacturers for '

    return generate_table(table_by_manu, 
            title = title_first_part_manuf + '{}'.format(selected_manu))