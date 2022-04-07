from dash import dcc, html, Input, Output, callback

# ---------------------------------------------------------------------------------
# Data import and cleaning
    
myList = ['A', 'B']
myDict = {'A': [1,2,3],'B': [4,5,6] }
default_category = 'A'
default_index = 0

# ---------------------------------------------------------------------------------
# Layout of this tab

layout = html.Div([
    html.H3('Tab content 1'),
    dcc.Dropdown(id='first-dropdown',
                 options=[{'label':l, 'value':l} for l in myList],
                 value = default_category
    ),
    dcc.Dropdown(id='second-dropdown',
                 options=[{'label':l, 'value':l} for l in myDict[default_category]],
                 value = myDict[default_category][default_index]
    )
])

# ------------------------------------------------------------------------------
# Callbacks of this tab

@callback(
    [Output('second-dropdown', 'options'),
     Output('second-dropdown', 'value')],
    [Input('first-dropdown', 'value')])
def update_dropdown(value):
    return [[ {'label': i, 'value': i} for i in myDict[value] ], myDict[value][default_index]]