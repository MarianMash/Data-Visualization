from pydoc import classname
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import tab_1, tab_2, tab_3, tab_4

# ---------------------------------------------------------------------------------

# suppress callback exceptions which are a result of the tab layout 
app = Dash(__name__, suppress_callback_exceptions=True)

#to make automatic settings for mobile (to be put into app =...):
# meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]

# ---------------------------------------------------------------------------------
# Layout

tab1 = tab_1.layout

tab2 = tab_2.layout

tab3 = tab_3.layout

tab4 = tab_4.layout

app.layout = html.Div([
    html.H1("Global energy statistics", className="m-3 text-xl-center text-light"),
    html.H3("Analysis of countries' energy indicators", className="m-3 text-xl-center"),
    dbc.Tabs(
            [
                dbc.Tab(tab_id='tab-1-example', label="Total energy overview"),
                dbc.Tab(tab_id='tab-2-example', label="Total energy comparison"),
                dbc.Tab(tab_id='tab-3-example', label="Electricity overview"),
                dbc.Tab(tab_id='tab-4-example', label="Renewables")
            ],
            id="tabs-example",
            active_tab="tab-1-example",
            className="m-3 nav nav-pills nav-fill"
        ),
    html.Div(id='tabs-content-example',
             children = tab1)
])

# ------------------------------------------------------------------------------
# Callback linking tabs layout to each tab
@app.callback(Output('tabs-content-example', 'children'),
             [Input('tabs-example', 'active_tab')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab1
    elif tab == 'tab-2-example':
        return tab2
    elif tab == 'tab-3-example':
        return tab3
    elif tab == 'tab-4-example':
        return tab4

# ---------------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run_server(debug=True)