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
    html.H3('Tab content 1'),
    dcc.Slider(id='my_slider',
                min = 1990, 
                max = 2020, 
                step = 1, 
                value=1990,  
                marks = None,
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode='drag'),
    html.Div(children=[
                    dcc.Graph(id="world", style={'display': 'inline-block'}),
                    dcc.Graph(id="bar_hor_1", style={'display': 'inline-block'})
                    ]),
    html.Div(id='output_container', children=[]),
    
    
])

# ------------------------------------------------------------------------------
# Callbacks of this tab

@callback(
    [Output(component_id='world',component_property = 'figure'),
    Output(component_id='output_container',component_property = 'children'),
    Output(component_id='bar_hor_1',component_property = 'figure')],
    [Input(component_id = 'my_slider', component_property = 'value')])

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
        color=dff['Total energy production (Mtoe)'],
        color_continuous_scale='Darkmint',
        range_color=(0, round(dff['Total energy production (Mtoe)'].max())),

        animation_frame = dff.Year,
        animation_group = dff.iso_a3,

        hover_name='Country', # here maybe Country
        hover_data={'Country': True, 'Total energy production (Mtoe)': True,"iso_a3":False},
        mapbox_style='light',
        zoom=1,
        center={'lat': 19, 'lon': 11},
        opacity=0.6
    )

    # Define layout specificities
    fig.update_layout(
    margin={'r':0,'t':0,'l':0,'b':0},
        coloraxis_colorbar={
            'title':'Mtoe',
            'tickvals':(0,dff['Total energy production (Mtoe)'].max()),
            #'ticktext':ticks        
         },legend=dict(
        yanchor="bottom",
        y=0.99,
        xanchor="right",
        x=0.01
)
        )
    # fig.update_layout(updatemenus= [dict(type="buttons",button = )])
        #horizontal barplot
    dfff=dff.nlargest(12, ['Total energy production (Mtoe)']).sort_values('Total energy production (Mtoe)', ascending=True)
    bar_hor = px.bar(dfff, 
                x='Total energy production (Mtoe)', 
                y="Country", orientation='h',
                barmode = "group",
                color=dfff['Total energy production (Mtoe)'],
                color_continuous_scale='Darkmint',
                range_color=(0, round(dff['Total energy production (Mtoe)'].max())),
    )
    bar_hor.update_layout(coloraxis_colorbar={
            'title':'Mtoe',
            'tickvals':(0,round(dff['Total energy production (Mtoe)'].max())),
            #'ticktext':ticks        
         })
    bar_hor.update_traces(text=list(dfff.Country), textposition='inside',textfont_color='White')
    bar_hor.update_yaxes(visible=False, showticklabels=False)


    return fig, container, bar_hor