from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly

#pip install geojson
import geojson


# ---------------------------------------------------------------------------------
# Data import and cleaning

df = pd.read_csv('ActualDataset.csv')

with open("geojson11.geojson") as f:
    gj = geojson.load(f)

# Accesstoken for Mapbox-API
plotly.express.set_mapbox_access_token("pk.eyJ1IjoibWFzaGF5ZWtoaTE4IiwiYSI6ImNsMXBkaXpveTE4eGIzY28yY2h2bDR0aWQifQ.4BeYsKCaxz8Mzg1A1C0LrA")


# ---------------------------------------------------------------------------------
# Layout of this tab

layout = html.Div([
    html.H3('Total energy production (Mtoe)'),
    dcc.Slider(id='my_slider',
                min = 1990, 
                max = 2020, 
                step = 1, 
                value=1990,  
                marks = None,
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode='drag'),
    html.Div(id='output_container', children=[]),
    dcc.Graph(id='world', figure={})
    
    
])
