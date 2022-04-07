from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)

# ---------------------------------------------------------------------------------
# Data import and cleaning
file = pd.read_csv("ActualDataset.csv")


# ---------------------------------------------------------------------------------
# Layout of this tab

layout = html.Div([
    html.H3('Tab content 2'),
    
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


# ------------------------------------------------------------------------------
# Callbacks of this tab

@callback(
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