import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go


from dash import Dash, dcc, html, Input, Output 

app = Dash(__name__)
# ---------------------------------------------------------------------------------
# Data cleaning

df = pd.read_excel('Dataset_melted.xlsx')

#-------------------------------------------------------------------------------------
# Building the graphs 

# GRAPH 1 - ELECTRICITY
country_list = ['Portugal', 'Romania', 'Spain', 'Sweden', 'United Kingdom']

options1 = [{'label': 'Portugal', 'value': 'Portugal'},
           {'label': 'Romania', 'value': 'Romania'},
           {'label': 'Spain', 'value': 'Spain'}, 
           {'label': 'Sweden', 'value': 'Sweden'}, 
           {'label': 'United Kingdom', 'value': 'United Kingdom'}]

# GRAPH 2 - 

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    # PAGE TITLE
    html.H1("First Test for DV", style={'text-align': 'center'}),

    dcc.Slider(id='my_slider',
                min = 1990, 
                max = 2020, 
                step = 1, 
                value=1990,  
                marks = None,
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode='drag'),
    html.Br(),
    dcc.Dropdown(
        id='drop1',
        options=options1,
        value='Portugal'
    ),

    #html.Br(),

    html.Div(id='output_container_slider_dropdown'),

    ])

# --------------------------------------------------------------------------------------------------------------------------
# Connect Dash-Components to Data
@app.callback(
    Output('output_container_slider_dropdown', 'children'),
    [Input('my_slider', 'value'), 
    Input(component_id='drop1', component_property='value')])
def update_output(my_slider, drop1):
    return 'You have selected {} and {}'.format(my_slider, drop1)



if __name__ == '__main__':
    app.run_server(debug=True)