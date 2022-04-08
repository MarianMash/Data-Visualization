from dash import dcc, html, Input, Output, callback
import pandas as pd

# ---------------------------------------------------------------------------------
# Data import
    
file = pd.read_csv("ActualDataset.csv")

# ---------------------------------------------------------------------------------
# Layout of this tab

layout = html.Div([
    html.H3('Tab content x'),
    #
    #  INSIDE THIS div YOU PUT THE LAYOUT OF THIS TAB
    #
])

# ------------------------------------------------------------------------------
# Callbacks of this tab

@callback(
    [Output(component_id='my_bar_chart', component_property='figure')],
    [Input(component_id='my_slider', component_property='value')]
)
def function(value):
    ##Some function
    some_output=value
    ######
    return some_output
