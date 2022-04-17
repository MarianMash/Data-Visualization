from dash import dcc, html, Input, Output, callback, callback_context
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from tab_1 import bar_plot_cs


#pip install geojson
import geojson
# ---------------------------------------------------------------------------------
# Data import and cleaning  

df = pd.read_csv('Merged_Energy_Dataset.csv')


        ### Consumption ###
tab_string = "Share of electricity in total final energy consumption (%)"

        ### Production ###
tab_string = "Share of renewables in electricity production (%)"


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
    
def Pie_chart(df1, selected_year,tab_string,cs_name = None):
    def in_percent(integer1):
        return "{:.0%}".format(integer1)
    df_cop = df1.copy()
    df_cop = df_cop[df_cop['Year'] == selected_year]
    
    if cs_name is not None:
        df_cop = df_cop[df_cop.Country == cs_name]
    else:
        pass
    
    if tab_string == "Share of electricity in total final energy consumption (%)":
        share_wind = df_cop["Wind (TWh – sub method)"].sum()/df_cop["Domestic electricity consumption (TWh)"].sum()
        share_solar = df_cop["Solar (TWh – sub method)"].sum()/df_cop["Domestic electricity consumption (TWh)"].sum()
        share_other = 1-share_wind-share_solar


        the_dict = {"Names":["Other","Solar","Wind"],"Values":[share_other,share_solar,share_wind]}



    else:  ### Share of renewables in electricity production (%)
        share_renewables = df_cop["Share of renewables in electricity production (%)"].sum()/len(df_cop["Share of renewables in electricity production (%)"])
        share_other = 100-share_renewables
        the_dict = {"Names":["Not Renewable Energy","Renewables Energy"],"Values":[share_other,share_renewables]}
        
    



    piechart=px.pie(
                data_frame=the_dict,
                values = the_dict["Values"],
                names= the_dict["Names"],
                hole=0.8,
            color_discrete_sequence = px.colors.qualitative.Antique)
    piechart.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },margin={'r':10,'t':0,'l':0,'b':0},legend=dict(yanchor="top", y=0.6, xanchor="left", x=0.40))
    return piechart
    




# ---------------------------------------------------------------------------------
layout = html.Div([

    html.Div(
            [   
                #Buttons Production-Consumption
                dbc.Row(
                    [
                        html.Div([
                                html.Button("Share of renewables",id='Share_of_Renewables', className="m-1 btn btn-info",style={"float":"right"}),
                                html.Button("Share of electricity",id='Share_of_Electricity', className="m-1 btn btn-info",style={"float":"right"}),
                                ],style={"float":"right"})
                    ]
                ),
                #Title 
                dbc.Row(
                    [
                        html.Div(html.H3(tab_string), id='Header_RN',  className="m-3 text-lg-center text-light"),
                        html.Div(html.P("Some text explaining what Share of energies is. Maybe it should be a description that changes at the click of the buttons Share of renewables and Share of electricity"), className="m-3 text-lg-center text-light")
                    ]
                ),
                #Buttons and slider
                dbc.Row(
                    [
                        dbc.Col([
                                html.Button(id='EL_buttonPlay', children='Play', className="m-1 btn btn-success"),
                                html.Button(id='EL_buttonPause', children='Pause', className="m-1 btn btn-success"),
                                html.Button(id='EL_buttonReset', children='Reset', className="m-1 btn btn-success"),
                                ], width=3),
                        dbc.Col([
                                dcc.Interval(id='EL_interval_component', interval=1500, n_intervals=0),
                                dcc.Slider(id='EL_slider', min = 1990, max = 2020, step = 1, value=1990, 
                                marks = {1990: '1990', 1995: '1995', 2000: '2000', 2005: '2005', 2010: '2010', 2015: '2015', 2020: '2020'},
                                tooltip={"placement": "bottom", "always_visible": True},
                                #updatemode='drag'
                                ),
                        ],width=9)
                    ]
                ),
                #two buttons related to bar and map
                dbc.Row([dbc.Col([
                            html.Button('Largest', id='EL_sort_button', n_clicks=0, className="mb-2 mt-3 btn btn-light"),
                        ],width=2),
                        dbc.Col([],width=8),
                ]),
                ## Bar and world plot
                dbc.Row(
                    [
                        dbc.Col(dbc.Card([dbc.CardHeader("Top 10 countries"),
                                        html.Br(className="mb-6"),
                                        dcc.Graph(id="EL_bar_plot"),
                                        html.Br(className="mb-6")],
                                        color="secondary", inverse=True),width=4),
                        dbc.Col(dbc.Card([dbc.CardHeader("World map"),
                                        html.Br(className="mb-6"),
                                        dcc.Graph(id="EL_world_plot"),
                                        html.Br(className="mb-6")],
                                        color="secondary", inverse=True),width=8),
                    ]
                ),

                html.Br(className="mb-6"),
                #button and slider
                html.Div([

                        dbc.Row(
                            [
                                dbc.Col(dbc.Card([dbc.CardHeader("Shares of Renewable Energy per continent"), ## can we have here a html as well? Because then we can make it dynamic
                                                    html.Br(className="mb-6"),
                                                    dcc.RangeSlider(id="EL_interval_slider",
                                                                    min=1990,
                                                                    max=2020,
                                                                    value=[1995, 2015   ],
                                                                    step = 1,
                                                                    className="dcc_control",
                                                                    marks = None,
                                                                    tooltip={"placement": "bottom", "always_visible": True},
                                                                    updatemode='drag'),
                                                    html.Br(className="mb-6"),
                                                dcc.Graph(id='EL_bar_plot_2_2'),
                                                html.Br(className="mb-6")],
                                                color="secondary", inverse=True),width=8),
                                dbc.Col(dbc.Card([dbc.CardHeader("Total Shares of Renewable Energy"),
                                                    html.Br(className="mb-6"),
                                                    dbc.Row([dcc.Slider(id='simple_slider_2_4',
                                                                        min = 1990, 
                                                                        max = 2020, 
                                                                        step = 1, 
                                                                        value=2020,  
                                                                        marks = None,
                                                                        tooltip={"placement": "bottom", "always_visible": True},
                                                                        updatemode='drag'),
                                                            #dcc.Dropdown(options= countries,
                                                            #            value='Portugal',
                                                            #            id='country_dropdown')
                                                            ]),
                                                    html.Br(className="mb-6"),
                                                dcc.Graph(id='circle_graph_2_4')],
                                                color="secondary", inverse=True),width=4),
                            ]
                        ),
                    ]
                )
                # dbc.Row(
                #     [
                #         dbc.Col(
                #                 html.A(html.Button('Show World',className="m-1 btn btn-light"),href='/'),
                #         width=3),
                #         dbc.Col(
                #                 #slider
                #                 html.Div([dcc.RangeSlider(id="EL_interval_slider",
                #                         min=1990,
                #                         max=2020,
                #                         value=[1995, 2015   ],
                #                         step = 1,
                #                         className="dcc_control",
                #                         marks = None,
                #                         tooltip={"placement": "bottom", "always_visible": True},
                #                         updatemode='drag')]),
                #                         width=9)
                #     ]
                # ),  
                # #barchart
                # dbc.Row(
                #     [
                #         dbc.Col(
                #                 #barchart
                #                 dbc.Card([dbc.CardHeader("Shares of Renewable Energy per continent"),
                #                 html.Br(className="mb-6"),
                #                 dcc.Graph(id='EL_bar_plot_2_2'),
                #                 html.Br(className="mb-6")],
                #                 color="secondary"),width=12)
                #     ]
                # ),
            ]
        ),

    ###
    # html.Div(children = [
    #     html.Div([
    #         html.Button("Share of renewables",id='Share_of_Renewables', className="btn btn-success"),
    #         html.Button("Share of electricity",id='Share_of_Electricity', className="btn btn-info"),
    #         ])
    #         ]),
    # html.Div(html.H3(tab_string),
    #     id='Header_RN'),
        
    # html.Div(children = [
    #     html.Div([
    #         html.Button(id='EL_buttonPlay', children='Play', className="btn btn-success"),
    #         html.Button(id='EL_buttonPause', children='Pause', className="btn btn-warning"),
    #         html.Button(id='EL_buttonReset', children='Reset', className="btn btn-primary"),
    #         dcc.Interval(id='EL_interval_component', interval=1500, n_intervals=0)], style={'width': '15%', 'display': 'inline-block'}),
    #     html.Div([
    #         dcc.Slider(id='EL_slider', min = 1990, max = 2020, step = 1, value=1990, 
    #                 marks = {1990: '1990', 1995: '1995', 2000: '2000', 2005: '2005', 2010: '2010', 2015: '2015', 2020: '2020'},
    #                 tooltip={"placement": "bottom", "always_visible": True},
    #                 #updatemode='drag'
    #                 )], style={'width': '75%', 'display': 'inline-block'}),
    #     html.Br(),
    #     html.Br(),
    #     html.Button('Largest', id='EL_sort_button', n_clicks=0, className="btn btn-light"),
    #     html.Button('Related to Population', id='EL_Normalized', n_clicks=0,style={"float":"right"}, className="btn btn-light")],
    # ),

    # html.Div(children=[
    #                     dcc.Graph(id="EL_bar_plot", style={'display': 'inline-block','width': '34%'}),
    #                     dcc.Graph(id="EL_world_plot", style={'display': 'inline-block','width': '64%'}),
    #                     ]),
    # html.Br(),
    # html.Br(),##

    # html.A(html.Button('Show World'),href='/'), #### this one can be improved
    
    # html.Div([dcc.RangeSlider(id="EL_interval_slider",
    #                 min=1990,
    #                 max=2020,
    #                 value=[1995, 2015   ],
    #                 step = 1,
    #                 className="dcc_control",
    #                 marks = None,
    #                 tooltip={"placement": "bottom", "always_visible": True},
    #                 updatemode='drag')]),
    # dcc.Graph(id='EL_bar_plot_2_2'),
                    

],className="m-3")
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
    Output(component_id ='EL_world_plot',component_property = 'figure'),
    Output(component_id ='EL_bar_plot',component_property = 'figure'),
    Output(component_id ='EL_bar_plot_2_2',component_property = 'figure'),
    Output(component_id = 'circle_graph_2_4', component_property ='figure'),



    [Input(component_id = 'EL_slider', component_property = 'value'),
    Input(component_id = 'Share_of_Renewables', component_property = 'n_clicks_timestamp'),
    Input(component_id = 'Share_of_Electricity', component_property = 'n_clicks_timestamp'),
    Input(component_id = 'EL_sort_button', component_property = 'n_clicks'),
    Input(component_id = 'EL_interval_slider', component_property = 'value'),
    Input(component_id ='simple_slider_2_4',component_property = 'value'),

    Input(component_id ='EL_world_plot',component_property = 'clickData'),

    ])
def update_graph(selected_year,Share_of_Renewables,Share_of_Electricity,sort_button2_value,value_bar,value_pie,c_selection):
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
    tab_string = 'Share of electricity in total final energy consumption (%)'
    header = [html.H3(tab_string)]
    
### determine which button was clicked last by comparing timestamps
    if Share_of_Renewables<Share_of_Electricity:
        # list_1 = consumption
        tab_string = 'Share of electricity in total final energy consumption (%)'
        header = [html.H3(tab_string)]

    if Share_of_Renewables > Share_of_Electricity:
        # list_1 = production 
        tab_string = "Share of renewables in electricity production (%)"
    
        header = [html.H3(tab_string)]
        

     # Largst / Smallest Button
    if sort_button2_value%2:
        dfff=dff.nsmallest(10, [tab_string]).sort_values(tab_string, ascending=False)
        
        button_text = "Smallest"
    else: 
        dfff=dff.nlargest(10, [tab_string]).sort_values(tab_string, ascending=True)
        button_text = "Largest"


    
    ########################################################################################################################################################    
    # Create figure
    fig = px.choropleth_mapbox(
        dff,
        geojson=gj,
        featureidkey = "properties.iso_a3",
        locations="iso_a3",
        color=dff[tab_string],
        color_continuous_scale='Darkmint',
        range_color=(0, dff[tab_string].max()),

        animation_frame = dff.Year,
        animation_group = dff.iso_a3,

        hover_name='Country', # here maybe Country
        hover_data={'Country': True, tab_string: True,"iso_a3":False},
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
            'tickvals':(0,round(dff[tab_string].max())),
         }
         )
    fig.update_coloraxes(colorbar_xanchor="left",   
                            #colorbar_x= -0.01,
                            colorbar_title_side = "right",
                            colorbar_orientation = "v",
                            colorbar_ticks = "inside")

    fig.update(layout_showlegend=False,layout_coloraxis_showscale = False)


 #horizontal barplot
 

    bar_hor = px.bar(dfff, 
                x=tab_string, 
                y="Country", orientation='h',
                barmode = "group",
                color=dfff[tab_string],
                color_continuous_scale='Darkmint',
                range_color=(round(dfff.iloc[9][tab_string]), round(dfff.iloc[0][tab_string])),
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
    bar_hor.update_traces(text=list(dfff.Country), textposition='inside')
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
        pie = Pie_chart(df, value_pie,tab_string,cs_name)

        
        return header, button_text , fig, bar_hor, figure1 , pie
    else:
        fig2 =  Continent_comp(df, tab_string,value_bar)
        pie = Pie_chart(df, value_pie,tab_string)

        return header, button_text , fig, bar_hor, fig2 , pie