import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output
import json
import numpy as np
from dash import html, dcc
import pathlib

# from .clean_and_analyze import analyze_data
from .visualization import stacked_bar, line_graph

# Read in data
data = pathlib.Path(__file__).parent / "../cleaned_data/data.csv"

data =  pd.read_csv(data)

# Define lists of possible treatments and of possible manufacturers
trt_list = []
for i in data['generic_name']:
        trt_list.append(i)

manu_list = []
for i in data['manufacturer']:
        manu_list.append(i)

colors = {
    'background': '#FDFEFE',
    'text': '#17202A'
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
by_treatment = html.Div([html.H2(children='Search by treatment',
                                      style={'textAlign': 'center','color': colors['text']}),
                            html.Div(children='''Placeholder''',
                                     style={'textAlign': 'left','color': colors['text'],'width':'100%','padding' :10}),
                            html.Br(),
                            html.Div(children='''Choose the treatment of interest'''),
                        dcc.Dropdown(id='treatment-dropdown', options=trt_list, value = "adalimumab", style={'width': '100%'}),
                        html.H3(id = 'generic_name',style={'textAlign': 'left','color': '#3CB371'}),
                        html.H3(id = 'brand_name',style={'textAlign': 'left','color': '#3CB371'}),
                        html.H3(id = 'manufacturer',style={'textAlign': 'left','color': '#3CB371'}),
                        html.Br(),
                        dcc.Graph(id='stacked-bar', style={'width': '100%'})],
                            className = 'five columns')

# By manufacturer section
by_manufacturer = html.Div([html.H2(children='Search by manufacturer',
                                 style={'textAlign': 'center','color': colors['text']}),
                            html.Div(children='''Placeholder''',
                                     style={'textAlign': 'left','color': colors['text'],'width':'100%','padding' :10}),
                            html.Br(),
                            html.Div(children='''Choose the manufacturer of interest'''),
                        dcc.Dropdown(id='manufacturer-dropdown', options=manu_list, value = "AbbVie", style={'width': '100%'}),
                        html.Br(),
                        dcc.Graph(id='line-graph', style={'width': '100%'})],
                       className = 'five columns')

# Define app layout
app.layout = html.Div(children=[
    html.Div(header_and_intro, style={"grid-area":"header"}),
    html.Div(by_treatment, style={"grid-area":"graph_1"}),
    html.Div(by_manufacturer, style={"grid-area":"graph_2"})],
                      style={
                          'backgroundColor': '#FFFFFF',
                          'display': 'grid',
                          'grid-template-areas': """
                          'header header'
                          'graph_1 graph_2'
                          """,
                          'grid-gap': '10px',
                          'grid-template-columns': 'minmax(300px, 1000px) minmax(300px, 1000px)',
                          'grid-template-rows': 'auto 1fr 1fr'
                      })

@app.callback(
        Output(component_id = 'generic-name', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_generic(selected_trt):
    row = data.loc[data['generic_name'] == selected_trt]
    generic_name = row['generic_name']
    
    return "Generic name: {}".format(generic_name)

@app.callback(
        Output(component_id = 'brand-name', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_brand(selected_trt):
    row = data.loc[data['generic_name'] == selected_trt]
    brand_name = row['brand_name']
    
    return "Brand name: {}".format(brand_name)

@app.callback(
        Output(component_id = 'manufacturer', component_property ='children'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_output_manufacturer(selected_trt):
    row = data.loc[data['generic_name'] == selected_trt]
    manufacturer = row['manufacturer']

    return "Manufacturer: {}".format(manufacturer)

@app.callback(
        Output(component_id='stacked-bar', component_property='figure'),
        Input(component_id="treatment-dropdown", component_property='value')
        )

def update_stackedbar(selected_trt):
    row = data.loc[data['generic_name'] == selected_trt]

    fig = stacked_bar(row)

    return fig


@app.callback(
        Output(component_id='line-graph', component_property='figure'),
        Input(component_id="manufacturer-dropdown", component_property='value')
        )

def update_linegraph(selected_manu):
    row = data.loc[data['manufacturer'] == selected_manu]

    fig = line_graph(row)

    return fig

