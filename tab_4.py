from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
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
    html.H3('Electricity production (TWh)'),
    dcc.Slider(id='my_slider_1',
                min = 1990, 
                max = 2020, 
                step = 1, 
                value=1990,  
                marks = None,
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode='drag'),
    html.Div(id='output_container_1', children=[]),
    dcc.Graph(id='world_1', figure={}),
    dcc.Graph(id='bar_hor', figure={})
    
])

# ------------------------------------------------------------------------------
# Callbacks of this tab

@callback(
    [Output(component_id='world_1',component_property = 'figure'),
    Output(component_id='output_container_1',component_property = 'children'),
    Output(component_id='bar_hor',component_property = 'figure')],
    [Input(component_id = 'my_slider_1', component_property = 'value')])

def Mapping(selected_year):
    dff = df.copy()
    dff = dff[dff["Year"]==selected_year]

    container = 'You have selected {}'.format(selected_year)
    # Create figure
    fig = px.choropleth_mapbox(
        dff,
        geojson=gj,
        featureidkey = "properties.iso_a3",
        locations="iso_a3",
        color=dff['Electricity production (TWh)'],
        color_continuous_scale='Darkmint',
        range_color=(0, dff['Electricity production (TWh)'].max()),
        animation_frame = dff.Year,
        animation_group = dff.iso_a3,
        hover_name='Country', # here maybe Country
        hover_data={'Country': True, 'Electricity production (TWh)': True,"iso_a3":False},
        mapbox_style='light',
        zoom=1,
        center={'lat': 19, 'lon': 11},
        opacity=0.6
    )

    # Define layout specificities
    fig.update_layout(
    margin={'r':0,'t':0,'l':0,'b':0},
        coloraxis_colorbar={
            'title':'Electricity production (TWh)',
            'tickvals':(0,dff['Electricity production (TWh)'].max()),
            #'ticktext':ticks        
        })

    #horizontal barplot
    dff=dff[['Country','Electricity production (TWh)']].nlargest(12, ['Electricity production (TWh)'])
    bar_hor = px.bar(dff, x="Electricity production (TWh)", y="Country", orientation='h',color_discrete_sequence = "darfmint")
   
    
    return fig, container, bar_hor