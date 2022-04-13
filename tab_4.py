from dash import dcc, html, Input, Output, callback, callback_context
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly
import plotly.graph_objects as go

from tab_1 import bar_plot_cs


#pip install geojson
import geojson
# ---------------------------------------------------------------------------------
# Data import and cleaning  

df = pd.read_csv('ActualDataset.csv')

        ### Consumption ###
tab_string = "Share of electricity in total final energy consumption (%)"
df[f"{tab_string}_div_pop"] = (df[tab_string]/df["pop_est"])*10000

        ### Production ###
tab_string = "Share of renewables in electricity production (%)"
df[f"{tab_string}_div_pop"] = (df[tab_string]/df["pop_est"])*10000


with open("geojson11.geojson") as f:
    gj = geojson.load(f)

def Continent_comp(df, tabstring,value):
    #bar plot 1 with renewables values per continent
    dff = df.copy()
    dff = dff[(dff['Year'] >= value[0]) & (dff['Year'] <= value[1])]
    dff = dff[[tabstring, 'continent', 'Year']]

    fig1 = go.Figure(
        data=[
            go.Bar(
                name="Europe",
                x= dff.Year.unique(),
                y= dff.loc[dff['continent'] == 'Europe'].groupby('Year')[tabstring].mean(),
                marker_color="#004687",
                opacity=0.8,
            ),
            go.Bar(
                name="Asia",
                x= dff.Year.unique(),
                y=dff.loc[dff['continent'] == 'Asia'].groupby('Year')[tabstring].mean(),
                marker_color="#AE8F6F",
                opacity=0.8,
            ),
            go.Bar(
                name="Oceania",
                x= dff.Year.unique(),
                y= dff.loc[dff['continent'] == 'Oceania'].groupby('Year')[tabstring].mean(),
                marker_color="#FF9912",
                opacity=0.8,
            ),
            go.Bar(
                name="Africa",
                x= dff.Year.unique(),
                y= dff.loc[dff['continent'] == 'Africa'].groupby('Year')[tabstring].mean(),
                marker_color="#4D4D4D",
                opacity=0.8,
            ),
            go.Bar(
                name="North America",
                x= dff.Year.unique(),
                y= dff.loc[dff['continent'] == 'North America'].groupby('Year')[tabstring].mean(),
                marker_color="#EE2C2C",
                opacity=0.8
            )]
            )
    fig1.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="left",
                x=0.3
    ))
    return fig1
# ---------------------------------------------------------------------------------
layout = html.Div([
    html.Div(children = [
        html.Div([
            html.Button("Share of renewables",id='Share_of_Renewables', className="btn btn-success"),
            html.Button("Share of electricity",id='Share_of_Electricity', className="btn btn-info"),
            ])
            ]),
    html.Div(html.H3(tab_string),
        id='Header_RN'),
        
    html.Div(children = [
        html.Div([
            html.Button(id='EL_buttonPlay', children='Play', className="btn btn-success"),
            html.Button(id='EL_buttonPause', children='Pause', className="btn btn-warning"),
            html.Button(id='EL_buttonReset', children='Reset', className="btn btn-primary"),
            dcc.Interval(id='EL_interval_component', interval=1500, n_intervals=0)], style={'width': '15%', 'display': 'inline-block'}),
        html.Div([
            dcc.Slider(id='EL_slider', min = 1990, max = 2020, step = 1, value=1990, 
                    marks = {1990: '1990', 1995: '1995', 2000: '2000', 2005: '2005', 2010: '2010', 2015: '2015', 2020: '2020'},
                    tooltip={"placement": "bottom", "always_visible": True},
                    #updatemode='drag'
                    )], style={'width': '75%', 'display': 'inline-block'}),
        html.Br(),
        html.Br(),
        html.Button('Largest', id='EL_sort_button', n_clicks=0, className="btn btn-light"),
        html.Button('Related to Population', id='EL_Normalized', n_clicks=0,style={"float":"right"}, className="btn btn-light")],
    ),

    html.Div(children=[
                        dcc.Graph(id="EL_bar_plot", style={'display': 'inline-block','width': '34%'}),
                        dcc.Graph(id="EL_world_plot", style={'display': 'inline-block','width': '64%'}),
                        ]),
    html.Br(),
    html.Br(),##

    html.A(html.Button('Show World'),href='/'), #### this one can be improved
    
    html.Div([dcc.RangeSlider(id="EL_interval_slider",
                    min=1990,
                    max=2020,
                    value=[1995, 2015   ],
                    step = 1,
                    className="dcc_control",
                    marks = None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode='drag')]),
    dcc.Graph(id='EL_bar_plot_2_2'),
                    

    ])
# ------------------------------------------------------------------------------
# Callbacks of this tab

@callback([
    Output(component_id='EL_interval_component', component_property='disabled'),
    Output(component_id='EL_buttonPlay', component_property='n_clicks'), 
    Output(component_id='EL_buttonPause', component_property='n_clicks'),
    #Output(component_id='msg-container', component_property='children')
    ],
    [Input(component_id='EL_buttonPlay', component_property='n_clicks'),
    Input(component_id='EL_buttonPause', component_property='n_clicks'),
    Input(component_id='EL_buttonReset', component_property='n_clicks'),
    Input(component_id='EL_slider', component_property='value'),
    Input(component_id='EL_slider', component_property='drag_value'),
    ]
)
def enable_interval_update(PlayButton, PauseButton, buttonReset, stepper, dragValue):
    #msg = 'play: {}, pause: {}, reset: {}, stepper: {}, drag: {}'.format(buttonPlay, buttonPause, buttonReset, stepper, dragValue)
    if not PlayButton:
        PlayButton = 0
    if not PauseButton:
        PauseButton = 0

    if PlayButton > PauseButton:
        return False, 1, 0#, msg 
    
    else:
        return True, 0, 0#, msg


@callback(
    [Output(component_id='EL_slider', component_property='value'),
    Output(component_id='EL_buttonReset', component_property='n_clicks'),
    Output(component_id='EL_interval_component', component_property='n_intervals')
    ], 
    [Input(component_id='EL_interval_component', component_property='n_intervals'), 
    Input(component_id='EL_buttonReset', component_property='n_clicks'),
    Input(component_id='EL_slider', component_property='drag_value')])
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

@callback(
    Output(component_id='Header_RN', component_property='children'),

    Output(component_id = 'EL_sort_button', component_property = 'children'),
    Output(component_id = 'EL_Normalized', component_property = 'children'),
    Output(component_id ='EL_world_plot',component_property = 'figure'),
    Output(component_id ='EL_bar_plot',component_property = 'figure'),
    Output(component_id ='EL_bar_plot_2_2',component_property = 'figure'),


    [Input(component_id = 'EL_slider', component_property = 'value'),
    Input(component_id = 'Share_of_Renewables', component_property = 'n_clicks_timestamp'),
    Input(component_id = 'Share_of_Electricity', component_property = 'n_clicks_timestamp'),
    Input(component_id = 'EL_Normalized', component_property = 'n_clicks'),
    Input(component_id = 'EL_sort_button', component_property = 'n_clicks'),
    Input(component_id = 'EL_interval_slider', component_property = 'value'),
    Input(component_id ='EL_world_plot',component_property = 'clickData'),

    ])
def update_graph(selected_year,Share_of_Renewables,Share_of_Electricity, sort_button_value,sort_button2_value,value_bar,c_selection):
    dff = df.copy()
    dff = dff[dff["Year"]==selected_year]
    
########################################################################################################################################################
    ############## 

    # Normalize Button
        # Production or Consumption
    
    # initialize Timestamps if they're not clicked yet

    if Share_of_Renewables is None:
        Share_of_Renewables = 0
    if Share_of_Electricity is None:
        Share_of_Electricity= 0

    # list_1 = production
    tab_string = "Share of electricity in total final energy consumption (%)"
    header = [html.H3(tab_string)]
    
### determine which button was clicked last by comparing timestamps
    if Share_of_Renewables<Share_of_Electricity:
        # list_1 = consumption
        tab_string = "Share of electricity in total final energy consumption (%)"
        header = [html.H3(tab_string)]

    if Share_of_Renewables > Share_of_Electricity:
        # list_1 = production 
        tab_string = "Share of renewables in electricity production (%)"
    
        header = [html.H3(tab_string)]
        
### Absolute or relative
    if sort_button_value%2:
        the_column = f"{tab_string}_div_pop"
        button2_text = "Per 10000-Capita"
    else: 
        button2_text = "Absolute"
        the_column = tab_string

     # Largst / Smallest Button
    if sort_button2_value%2:
        dfff=dff.nsmallest(10, [the_column]).sort_values(the_column, ascending=False)
        
        button_text = "Smallest"
    else: 
        dfff=dff.nlargest(10, [the_column]).sort_values(the_column, ascending=True)
        button_text = "Largest"


    
    ########################################################################################################################################################    
    # Create figure
    fig = px.choropleth_mapbox(
        dff,
        geojson=gj,
        featureidkey = "properties.iso_a3",
        locations="iso_a3",
        color=dff[the_column],
        color_continuous_scale='Darkmint',
        range_color=(0, dff[the_column].max()),

        animation_frame = dff.Year,
        animation_group = dff.iso_a3,

        hover_name='Country', # here maybe Country
        hover_data={'Country': True, the_column: True,"iso_a3":False},
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
            'tickvals':(0,round(dff[the_column].max())),
         }
         )
    fig.update_coloraxes(colorbar_xanchor="left",   
                            #colorbar_x= -0.01,
                            colorbar_title_side = "right",
                            colorbar_orientation = "v",
                            colorbar_ticks = "inside")

    fig.update(layout_showlegend=False)


 #horizontal barplot
 

    bar_hor = px.bar(dfff, 
                x=the_column, 
                y="Country", orientation='h',
                barmode = "group",
                color=dfff[the_column],
                color_continuous_scale='Darkmint',
                range_color=(round(dfff.iloc[9][the_column]), round(dfff.iloc[0][the_column])),
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
    

########################################## Barchart ##############################################################################################

        #bar plot 2 with total consumption values per continent
    dff1 = df.copy()
    dff1 = dff1[(dff1['Year'] >= value_bar[0]) & (dff1['Year'] <= value_bar[1])]
    dff1 = dff1[[tab_string, 'continent', 'Year']]

    fig2 = go.Figure(
            data=[
                go.Bar(
                    name="Europe",
                    x= dff1.Year.unique(),
                    y= dff1.loc[df['continent'] == 'Europe'].groupby('Year')[tab_string].mean(),
                    marker_color="#004687",
                    opacity=0.8,
                ),
                go.Bar(
                    name="Asia",
                    x= dff1.Year.unique(),
                    y=dff1.loc[df['continent'] == 'Asia'].groupby('Year')[tab_string].mean(),
                    marker_color="#AE8F6F",
                    opacity=0.8,
                ),
                go.Bar(
                    name="Oceania",
                    x= dff1.Year.unique(),
                    y= dff1.loc[df['continent'] == 'Oceania'].groupby('Year')[tab_string].mean(),
                    marker_color="#FF9912",
                    opacity=0.8,
                ),
                go.Bar(
                    name="Africa",
                    x= dff1.Year.unique(),
                    y= dff1.loc[df['continent'] == 'Africa'].groupby('Year')[tab_string].mean(),
                    marker_color="#4D4D4D",
                    opacity=0.8,
                ),
                go.Bar(
                    name="North America",
                    x= dff1.Year.unique(),
                    y= dff1.loc[df['continent'] == 'North America'].groupby('Year')[tab_string].mean(),
                    marker_color="#EE2C2C",
                    opacity=0.8
                )
            ]
    )
    fig2.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },margin={'r':0,'t':0,'l':10,'b':0},barmode="stack",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="left",
                x=0.3
    ))

    if c_selection is not None:
        
        location = c_selection['points'][0]['location']
        cs_name = dff[dff.iso_a3 == location]["Country"].to_list()[0]

        figure1 = bar_plot_cs(df,value_bar,cs_name,tab_string)

        
        return header, button_text , button2_text, fig, bar_hor, figure1 
    else:
        fig2 =  Continent_comp(df, tab_string,value_bar)

        return header, button_text , button2_text, fig, bar_hor, fig2 