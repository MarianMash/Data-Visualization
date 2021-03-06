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

# Consumption 
tab_string = "Share of electricity in total final energy consumption (%)"
tab_string_new = 'Share of wind and solar in electricity production (%)'

# Production
tab_string = "Share of renewables in electricity production (%)"

description_string = """"Share of electricity in total final energy consumption is the ratio between the electricity 
                                consumption and the total energy consumed for commercial purposes"""

# headers for the barchart and piechart of the second row 
header_barplot_2_4_string = "Share of "
header_pieplot_2_4_string = "Share of "

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
                marker_color="#d5f4e6",
                opacity=0.8,
            ),
            go.Bar(
                name="Asia",
                x= dff.Year.unique(),
                y=dff.loc[dff['continent'] == 'Asia'].groupby('Year')[tabstring].mean(),
                marker_color="#618685",
                opacity=0.8,
            ),
            go.Bar(
                name="Oceania",
                x= dff.Year.unique(),
                y= dff.loc[dff['continent'] == 'Oceania'].groupby('Year')[tabstring].mean(),
                marker_color="#80ced6",
                opacity=0.8,
            ),
            go.Bar(
                name="Africa",
                x= dff.Year.unique(),
                y= dff.loc[dff['continent'] == 'Africa'].groupby('Year')[tabstring].mean(),
                marker_color="#fefbd8",
                opacity=0.8,
            ),
            go.Bar(
                name="North America",
                x= dff.Year.unique(),
                y= dff.loc[dff['continent'] == 'North America'].groupby('Year')[tabstring].mean(),
                marker_color="#36486b",
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
        share_wind = df_cop["Wind (TWh ??? sub method)"].sum()/df_cop["Domestic electricity consumption (TWh)"].sum()
        share_solar = df_cop["Solar (TWh ??? sub method)"].sum()/df_cop["Domestic electricity consumption (TWh)"].sum()
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
            color_discrete_sequence = px.colors.qualitative.Prism)
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
                                html.Button("% in electricity production",id='Share_of_Renewables', className="m-1 btn btn-info",style={"float":"right"}),
                                html.Button("% of wind and solar",id='Share_of_Electricity', className="m-1 btn btn-info",style={"float":"right"}),
                                ],style={"float":"right"})
                    ]
                ),
                #Title 
                dbc.Row(
                    [
                        html.Div(html.H3(tab_string), id='Header_RN',  className="m-3 text-lg-center text-light"),
                        dbc.Col([
                            html.Div(html.P(description_string), id='Second_Header_RN', className="m-3 text-lg text-light")
                        ],width={'size':8, 'offset':2})
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
                                ),
                        ],width=9)
                    ]
                ),
                # two buttons related to bar and map
                dbc.Row([dbc.Col([
                            html.Button('Largest', id='EL_sort_button', n_clicks=0, className="mb-2 mt-3 btn btn-light"),
                        ],width=2),
                        dbc.Col([],width=8),
                ]),
                # Bar and world plot
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
                html.P("To display the values of a specific country in the following plots, click on it in the map. To reset the statistics click on the following button"),
                html.A(html.Button(id = 'btnShowWorldT4', children = 'Show World', className="m-1 btn btn-light")), 
                html.Br(className="mb-6"),
                # button and slider
                html.Div([
                        dbc.Row(
                            [
                                dbc.Col(dbc.Card([dbc.CardHeader(header_barplot_2_4_string, id='header_barplot_2_4'), 
                                    #"Shares of renewable energy per continent"
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
                                dbc.Col(dbc.Card([dbc.CardHeader(header_pieplot_2_4_string, id='header_pieplot_2_4'
                                    #"Total shares of renewable energy"
                                    ),
                                                    html.Br(className="mb-6"),
                                                    dbc.Row([dcc.Slider(id='simple_slider_2_4',
                                                                        min = 1990, 
                                                                        max = 2020, 
                                                                        step = 1, 
                                                                        value=2020,  
                                                                        marks = None,
                                                                        tooltip={"placement": "bottom", "always_visible": True},
                                                                        updatemode='drag'),
                                                            ]),
                                                    html.Br(className="mb-6"),
                                                dcc.Graph(id='circle_graph_2_4'),
                                                html.Br(className="mb-6")],
                                                color="secondary", inverse=True),width=4),
                            ]
                        ),
                    ]
                )
            ]
        ),  
],className="m-3")

# ------------------------------------------------------------------------------
# Callbacks of this tab

@callback([
    Output(component_id='EL_interval_component', component_property='disabled'),
    Output(component_id='EL_buttonPlay', component_property='n_clicks'), 
    Output(component_id='EL_buttonPause', component_property='n_clicks'),
    ],
    [Input(component_id='EL_buttonPlay', component_property='n_clicks'),
    Input(component_id='EL_buttonPause', component_property='n_clicks'),
    Input(component_id='EL_buttonReset', component_property='n_clicks'),
    Input(component_id='EL_slider', component_property='value'),
    Input(component_id='EL_slider', component_property='drag_value'),
    ]
)
def enable_interval_update(PlayButton, PauseButton, buttonReset, stepper, dragValue):    
    if not PlayButton:
        PlayButton = 0
    if not PauseButton:
        PauseButton = 0

    if PlayButton > PauseButton:
        return False, 1, 0
    
    else:
        return True, 0, 0

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

@callback([
    Output(component_id='Header_RN', component_property='children'),
    Output(component_id='Second_Header_RN', component_property='children'),
    Output(component_id = 'EL_sort_button', component_property = 'children'),
    Output(component_id ='EL_world_plot',component_property = 'figure'),
    Output(component_id ='EL_bar_plot',component_property = 'figure'),
    Output(component_id ='EL_bar_plot_2_2',component_property = 'figure'),
    Output(component_id = 'circle_graph_2_4', component_property ='figure'),
    Output(component_id='header_barplot_2_4', component_property='children'),
    Output(component_id='header_pieplot_2_4', component_property='children'),
    Output(component_id='btnShowWorldT4', component_property='n_clicks_timestamp'),
    ],
    [Input(component_id = 'EL_slider', component_property = 'value'),
    Input(component_id = 'Share_of_Renewables', component_property = 'n_clicks_timestamp'),
    Input(component_id = 'Share_of_Electricity', component_property = 'n_clicks_timestamp'),
    Input(component_id = 'EL_sort_button', component_property = 'n_clicks'),
    Input(component_id = 'EL_interval_slider', component_property = 'value'),
    Input(component_id ='simple_slider_2_4',component_property = 'value'),
    Input(component_id ='EL_world_plot',component_property = 'clickData'),
    Input(component_id='btnShowWorldT4', component_property='n_clicks_timestamp'),
    ])

def update_graph(selected_year,Share_of_Renewables,Share_of_Electricity,sort_button2_value,value_bar,value_pie,c_selection, btnShowWorld):
    dff = df.copy()
    dff = dff[dff["Year"]==selected_year]
    
    # initialize Timestamps if they're not clicked yet
    if Share_of_Renewables is None:
        Share_of_Renewables = 0
    if Share_of_Electricity is None:
        Share_of_Electricity= 0

    # list_1 = production
    tab_string = 'Share of electricity in total final energy consumption (%)'
    tab_string_new = 'Share of wind and solar in electricity consumption (%)'
    header = [html.H3(tab_string_new)]
    description_string = """Share of electricity in total final energy consumption is the ratio between the 
                            electricity consumption and the total energy consumed for commercial purposes."""
    second_header = [html.P(description_string)]
    header_barplot_2_4_string = "Share of "
    header_pieplot_2_4_string = "Share of "


    # determine which button was clicked last by comparing timestamps
    if Share_of_Renewables<Share_of_Electricity:
        # list_1 = consumption
        tab_string = 'Share of electricity in total final energy consumption (%)'
        tab_string_new = 'Share of wind and solar in electricity production (%)'
        header = [html.H3(tab_string_new)]
        description_string = """Share of wind and solar energy in electricity production as the name suggests represents the percentage 
                            of electricity produced from wind and solar energy over the total electricity production."""
        second_header = [html.P(description_string)]
        header_barplot_2_4_string += 'wind and solar energy of the electricity production'
        header_pieplot_2_4_string += 'wind and solar energy of the electricity production'

    if Share_of_Renewables >= Share_of_Electricity:
        # list_1 = production 
        tab_string = "Share of renewables in electricity production (%)"
        tab_string_new = "Share of renewables in electricity production (%)"
        header = [html.H3(tab_string_new)]
        description_string = """Share of renewables in electricity production represents the percentage of energy coming from renewable sources
                            like wind, solar, hydropower, geothermal and bio energies """
        second_header = [html.P(description_string)]
        header_barplot_2_4_string += 'renewable energy '
        header_pieplot_2_4_string += 'renewable energy '

     # Largest / Smallest Button
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

        hover_name='Country', 
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
                    marker_color="#d5f4e6",
                    opacity=0.8,
                ),
                go.Bar(
                    name="Asia",
                    x= dff1.Year.unique(),
                    y=dff1.loc[df['continent'] == 'Asia'].groupby('Year')[tab_string].mean(),
                    marker_color="#618685",
                    opacity=0.8,
                ),
                go.Bar(
                    name="Oceania",
                    x= dff1.Year.unique(),
                    y= dff1.loc[df['continent'] == 'Oceania'].groupby('Year')[tab_string].mean(),
                    marker_color="#80ced6",
                    opacity=0.8,
                ),
                go.Bar(
                    name="Africa",
                    x= dff1.Year.unique(),
                    y= dff1.loc[df['continent'] == 'Africa'].groupby('Year')[tab_string].mean(),
                    marker_color="#fefbd8",
                    opacity=0.8,
                ),
                go.Bar(
                    name="North America",
                    x= dff1.Year.unique(),
                    y= dff1.loc[df['continent'] == 'North America'].groupby('Year')[tab_string].mean(),
                    marker_color="#36486b",
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
                x=0.3),
            yaxis=dict(title="%"))

    
    # show world button 
    if btnShowWorld is not None:
        c_selection = None

    if c_selection is not None:
        
        location = c_selection['points'][0]['location']
        cs_name = dff[dff.iso_a3 == location]["Country"].to_list()[0]


        figure1 = bar_plot_cs(df,value_bar,cs_name,tab_string)
        pie = Pie_chart(df, value_pie,tab_string,cs_name)

        # generate header string for the barplot
        header_barplot_2_4_string += ' of ' + cs_name
        header_barplot_2_4 = [html.P(header_barplot_2_4_string)]

        #generate header string for the piechart
        header_pieplot_2_4_string += ' of ' + cs_name #+ ' per energy type'
        header_pieplot_2_4 = [html.P(header_pieplot_2_4_string)]
        
        return header,second_header, button_text , fig, bar_hor, figure1 , pie, header_barplot_2_4, header_pieplot_2_4, None
    else:
        fig2 =  Continent_comp(df, tab_string,value_bar)
        pie = Pie_chart(df, value_pie,tab_string)

        # generate header string for the barplot
        header_barplot_2_4_string += ' per continent'
        header_barplot_2_4 = [html.P(header_barplot_2_4_string)] 

        #generate header string for the piechart
        header_pieplot_2_4_string += ' per energy type'
        header_pieplot_2_4 = [html.P(header_pieplot_2_4_string)] 

        return header,second_header, button_text , fig, bar_hor, fig2 , pie, header_barplot_2_4, header_pieplot_2_4, None