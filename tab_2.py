import pandas as pd
from numpy import argmax
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from math import log
import operator
import dash_bootstrap_components as dbc
import plotly.io as pio


from dash import Dash, dcc, html, Input, Output, callback

# ---------------------------------------------------------------------------------
# Data import and cleaning

file = pd.read_csv("Datasets/Merged_Energy_Dataset.csv")

# country list for dropdown 
countryListComparison = []
for country in file['Country'].unique():
    countryListComparison.append({'label':str(country),'value':country})

# ---------------------------------------------------------------------------------
# Layout of this tab

layout = html.Div([
    #Title 
    dbc.Row(
        [
            html.Div(html.H3("Comparison of total energy production and consumption"), className="m-3 text-lg-center text-light"),
            dbc.Col([
                html.Div(html.P("The total energy production and consumption are shown in a dispersion graph to compare the level of these two indices over the years for each country or alternatively for the selected ones. It is possible to compare them on different axes scales and to set the size of the points proportional to the country's GDP, population or area. Besides it a more detailed analysis is presented selected countries"), className="m-3 text-lg text-light")
            ],width={'size':8, 'offset':2})
        ]
    ),
    #Buttons - slider - dropdown
    dbc.Row(
        [
            dbc.Col([
                    
                    html.Button(id='buttonPlayComparison', children='Play', className="m-1 btn btn-success"),
                    html.Button(id='buttonPauseComparison', children='Pause', className="m-1 btn btn-success"),
                    html.Button(id='buttonResetComparison', children='Reset', className="m-1 btn btn-success")
            ], width=3),
            dbc.Col([
                    dcc.Interval(id='intervalComponentComparison', interval=1500, n_intervals=0),
                    dcc.Slider(id='sliderComparison', min = 1990, max = 2020, step = 1, value=1990, 
                    marks = {1990: '1990', 1995: '1995', 2000: '2000', 2005: '2005', 2010: '2010', 2015: '2015', 2020: '2020'},
                    tooltip={"placement": "bottom", "always_visible": True})
            ],width=6),
            dbc.Col([
                    dcc.Dropdown(
                    id='drop1',
                    options=countryListComparison,
                    value=['Portugal', 'Spain'], 
                    multi = True)
            ],width=3)
        ]
    ),

    dbc.Row(
        [
            dbc.Col([
                    html.Button(id='buttonShowSelectedOnly', children='Show Selected Only', n_clicks_timestamp=0, className="m-2 btn btn-light"),
                    html.Button(id='buttonDefault', children='Default', n_clicks_timestamp=0, className="m-1 btn btn-light"),
                    html.Button(id='buttonGDP', children='GDP', n_clicks_timestamp=0, className="m-1 btn btn-light"),
                    html.Button(id='buttonPopulation', children='Population', n_clicks_timestamp=0, className="m-1 btn btn-light"),
                    #html.Button(id='buttonArea', children='Area', n_clicks_timestamp=0, className="m-1 btn btn-light")
            ], width=5),
            dbc.Col([
                    dcc.RadioItems(
                    ['Linear X axis', 'Log X axis'],
                    'Linear X axis',
                    id='xaxis_type',
                    inline=True, 
                    style = {'display': 'inline-block', "margin-left": "40px", "verticalAlign": "middle"}
                    ),
                    
                
                    dcc.RadioItems(
                        ['Linear Y axis', 'Log Y axis'],
                        'Linear Y axis',
                        id='yaxis_type',
                        inline=True,
                        style = {'display': 'inline-block', "margin-left": "20px", "verticalAlign": "middle"}
                    )
            ],width=5, className="m-3")
        ]
    ),

    #Scatterplot and bar chart
    dbc.Row(
        [
            dbc.Col(dbc.Card([dbc.CardHeader("Scatterplot of total energy production and consumption of countries "),
                            html.Br(className="mb-6"),
                            dcc.Graph(id='electricity_graph'),
                            html.Br(className="mb-6")],
                            color="secondary", inverse=True),width=8),
            dbc.Col(dbc.Card([dbc.CardHeader("Production and consumption for selected countries"),
                            html.Br(className="mb-6"),
                            dcc.Graph(id='electricity_bar'),
                            html.Br(className="mb-6")],
                            color="secondary", inverse=True),width=4),
        ]
    ),
], className="m-3")

# ---------------------------------------- CALLBACKS --------------------------------------##

@callback([
    Output(component_id='intervalComponentComparison', component_property='disabled'),
    Output(component_id='buttonPlayComparison', component_property='n_clicks'), 
    Output(component_id='buttonPauseComparison', component_property='n_clicks')],
    [Input(component_id='buttonPlayComparison', component_property='n_clicks'),
    Input(component_id='buttonPauseComparison', component_property='n_clicks'),
    Input(component_id='buttonResetComparison', component_property='n_clicks'),
    Input('sliderComparison', 'value'),
    Input('sliderComparison', 'drag_value')])
def enable_interval_update_comparison(buttonPlay, buttonPause, buttonReset, stepper, dragValue):
    if not buttonPlay:
        buttonPlay = 0
    if not buttonPause:
        buttonPause = 0
    if buttonPlay > buttonPause:
        return False, 1, 0
    else:
        return True, 0, 0

@callback(
    [Output('sliderComparison', 'value'),
    Output(component_id='buttonResetComparison', component_property='n_clicks'),
    Output('intervalComponentComparison', 'n_intervals')], 
    [Input('intervalComponentComparison', 'n_intervals'), 
    Input(component_id='buttonResetComparison', component_property='n_clicks'),
    Input('sliderComparison', 'drag_value')])
def on_click_comparison(n_intervals, buttonReset, dragValue):
    if buttonReset is None:
        buttonReset = 0
    if n_intervals is None:
        return 0
    if dragValue is None:
        dragValue = 1990
    
    if buttonReset > 0:
        return 1990, 0, 0 
    
    if int(dragValue) - 1989 != n_intervals:
        n_intervals = int(dragValue) -1990

    return 1990 + (n_intervals)%30, 0, n_intervals

@callback(
    [Output('electricity_graph', 'figure'),
    Output('electricity_bar', 'figure')],
    [Input('sliderComparison', 'value'), 
    Input('drop1', 'value'),
    Input('xaxis_type', 'value'),
    Input('yaxis_type', 'value'),
    Input('buttonShowSelectedOnly', 'n_clicks'),
    Input('buttonDefault', 'n_clicks_timestamp'),
    Input('buttonGDP', 'n_clicks_timestamp'),
    Input('buttonPopulation', 'n_clicks_timestamp'),])

def update_comparison_graph(slider_value, drop1_value, xaxis_type, yaxis_type, btnSelected, btnDefault, btnGDP, btnPopulation):
    file['default_size'] = 1
    file['area'] = 1
    file['scatterColor'] = 'default'
    
    # select year  
    if btnSelected is None: 
        btnSelected = 0
    
    # select underlying data based on the value of button 'show selected only'
    dff = file.loc[file['Year'] == slider_value]
    if btnSelected % 2 == 1: 
        dff = file.loc[(file['Country'].isin(drop1_value)) & (file['Year'] == slider_value)]
        

    # select marker size column based on inputs from the buttons
    timestampsDict = {
        'default_size': btnDefault, 
        'gdp_md_est': btnGDP, 
        'pop_est': btnPopulation
    }
    sizePicker = max(timestampsDict.items(), key=operator.itemgetter(1))[0]

    # create custom scatter color for selected countries 
    for dropSelection in drop1_value:
        if dff.shape[0] == 0:
            break
        i = dff.loc[dff['Country']==dropSelection].index.values[0]
        dff.loc[i, 'scatterColor'] = dropSelection

    fig = px.scatter(data_frame=dff, 
                    x = "Total production of Energy (Twh)",
                    y = "Total consumption of Energy (Twh)",
                    size = sizePicker, 
                    hover_name = 'Country', 
                    color = 'scatterColor', 
                    category_orders={'scatterColor': [dropSelection for dropSelection in drop1_value]},
                    template="plotly_dark")
    if sizePicker == 'default_size':
        fig.update_traces(marker={'size': 10})
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    fig.update_xaxes(title = 'Total energy production',
                     type='linear' if xaxis_type == 'Linear X axis' else 'log')
    fig.update_yaxes(title = 'Total energy consumption',
                     type='linear' if yaxis_type == 'Linear Y axis' else 'log')

    # ----------------- BARPLOT -----------------
    barNames = ['Production', 'Consumption']
    dataHolder = []
    for dropSelection in drop1_value:
        selectedCountryX = float(dff.loc[dff['Country'] == dropSelection]["Total production of Energy (Twh)"])
        selectedCountryY = float(dff.loc[dff['Country'] == dropSelection]["Total consumption of Energy (Twh)"])
        
        barValues = []
        if xaxis_type == 'Linear':
            barValues.append(selectedCountryX)
        else:
            barValues.append(log(selectedCountryX))

        if yaxis_type == 'Linear':
            barValues.append(selectedCountryY)
        else:
            barValues.append(log(selectedCountryY))

        dataHolder.append(
            go.Bar(
                name = dropSelection,
                x = barNames,
                y = barValues
            )
        )

    figBar = go.Figure(data=dataHolder)
    figBar.update_layout(template = "plotly_dark", yaxis=dict(title="Twh"))

    for trace in figBar['data']:
        trace['showlegend'] = False
    
    return fig, figBar
