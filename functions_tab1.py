from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly

#pip install geojson
import geojson

first = go.Scattermapbox(fill = "toself",
                         lon = [-74, -70, -70, -74], 
                         lat = [47, 47, 45, 45],
                         marker = { 'size': 10, 'color': "orange" })
bar_hor = px.bar(dfff, 
                x='Total energy production (Mtoe)', 
                y="Country", orientation='h',
                barmode = "group",
                color=dfff['Total energy production (Mtoe)'],
                color_continuous_scale='Darkmint',
                range_color=(0, round(dff['Total energy production (Mtoe)'].max())),
    )



first_l = dict(mapbox = {'style': "stamen-terrain",
                         'center': {'lon': -73, 'lat': 46 },
                         'zoom': 5},
               showlegend = False)
second = go.Scattermapbox(fill = "toself",
                          lon = [-60, -90, -50, -60], 
                          lat = [46, 57, 55, 45],
                          marker = { 'size': 10, 'color': "yellow" })
second_l = dict(mapbox = {'style': "stamen-terrain",
                          'center': {'lon': -50, 'lat': 50 },
                          'zoom': 5},
                showlegend = False)