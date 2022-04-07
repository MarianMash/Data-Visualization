from multiprocessing.sharedctypes import Value
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash, dcc, html, Input, Output 

# stile for the app 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# ---------------------------------------------------------------------------------
# Data import and cleaning

file = pd.read_excel("Dataset_melted.xlsx")        

myList = ['A', 'B']
myDict = {'A': [1,2,3],'B': [4,5,6] }
default_category = 'A'
default_index = 0

# ------------------------------------------------------------------------------
# App layout

tab1 = html.Div([
    html.H3('Tab content 1'),
    dcc.Dropdown(id='first-dropdown',
                 options=[{'label':l, 'value':l} for l in myList],
                 value = default_category
    ),
    dcc.Dropdown(id='second-dropdown',
                 options=[{'label':l, 'value':l} for l in myDict[default_category]],
                 value = myDict[default_category][default_index]
    ),
    dcc.Slider(id='my_slider',
                min = 1990, 
                max = 2020, 
                step = 1, 
                value=1990,  
                marks = None,
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode='drag'),
    html.Div(id='output_container_slider'),
    
    html.Br(),

    dcc.Graph(id='my_bar_chart', figure={})
])

tab2 = html.Div([
    html.H3('Tab content 2'),
])    

app.layout = html.Div([
    html.H1("Global energy statistics - DV project", style={'text-align': 'center'}),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(id="tab-1", label='Tab One', value='tab-1-example'),
        dcc.Tab(id="tab-2", label='Tab Two', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example',
             children = tab1)
])

# ------------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components

@app.callback(Output('tabs-content-example', 'children'),
             [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab1
    elif tab == 'tab-2-example':
        return tab2

@app.callback(
    [Output('second-dropdown', 'options'),
     Output('second-dropdown', 'value')],
    [Input('first-dropdown', 'value')])
def update_dropdown(value):
    return [[ {'label': i, 'value': i} for i in myDict[value] ], myDict[value][default_index]]

@app.callback(
            [Output(component_id='output_container_slider', component_property='text'),
            Output(component_id='my_bar_chart', component_property='figure')],
            [Input(component_id='my_slider', component_property='value')])
def update_graph(value):
    #text with selected year
    container = 'You have selected "{}"'.format(value)

    dff = file.copy()
    dff = dff[dff["Year"]==value]
    dff = dff[["Country","Total energy production (Mtoe)","Year"]]
    #bar plot with values per country
    fig = px.bar(dff, x='Country', y="Total energy production (Mtoe)")

    return container, fig

#abcde
if __name__ == '__main__':
    app.run_server(debug=True)