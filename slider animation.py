import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from math import log

from dash import Dash, dcc, html, Input, Output 

app = Dash(__name__)

import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies
from dash.dependencies import Input, Output



app.layout = html.Div([
    html.Div([
        html.Div([
            html.Button(id='buttonPlay', children='Play'),
            html.Button(id='buttonPause', children='Pause'),
            html.Button(id='buttonReset', children='Reset'),
            dcc.Interval(id='interval-component',
                        interval=1500, # in milliseconds
                        n_intervals=0)
        ], style={'width': '15%', 'display': 'inline-block'}),
        html.Div([
        dcc.Slider(
            id = "steper",
            min=1990,
            max=2020,
            step = 1,
            marks={
                1990: '1990',
                1995: '1995',
                2000: '2000',
                2005: '2005',
                2010: '2010',
                2015: '2015',
                2020: '2020'},
            value=1990,
            included = False,
            tooltip={"placement": "bottom", "always_visible": True},
            #updatemode='drag'
            ),
        ], style={'width': '75%', 'display': 'inline-block'}),
        html.Br(),
        html.Br(),
        html.Div(id='msg-container'),
    ], className = 'row'),
    
])



@app.callback([
    Output(component_id='interval-component', component_property='disabled'),
    Output(component_id='buttonPlay', component_property='n_clicks'), 
    Output(component_id='buttonPause', component_property='n_clicks'),
    Output(component_id='msg-container', component_property='children')],
    [Input(component_id='buttonPlay', component_property='n_clicks'),
    Input(component_id='buttonPause', component_property='n_clicks'),
    Input(component_id='buttonReset', component_property='n_clicks'),
    Input('steper', 'value'),
    Input('steper', 'drag_value')]
)
def enable_interval_update(buttonPlay, buttonPause, buttonReset, stepper, dragValue):
    msg = 'play: {}, pause: {}, reset: {}, stepper: {}, drag: {}'.format(buttonPlay, buttonPause, buttonReset, stepper, dragValue)
    if not buttonPlay:
        buttonPlay = 0
    if not buttonPause:
        buttonPause = 0

    if buttonPlay > buttonPause:
        return False, 1, 0, msg 
    
    else:
        return True, 0, 0, msg


@app.callback(
    [Output('steper', 'value'),
    Output(component_id='buttonReset', component_property='n_clicks'),
    Output('interval-component', 'n_intervals')
    ], 
    [Input('interval-component', 'n_intervals'), 
    Input(component_id='buttonReset', component_property='n_clicks'),
    Input('steper', 'drag_value')])
def on_click(n_intervals, buttonReset, dragValue):
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


if __name__ == '__main__':
    app.run_server(debug=True)