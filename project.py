import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
import geojson



from dash import Dash, dcc, html, Input, Output 

app = Dash(__name__)
# ---------------------------------------------------------------------------------
# Data cleaning

df = pd.read_csv('ActualDataset.csv')

with open("geojson11.geojson") as f:
    gj = geojson.load(f)

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
    dcc.Graph(id="graph"),

    html.Div(id='output_container_slider_dropdown'),
    

    ])

# --------------------------------------------------------------------------------------------------------------------------
# Connect Dash-Components to Data
@app.callback(
    Output('output_container_slider_dropdown', 'children'),
    Output("graph", "figure"),
    [Input('my_slider', 'value'), 
    Input(component_id='drop1', component_property='value')])
def update_output(my_slider, drop1):
    return 'You have selected {} and {}'.format(my_slider, drop1)
def Mapping():
    # Create figure
    fig = px.choropleth_mapbox(
        df,
        geojson=gj,
        featureidkey = "properties.iso_a3",
        locations="iso_a3",
        color=df['Total energy production (Mtoe)'],
        color_continuous_scale='YlOrRd',
        range_color=(0, df['Total energy production (Mtoe)'].max()),
        hover_name='iso_a3', # here maybe Country
        hover_data={'Country': True, 'Total energy production (Mtoe)': True,"iso_a3":False},
        mapbox_style='dark',
        zoom=0.7,
        center={'lat': 19, 'lon': 11},
        opacity=0.6
    )

    # Define layout specificities
    fig.update_layout(
       margin={'r':0,'t':0,'l':0,'b':0},
        coloraxis_colorbar={
            'title':'Total energy production (Mtoe)',
            'tickvals':(0,df['Total energy production (Mtoe)'].max()),
            #'ticktext':ticks        
        })

    # Display figure
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)