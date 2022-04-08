import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)


from dash import Dash, dcc, html, Input, Output, callback

app = Dash(__name__)
# ---------------------------------------------------------------------------------
# Data import and cleaning
file = pd.read_csv("ActualDataset.csv")


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("First Test for DV", style={'text-align': 'center'}),

    html.P("Select range of histogram:",
            className="control_label"),

    dcc.RangeSlider(id="year_slider",
                    min=1990,
                    max=2020,
                    value=[2005, 2006],
                    step = 1,
                    className="dcc_control",
                    marks = None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode='drag'),
    #html.Div(id='output_container_slider'),

    html.Br(),

    dcc.Graph(id='bar_chart'),
    
    html.Br(),
    ])

# ------------------------------------------------------------------------------
# Connect Dash-Components to Data

@callback(
            Output(component_id='bar_chart', component_property='figure'),
            [Input(component_id='year_slider', component_property='value')])


def update_graph(value):
    #text with selected year
    #container = 'You have selected "{}"'.format(value)

    dff = file.copy()
    dff = dff[(dff['Year'] >= value[0]) & (dff['Year'] <= value[1])]
    dff = dff[["Country","Share of renewables in electricity production (%)","Year"]]
    #bar plot with values per country
    fig = px.bar(dff, x='Year', y="Share of renewables in electricity production (%)")

    #return container, fig
    return fig


#----------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)