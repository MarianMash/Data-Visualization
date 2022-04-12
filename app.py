from pydoc import classname
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import tab_1, tab_2, tab_3, tab_4

# ---------------------------------------------------------------------------------
# Stile for the app 
# external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/minty/bootstrap.min.css']

# app = Dash(__name__, external_stylesheets=external_stylesheets)

#dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = Dash(__name__)#, external_stylesheets=[dbc.themes.SOLAR])

#to make automatic settings for mobile (to be put into app =...):
# meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]

# ---------------------------------------------------------------------------------
# Layout

tab1 = tab_1.layout

tab2 = tab_2.layout

tab3 = tab_3.layout

tab4 = tab_4.layout

app.layout = html.Div([
    html.H1("Global energy statistics - DV project", className="m-3 text-xl-center text-light"),
    html.H3("Analysis of countries energy indicators", className="m-3 text-xl-center"),
    # dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
    #     dcc.Tab(id="tab-1", label='Tab One', value='tab-1-example'),
    #     dcc.Tab(id="tab-2", label='Tab Two', value='tab-2-example'),
    #     dcc.Tab(id="tab-3", label='Tab Three', value='tab-3-example'),
    #     dcc.Tab(id="tab-4", label='Tab Four', value='tab-4-example')
    # ]),
    dbc.Tabs(
            [
                dbc.Tab(tab_id='tab-1-example', label="Total Energy"),
                dbc.Tab(tab_id='tab-2-example', label="Tab Two"),
                dbc.Tab(tab_id='tab-3-example', label="Tab Three"),
                dbc.Tab(tab_id='tab-4-example', label="Tab Four")
            ],
            id="tabs-example",
            active_tab="tab-1-example",
            className="m-3 nav nav-pills nav-fill"
        ),
    html.Div(id='tabs-content-example',
             children = tab1)
])

# app.css.append_css({
#     "external_url:https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/minty/bootstrap.min.css"
# })

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

# ---------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)