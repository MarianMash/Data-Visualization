from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd

import tab_1, tab_2, tab_3, tab_4

# ---------------------------------------------------------------------------------
# Stile for the app 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# ---------------------------------------------------------------------------------
# Layout

tab1 = tab_1.layout

tab2 = tab_2.layout

tab3 = tab_3.layout

tab4 = tab_4.layout

app.layout = html.Div([
    html.H1("Global energy statistics - DV project", style={'text-align': 'center'}),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(id="tab-1", label='Tab One', value='tab-1-example'),
        dcc.Tab(id="tab-2", label='Tab Two', value='tab-2-example'),
        dcc.Tab(id="tab-3", label='Tab Three', value='tab-3-example'),
        dcc.Tab(id="tab-4", label='Tab Four', value='tab-4-example')
    ]),
    html.Div(id='tabs-content-example',
             children = tab1)
])

# ------------------------------------------------------------------------------
# Callback linking tabs layout to each tab
@app.callback(Output('tabs-content-example', 'children'),
             [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab1
    elif tab == 'tab-2-example':
        return tab2
    elif tab == 'tab-3-example':
        return tab3
    elif tab == 'tab-4-example':
        return tab4

# ---------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)