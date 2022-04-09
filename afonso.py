import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go


from dash import Dash, dcc, html, Input, Output, callback

app = Dash(__name__)
# ---------------------------------------------------------------------------------
# Data import and cleaning
file = pd.read_csv("ActualDataset.csv")

countries = []
for country in file['Country'].unique():
    countries.append({'label':str(country),'value':country})



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

    dcc.Graph(id='bar_chart_2'),

    html.Br(),

    dcc.Slider(id='slider',
                min = 1990, 
                max = 2020, 
                step = 1, 
                value=1990,  
                marks = None,
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode='drag',
                ),
    html.Br(),

    dcc.Dropdown(
        options= countries,
        value='Portugal',
        id='country_dropdown',
        style={"width": "50%"}
        ),

    html.Br(),

    dcc.Graph(id='circle_graph')
    ])

# ------------------------------------------------------------------------------
# Connect Dash-Components to Data

@callback(
            [Output(component_id='bar_chart', component_property='figure'),
            Output(component_id='bar_chart_2', component_property='figure')],
            [Input(component_id='year_slider', component_property='value')])


def update_bar_graph(value):
    #text with selected year
    #container = 'You have selected "{}"'.format(value)


    #bar plot 1 with renewables values per continent
    dff = file.copy()
    dff = dff[(dff['Year'] >= value[0]) & (dff['Year'] <= value[1])]
    dff = dff[['Share of renewables in electricity production (%)', 'continent', 'Year']]

    fig1 = go.Figure(
        data=[
            go.Bar(
                name="Europe",
                x= dff.Year.unique(),
                y= dff.loc[file['continent'] == 'Europe'].groupby('Year')['Share of renewables in electricity production (%)'].mean(),
                marker_color="#004687",
                opacity=0.8,
            ),
            go.Bar(
                name="Asia",
                x= dff.Year.unique(),
                y=dff.loc[file['continent'] == 'Asia'].groupby('Year')['Share of renewables in electricity production (%)'].mean(),
                marker_color="#AE8F6F",
                opacity=0.8,
            ),
            go.Bar(
                name="Oceania",
                x= dff.Year.unique(),
                y= dff.loc[file['continent'] == 'Oceania'].groupby('Year')['Share of renewables in electricity production (%)'].mean(),
                marker_color="#FF9912",
                opacity=0.8,
            ),
            go.Bar(
                name="Africa",
                x= dff.Year.unique(),
                y= dff.loc[file['continent'] == 'Africa'].groupby('Year')['Share of renewables in electricity production (%)'].mean(),
                marker_color="#4D4D4D",
                opacity=0.8,
            ),
            go.Bar(
                name="North America",
                x= dff.Year.unique(),
                y= dff.loc[file['continent'] == 'North America'].groupby('Year')['Share of renewables in electricity production (%)'].mean(),
                marker_color="#EE2C2C",
                opacity=0.8
            )
        ]
    )
    #bar plot 2 with total consumption values per continent
    dff1 = file.copy()
    dff1 = dff1[(dff['Year'] >= value[0]) & (dff1['Year'] <= value[1])]
    dff1 = dff1[['Total energy consumption (Mtoe)', 'continent', 'Year']]

    fig2 = go.Figure(
            data=[
                go.Bar(
                    name="Europe",
                    x= dff1.Year.unique(),
                    y= dff1.loc[file['continent'] == 'Europe'].groupby('Year')['Total energy consumption (Mtoe)'].mean(),
                    marker_color="#004687",
                    opacity=0.8,
                ),
                go.Bar(
                    name="Asia",
                    x= dff1.Year.unique(),
                    y=dff1.loc[file['continent'] == 'Asia'].groupby('Year')['Total energy consumption (Mtoe)'].mean(),
                    marker_color="#AE8F6F",
                    opacity=0.8,
                ),
                go.Bar(
                    name="Oceania",
                    x= dff1.Year.unique(),
                    y= dff1.loc[file['continent'] == 'Oceania'].groupby('Year')['Total energy consumption (Mtoe)'].mean(),
                    marker_color="#FF9912",
                    opacity=0.8,
                ),
                go.Bar(
                    name="Africa",
                    x= dff1.Year.unique(),
                    y= dff1.loc[file['continent'] == 'Africa'].groupby('Year')['Total energy consumption (Mtoe)'].mean(),
                    marker_color="#4D4D4D",
                    opacity=0.8,
                ),
                go.Bar(
                    name="North America",
                    x= dff1.Year.unique(),
                    y= dff1.loc[file['continent'] == 'North America'].groupby('Year')['Total energy consumption (Mtoe)'].mean(),
                    marker_color="#EE2C2C",
                    opacity=0.8
                )
            ]
    )
    fig2.update_layout(
        barmode="stack"
    )
    #return plots
    return fig1, fig2

#circle graph of total consumption of all features by country
@callback(
            Output(component_id='circle_graph', component_property='figure'),
            [Input(component_id='country_dropdown', component_property='value'),
            Input(component_id='slider', component_property='value')])

def update_circle_graph(country_dropdown, value):
    labels_dict ={'Oil products domestic consumption (Mt)': 'Oil',
           'Natural gas domestic consumption (bcm)': 'Gas',
           'Coal and lignite domestic consumption (Mt)': 'Coal', 
           'Electricity domestic consumption (TWh)': 'Electricity'}


    dff2 = file.copy()
    dff2 = dff2[dff2['Year'] == value]
    dff2 = dff2[dff2['Country'] == country_dropdown]
    dff2 = dff2[['Oil products domestic consumption (Mt)','Natural gas domestic consumption (bcm)',
                'Coal and lignite domestic consumption (Mt)','Electricity domestic consumption (TWh)']]

    piechart=px.pie(
                data_frame=dff2,
                values = dff2.values.tolist()[0],
                names= list(labels_dict.values()),
                hole=.8)

    return piechart

#----------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
 