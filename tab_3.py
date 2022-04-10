import pandas as pd
from numpy import argmax
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from math import log
import operator

from dash import Dash, dcc, html, Input, Output, callback

# ---------------------------------------------------------------------------------
# Data import and cleaning
country_list = ['Portugal', 'Romania', 'Spain', 'Sweden', 'United Kingdom']

options1 = [{'label': 'Portugal', 'value': 'Portugal'},
           {'label': 'Romania', 'value': 'Romania'},
           {'label': 'Spain', 'value': 'Spain'}, 
           {'label': 'Sweden', 'value': 'Sweden'}, 
           {'label': 'United Kingdom', 'value': 'United Kingdom'}]

file = pd.read_csv("ActualDataset.csv")


# ---------------------------------------------------------------------------------
# Layout of this tab

layout = html.Div([
    # GRAPH 1
    html.Div(children = [
        html.H3('Choose a year baby:'),
        dcc.Slider(id='comparison_slider',
                    min = 1990, 
                    max = 2020, 
                    step = 1, 
                    value=1990,  
                    marks = None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode='drag'), 
        html.Br(),
        dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='xaxis_type',
                inline=True
            ),
    ], style={'width': '48%', 'display': 'inline-block'}),
    #),
    html.Div(children = [
        html.Label('Choose a Country:'),
        dcc.Dropdown(
            id='drop1',
            options=options1,
            value='Portugal'),
        html.Br(),
        dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='yaxis_type',
                inline=False
            ),
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    #),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
            html.Button(id='buttonDefault', children='Default', n_clicks_timestamp=0),
            html.Button(id='buttonGDP', children='GDP', n_clicks_timestamp=0),
            html.Button(id='buttonPopulation', children='Population', n_clicks_timestamp=0),
            html.Button(id='buttonArea', children='Area', n_clicks_timestamp=0),
            html.Div(id='recentButtonContainer')
    ]),
    html.Br(),
    html.Div([
        dcc.Graph(id='electricity_graph', style={'display': 'inline-block'}),
        dcc.Graph(id='electricity_bar', style={'display': 'inline-block'}),
    ], className = 'row'),
    html.Br(),
    
    html.Br()

])

# ------------------------------------------------------------------------------
# Callbacks of this tab

@callback(Output('recentButtonContainer', 'children'),
        [Input('buttonDefault', 'n_clicks_timestamp'),
        Input('buttonGDP', 'n_clicks_timestamp'),
        Input('buttonPopulation', 'n_clicks_timestamp'),
        Input('buttonArea', 'n_clicks_timestamp')])
def display(btnDefault, btnGDP, btnPopulation, btnArea):
    timestamps = [btnDefault, btnGDP, btnPopulation, btnArea]
    return 'button {} was most recently pressed'.format(argmax(timestamps))

@callback(
    [Output('electricity_graph', 'figure'),
    Output('electricity_bar', 'figure')],
    [Input('comparison_slider', 'value'), 
    Input('drop1', 'value'),
    Input('xaxis_type', 'value'),
    Input('yaxis_type', 'value'),
    Input('buttonDefault', 'n_clicks_timestamp'),
    Input('buttonGDP', 'n_clicks_timestamp'),
    Input('buttonPopulation', 'n_clicks_timestamp'),
    Input('buttonArea', 'n_clicks_timestamp')])

def update_comparison_graph(slider_value, drop1_value, xaxis_type, yaxis_type, btnDefault, btnGDP, btnPopulation, btnArea):
    # add default marker size column 
    file['default_size'] = 0.3
    
    # select year  
    dff = file[file['Year'] == slider_value]
    
    # save values of the selected country
    selectedCountryX = float(dff[dff['Country'] == drop1_value]['Total energy production (Mtoe)'])
    selectedCountryY = float(dff[dff['Country'] == drop1_value]['Total energy consumption (Mtoe)'])

    # select marker size column based on imputs from the buttons
    timestampsDict = {
        'default_size': btnDefault, 
        'gdp_md_est': btnGDP, 
        'pop_est': btnPopulation,
        'default_size': btnArea
    }
    sizePicker = max(timestampsDict.items(), key=operator.itemgetter(1))[0]
    sizeSeries = dff[sizePicker] * 2

    fig = px.scatter(data_frame=dff, 
                    x = 'Total energy production (Mtoe)',
                    y = 'Total energy consumption (Mtoe)',
                    size = sizeSeries, 
                    hover_name = 'Country')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title = 'Total energy production',
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title = 'Total energy consumption',
                     type='linear' if yaxis_type == 'Linear' else 'log')

    fig.add_trace(go.Scatter(x = dff[dff['Country'] == drop1_value]['Total energy production (Mtoe)'], 
                        y = dff[dff['Country'] == drop1_value]['Total energy consumption (Mtoe)'], 
                        mode = 'markers',
                        marker_symbol = 'star',
                        marker_size = 15, 
                        showlegend = False))

    barNames = ['Production', 'Consumption']
    barValues = []
    if xaxis_type == 'Linear':
        barValues.append(selectedCountryX)
    else:
        barValues.append(log(selectedCountryX))

    if yaxis_type == 'Linear':
        barValues.append(selectedCountryY)
    else:
        barValues.append(log(selectedCountryY))
    
    data = [go.Bar(
    x = barNames,
    y = barValues
    )]

    figBar = go.Figure(data=data)

    return fig, figBar
