from dash import dcc, html, Input, Output, callback, callback_context
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from tab_1 import bar_plot_cs


#pip install geojson
import geojson

# ---------------------------------------------------------------------------------##
# Data import and cleaning

df = pd.read_csv('Merged_Energy_Dataset.csv')

# Production
tab_string = "Electricity production (TWh)"
header_barplot_2_2_string = "Total Electricity "
df[f"{tab_string}_div_pop"] = (df[tab_string]/df["pop_est"])*10000

# Consumption
tab_string = "Domestic electricity consumption (TWh)"
df[f"{tab_string}_div_pop"] = (df[tab_string]/df["pop_est"])*10000


with open("geojson11.geojson") as f:
    gj = geojson.load(f)

# ---------------------------------------------------------------------------------
# Layout of this tab

layout = html.Div([

    html.Div(
            [   
                #Buttons Production-Consumption
                dbc.Row(
                    [
                        dbc.Col([
                                html.Button("Production",id='Prod_1', className="mx-1 btn btn-info"),
                                html.Button("Consumption",id='Cons_1', className="mx-1 btn btn-info"),
                                ],width={'size':3,'offset':4})
                    ],justify="center"
                ),
                #Title 
                dbc.Row(
                    [
                        html.Div(html.H3(tab_string),id='Header_elec', className="m-3 text-lg-center text-light"),
                        dbc.Col([
                            html.Div(html.P("""Electricity production is the sum of the electrical energy production by all the generating units concerned,
                                        while the electricity consumption represents the amount of electrical energy demanded from the existing electricity supply for every day to day purposes."""), className="m-3 text-lg text-light")
                        ],width={'size':8, 'offset':2})
                    ]
                ),
                #Buttons and slider
                dbc.Row(
                    [
                        dbc.Col([
                                
                                html.Button(id='PlayButton', children='Play', className="m-1 btn btn-success"),
                                html.Button(id='PauseButton', children='Pause', className="m-1 btn btn-success"),
                                html.Button(id='ResetButton', children='Reset', className="m-1 btn btn-success"),
                                ], width=3),
                        dbc.Col([
                                dcc.Interval(id='IntervalComponent', interval=1500, n_intervals=0),
                                dcc.Slider(id='Slider', min = 1990, max = 2020, step = 1, value=1990, 
                                            marks = {1990: '1990', 1995: '1995', 2000: '2000', 2005: '2005', 2010: '2010', 2015: '2015', 2020: '2020'},
                                            tooltip={"placement": "bottom", "always_visible": True},
                                            )
                        ],width=9)
                    ]
                ),
                #two buttons related to bar and map
                dbc.Row([dbc.Col([
                            html.Button('Largest', id='Button_for_Sorting', n_clicks=0, className="mb-2 mt-3 btn btn-light"),
                        ],width=2),
                        dbc.Col([],width=8),
                        dbc.Col([
                            html.Button('Related to Population', id='Button_for_Normalize', n_clicks=0,style={"float":"right"}, className="mb-2 mt-3 btn btn-light")
                        ],width=2)
                ]),
                #Bar chart and map graph
                dbc.Row(
                    [
                        dbc.Col(dbc.Card([dbc.CardHeader("Top 10 countries"),
                                        html.Br(className="mb-6"),
                                        dcc.Graph(id="bar_plot"),
                                        html.Br(className="mb-6")],
                                        color="secondary", inverse=True),width=4),
                        dbc.Col(dbc.Card([dbc.CardHeader("World map"),
                                        html.Br(className="mb-6"),
                                        dcc.Graph(id="world_plot"),
                                        html.Br(className="mb-6")],
                                        color="secondary", inverse=True),width=8),
                    ]
                ),
            ]
        ),
    html.P("To display the values of a specific country in the following plot, click on it in the map. To reset the statistics click on the following button"),
    html.A(html.Button(id = 'btnShowWorld', children = 'Show World', className="m-1 btn btn-light")),
    html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(dbc.Card([dbc.CardHeader(header_barplot_2_2_string, id='header_barplot_2_2'), 
                                            html.Br(className="mb-6"),
                                            dcc.RangeSlider(id="interval_slider",
                                                            min=1990,
                                                            max=2020,
                                                            value=[1995, 2015   ],
                                                            step = 1,
                                                            className="dcc_control",
                                                            marks = None,
                                                            tooltip={"placement": "bottom", "always_visible": True},
                                                            updatemode='drag'),
                                            html.Br(className="mb-6"),
                                        dcc.Graph(id='bar_plot_2_2'),
                                        html.Br(className="mb-6")],
                                        color="secondary", inverse=True),width=12)
                    ]
                ),
            ]
        )
                    
    ], className="m-3"  
)

# ------------------------------------------------------------------------------
# Callbacks of this tab
@callback([
    Output(component_id='IntervalComponent', component_property='disabled'),
    Output(component_id='PlayButton', component_property='n_clicks'), 
    Output(component_id='PauseButton', component_property='n_clicks'),
    ],
    [Input(component_id='PlayButton', component_property='n_clicks'),
    Input(component_id='PauseButton', component_property='n_clicks'),
    Input(component_id='ResetButton', component_property='n_clicks'),
    Input(component_id='Slider', component_property='value'),
    Input(component_id='Slider', component_property='drag_value'),
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
    [Output(component_id='Slider', component_property='value'),
    Output(component_id='ResetButton', component_property='n_clicks'),
    Output(component_id='IntervalComponent', component_property='n_intervals')
    ], 
    [Input(component_id='IntervalComponent', component_property='n_intervals'), 
    Input(component_id='ResetButton', component_property='n_clicks'),
    Input(component_id='Slider', component_property='drag_value')])
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
    Output(component_id='Header_elec', component_property='children'),
    Output(component_id = 'Button_for_Sorting', component_property = 'children'),
    Output(component_id = 'Button_for_Normalize', component_property = 'children'),
    Output(component_id ='world_plot',component_property = 'figure'),
    Output(component_id ='bar_plot',component_property = 'figure'),
    Output(component_id ='bar_plot_2_2',component_property = 'figure'),
    Output(component_id='header_barplot_2_2', component_property='children'),
    Output(component_id='btnShowWorld', component_property='n_clicks_timestamp'),

    [Input(component_id = 'Slider', component_property = 'value'),
    Input(component_id = 'Prod_1', component_property = 'n_clicks_timestamp'),
    Input(component_id = 'Cons_1', component_property = 'n_clicks_timestamp'),
    Input(component_id = 'Button_for_Normalize', component_property = 'n_clicks'),
    Input(component_id = 'Button_for_Sorting', component_property = 'n_clicks'),
    Input(component_id = 'interval_slider', component_property = 'value'),
    Input(component_id ='world_plot',component_property = 'clickData'),
    Input(component_id='btnShowWorld', component_property='n_clicks_timestamp'),
    ])
def update_graph(selected_year,Timestamp_Button_Prod,Timestamp_Button_Con, sort_button_value,sort_button2_value,value_bar,c_selection, btnShowWorld):
    dff = df.copy()
    dff = dff[dff["Year"]==selected_year]
    
########################################################################################################################################################
    ############## 
    
    # initialize Timestamps if they're not clicked yet

    if Timestamp_Button_Con is None:
        Timestamp_Button_Con = 0
    if Timestamp_Button_Prod is None:
        Timestamp_Button_Prod= 0

    # list_1 = production
    tab_string = "Electricity production (TWh)"
    header_barplot_2_2_string = "Total electricity "

    header = [html.H3(tab_string)]
    #header_barplot_2_2 = [html.H3(header_barplot_2_2_string)]
    
    # determine which button was clicked last by comparing timestamps
    if Timestamp_Button_Prod<Timestamp_Button_Con:
        # list_1 = consumption
        tab_string = "Domestic electricity consumption (TWh)"
        header_barplot_2_2_string += 'consumption '
        header = [html.H3(tab_string)]

    if Timestamp_Button_Prod >= Timestamp_Button_Con:
        # list_1 = production 
        tab_string = "Electricity production (TWh)"
        header_barplot_2_2_string += 'production '
        header = [html.H3(tab_string)]
        
    # Absolute or relative
    if sort_button_value%2:
        the_column = f"{tab_string}_div_pop"
        button2_text = "Per 10000-Capita"
    else: 
        button2_text = "Absolute"
        the_column = tab_string

    # Largest / Smallest Button
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

        hover_name='Country',
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
                            colorbar_title_side = "right",
                            colorbar_orientation = "v",
                            colorbar_ticks = "inside")

    fig.update(layout_showlegend=False,layout_coloraxis_showscale = False)



    #horizontal barplot
    bar_hor = px.bar(dfff, 
                x=the_column, 
                y="Country", orientation='h',
                barmode = "group",
                color=dfff[the_column],
                color_continuous_scale='Darkmint',
                range_color=(round(dfff.iloc[9][the_column]), round(dfff.iloc[0][the_column])),
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
            yaxis=dict(title="TWh"))

    if btnShowWorld is not None:
        c_selection = None

    if c_selection is not None:
        
        location = c_selection['points'][0]['location']
        cs_name = dff[dff.iso_a3 == location]["Country"].to_list()[0]

        figure1 = bar_plot_cs(df,value_bar,cs_name,tab_string)
        header_barplot_2_2_string += 'of ' + cs_name
        header_barplot_2_2 = [html.P(header_barplot_2_2_string)] 
        
        return header, button_text , button2_text, fig, bar_hor, figure1, header_barplot_2_2, None 
    else:
        # fig2 =  fig2
        header_barplot_2_2_string += 'per continent'
        header_barplot_2_2 = [html.P(header_barplot_2_2_string)] 
        return header, button_text , button2_text, fig, bar_hor, fig2, header_barplot_2_2, None 