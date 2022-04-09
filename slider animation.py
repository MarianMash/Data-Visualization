import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from math import log

from dash import Dash, dcc, html, Input, Output 

app = Dash(__name__)

import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies
from dash.dependencies import Input, Output



app.layout = html.Div([
    html.Div([
        html.Div([
            html.Button(id='buttonPlay', children='Play'),
            html.Button(id='buttonPause', children='Pause'),
            html.Button(id='buttonReset', children='Reset'),
            dcc.Interval(id='interval-component',
                        interval=1500, # in milliseconds
                        n_intervals=0)
        ], style={'width': '15%', 'display': 'inline-block'}),
        html.Div([
        dcc.Slider(
            id = "steper",
            min=1990,
            max=2020,
            step = 1,
            marks={
                1990: '1990',
                1995: '1995',
                2000: '2000',
                2005: '2005',
                2010: '2010',
                2015: '2015',
                2020: '2020'},
            value=1990,
            included = False,
            tooltip={"placement": "bottom", "always_visible": True},
            #updatemode='drag'
            ),
        ], style={'width': '75%', 'display': 'inline-block'}),
        html.Br(),
        html.Br(),
        html.Div(id='msg-container'),
    
    ], className = 'row'),
    html.Div(children=[
                dcc.Graph(id="bar_hor_1", style={'display': 'inline-block','width': '34%'}),
                dcc.Graph(id="world", style={'display': 'inline-block','width': '64%'}),
                ]),
])



@app.callback([
    Output(component_id='interval-component', component_property='disabled'),
    Output(component_id='buttonPlay', component_property='n_clicks'), 
    Output(component_id='buttonPause', component_property='n_clicks'),
    Output(component_id='msg-container', component_property='children')],
    [Input(component_id='buttonPlay', component_property='n_clicks'),
    Input(component_id='buttonPause', component_property='n_clicks'),
    Input(component_id='buttonReset', component_property='n_clicks'),
    Input('steper', 'value'),
    Input('steper', 'drag_value')]
)
def enable_interval_update(buttonPlay, buttonPause, buttonReset, stepper, dragValue):
    msg = 'play: {}, pause: {}, reset: {}, stepper: {}, drag: {}'.format(buttonPlay, buttonPause, buttonReset, stepper, dragValue)
    if not buttonPlay:
        buttonPlay = 0
    if not buttonPause:
        buttonPause = 0

    if buttonPlay > buttonPause:
        return False, 1, 0, msg 
    
    else:
        return True, 0, 0, msg


@app.callback(
    [Output('steper', 'value'),
    Output(component_id='buttonReset', component_property='n_clicks'),
    Output('interval-component', 'n_intervals')
    ], 
    [Input('interval-component', 'n_intervals'), 
    Input(component_id='buttonReset', component_property='n_clicks'),
    Input('steper', 'drag_value')])
def on_click(n_intervals, buttonReset, dragValue):
    if buttonReset is None:
        buttonReset = 0
    if n_intervals is None:
        return 0
    if dragValue is None:
        dragValue = 1990
    
    if buttonReset > 0:
        return 1990, 0, 0 
    
    if int(dragValue) - 1989 != n_intervals:
        n_intervals = int(dragValue) -1990

    return 1990 + (n_intervals)%30, 0, n_intervals

@app.callback(
    [Output(component_id='world',component_property = 'figure'),
    Output(component_id='bar_hor_1',component_property = 'figure'),
    Output(component_id = 'sort_button', component_property = 'children')],

    [Input(component_id = 'steper', component_property = 'value'),
    Input(component_id = 'sort_button', component_property = 'n_clicks')])


def Mapping(selected_year,sort_button_value):
    dff = df.copy()
    dff = dff[dff["Year"]==selected_year]

    # Create figure
    fig = px.choropleth_mapbox(
        dff,
        geojson=gj,
        featureidkey = "properties.iso_a3",
        locations="iso_a3",
        color=dff['Total energy production (Mtoe)'],
        color_continuous_scale='Darkmint',
        range_color=(0, dff['Total energy production (Mtoe)'].max()),

        animation_frame = dff.Year,
        animation_group = dff.iso_a3,

        hover_name='Country', # here maybe Country
        hover_data={'Country': True, 'Total energy production (Mtoe)': True,"iso_a3":False},
        mapbox_style='light',
        zoom=1.01,
        center={'lat': 19, 'lon': 11},
        opacity=0.6
    )

    # Define layout specificities
    fig.update_layout(dragmode=False,
    margin={'r':0,'t':0,'l':0,'b':0},
        coloraxis_colorbar={
            'title':'Mtoe',
            'tickvals':(0,round(dff['Total energy production (Mtoe)'].max())),
         }
         )
    fig.update_coloraxes(colorbar_xanchor="left",   
                            #colorbar_x= -0.01,
                            colorbar_title_side = "right",
                            colorbar_orientation = "v",
                            colorbar_ticks = "inside")





    #horizontal barplot
    if sort_button_value%2:
        dfff=dff.nsmallest(10, ['Total energy production (Mtoe)']).sort_values('Total energy production (Mtoe)', ascending=False)
        
        button_text = "Smallest"
    else: 
        dfff=dff.nlargest(10, ['Total energy production (Mtoe)']).sort_values('Total energy production (Mtoe)', ascending=True)
        button_text = "Largest"

    bar_hor = px.bar(dfff, 
                x='Total energy production (Mtoe)', 
                y="Country", orientation='h',
                barmode = "group",
                color=dfff['Total energy production (Mtoe)'],
                color_continuous_scale='Darkmint',
                range_color=(round(dfff.iloc[9]['Total energy production (Mtoe)']), round(dfff.iloc[0]['Total energy production (Mtoe)'])),
    )
    # bar_hor.update_layout(coloraxis_colorbar={
    #         'title':'Mtoe',
    #         'tickvals':(0,round(dff.iloc[0]['Total energy production (Mtoe)'])),
    #         #'ticktext':ticks        
    #      })
    bar_hor.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },margin={'r':0,'t':0,'l':15,'b':0})
    bar_hor.update_traces(text=list(dfff.Country), textposition='inside',textfont_color='White')
    bar_hor.update_yaxes(visible=False, showticklabels=False)
    bar_hor.update_xaxes(visible=False, showticklabels=False)
    bar_hor.update(layout_coloraxis_showscale=False)



    return fig, bar_hor, button_text 


if __name__ == '__main__':
    app.run_server(debug=True)