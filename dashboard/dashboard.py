import pandas as pd
import sqlite3
import re
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html, dcc, dash_table, State, callback
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import json
import numpy as np
import pathlib

# from .clean_and_analyze import analyze_data
from .visualization import visualization

# Read in data: connect to the SQL database
connection = sqlite3.connect("data/trials.db")
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

# Define lists of possible treatments and of possible manufacturers
trt_list = pd.read_sql_query("SELECT DISTINCT treatment FROM trials", connection)
# trt_list = []
# for i in data['generic_name']:
#         trt_list.append(i)

manu_list = pd.read_sql_query("SELECT DISTINCT manufacturer FROM trials", connection)
# manu_list = []
# for i in data['manufacturer']:
#         manu_list.append(i)

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

#App
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

# Header
header_and_intro = html.Div([html.H1(children='Racial and Ethnicity Representation in Clinical Trials',
                                style={'textAlign': 'center','color': colors['text']}),
                        html.Div(children='''Placeholder ''',
                                style={'textAlign': 'left','color': colors['text'],'width' : '100%','padding' :5})])

# By treatment section
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
                        # TODO: figure out how to get a dropdown of the conditions for the treatment selected above
                        #  html.H3(id = 'conditions'),
                        # dcc.Dropdown(id='condition-dropdown', options=conditions, 
                        #     placeholder="Select a condition the treatment is used for", style={'width': '100%'}),
                        html.Br(),
                        dcc.Graph(id='stacked-bar', style={'width': '100%'})],
                        # TODO: figure out best way to get the table of stats from visualization.py displayed here
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

# Callback function for searching treatments
@app.callback(
        Output(component_id = 'treatment-dropdown', component_property ='options'),
        Input(component_id="treatment-dropdown", component_property='search-value')
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
    generic_name = selected_trt
    
    return "Generic name: {}".format(generic_name)

# Callback function for printing the brand name
@app.callback(
        Output(component_id = 'brand-name', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_brand(selected_trt):
    query = "SELECT distinct brand_name FROM trials WHERE generic_name = ?"
    brand_name = connection.execute(query, (selected_trt))
    #row = data.loc[data['generic_name'] == selected_trt]
    #brand_name = row['brand_name']
    
    return "Brand name: {}".format(brand_name)

# Callback function for printing the manufacturer name
@app.callback(
        Output(component_id = 'manufacturer', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_manufacturer(selected_trt):
    query = "SELECT distinct manufacturer FROM trials WHERE generic_name = ?"
    manufacturer = connection.execute(query, (selected_trt))
    # row = data.loc[data['generic_name'] == selected_trt]
    # manufacturer = row['manufacturer']

    return "Manufacturer: {}".format(manufacturer)

# Callback function for pulling list of conditions for the treatment
@app.callback(
        Output(component_id = 'brand-name', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_conditions(selected_trt):
    query = "SELECT distinct conditions FROM trials WHERE generic_name = ?"
    conditions = connection.execute(query, (selected_trt))

    return conditions

# Callback function for updating the stacked bar chart
@app.callback(
        Output(component_id='stacked-bar', component_property='figure'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_stackedbar(selected_trt):
    query = "SELECT * FROM trials WHERE generic_name = ?"
    trt_trials = connection.execute(query, (selected_trt))

    fig = by_drug(trt_trials)

    return fig

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
    query = "SELECT * FROM trials WHERE manufacturer = ?"
    manu_trials = connection.execute(query, (selected_manu))

    fig = by_manufacturer(manu_trials)

    return fig

