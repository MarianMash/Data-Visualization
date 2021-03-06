from pydoc import classname
from re import A, template
from turtle import width
from dash import dcc, html, Input, Output, callback, callback_context
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.io as pio

#pip install geojson
import geojson

# ---------------------------------------------------------------------------------##
# Data import and cleaning

df = pd.read_csv('Merged_Energy_Dataset.csv')

# Consumption
tab_string = "Total consumption of Energy (Twh)"
df[f"{tab_string}_div_pop"] = (df[tab_string]/df["pop_est"])*10000

# Production
tab_string = "Total production of Energy (Twh)"
df[f"{tab_string}_div_pop"] = (df[tab_string]/df["pop_est"])*10000


# headers for the barchart and piechart of the second row 
header_barplot_2_string = "Total energy "
header_pieplot_2_string = "Total energy "

with open("geojson11.geojson") as f:
    gj = geojson.load(f)

# Lists for lower Graphs
consumption = ['Oil products domestic consumption (Mt)','Natural gas domestic consumption (bcm)',
                'Coal and lignite domestic consumption (Mt)','Domestic electricity consumption (TWh)']



production = ['Refined oil products production (Mt)','Natural gas production (bcm)',
                'Coal and lignite production (Mt)','Electricity production (TWh)']
            
##### Some Helper Functions #####
def bar_plot_cs(df, value, location,tab_string):
    df_cs = df.copy()
    df_cs = df_cs[(df_cs['Year'] >= value[0]) & (df_cs['Year'] <= value[1])]
    df_cs = df_cs[df_cs['Country'] == location]
    df_cs = df_cs[[tab_string,'Year']]

    fig_cs = go.Figure(
            data=[
                go.Bar(
                    name= location,
                    x= df_cs.Year.unique(),
                    y= df_cs[tab_string],
                    marker_color="#004687",
                    opacity=0.8,
                    hovertext= location
                ),
            ]
    )
    fig_cs.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },margin={'r':0,'t':0,'l':10,'b':0},barmode="stack",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="left",
                x=0.3),
            yaxis=dict(title="TWh")
            )
    return fig_cs

def pie_func(df,value_pie,cs_name,list_1): 
    labels_dict ={list_1[0]: 'Oil',
        list_1[1]: 'Gas',
        list_1[2]: 'Coal', 
        list_1[3]: 'Electricity'}

    dff2 = df.copy()
    dff2 = dff2[dff2['Year'] == value_pie]
    
    if cs_name == 1:
        dff3 = dff2.copy()
        dff3 = dff3[list_1]
        dff3 = dff3.fillna(0)
        dff3 = dff3.replace('n.a.', 0)
        dff3[list_1[1]] = pd.to_numeric(dff3[list_1[1]])
        dff3[list_1[2]] = pd.to_numeric(dff3[list_1[2]])
        dff3 = dff3.sum()

        piechart=px.pie(
                data_frame=dff3,
                values = dff3.values.tolist(),
                names= list(labels_dict.values()),
                hole=.8,
            color_discrete_sequence = px.colors.qualitative.Prism)
        piechart.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)",
                "paper_bgcolor": "rgba(0, 0, 0, 0)"},
                margin={'r':10,'t':0,'l':0,'b':0},legend=dict(yanchor="top", y=0.6, xanchor="left", x=0.40))

    else:
        dff2 = dff2[dff2['Country'] == cs_name]
        dff2 = dff2[list_1]

        piechart=px.pie(
                    data_frame=dff2,
                    values = dff2.values.tolist()[0],
                    names= list(labels_dict.values()),
                    hole=.8,
                color_discrete_sequence = px.colors.qualitative.Prism)
        piechart.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)",
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                },margin={'r':10,'t':0,'l':0,'b':0},legend=dict(yanchor="top", y=0.6, xanchor="left", x=0.40))
    return piechart

# Accesstoken for Mapbox-API
plotly.express.set_mapbox_access_token("pk.eyJ1IjoibWFzaGF5ZWtoaTE4IiwiYSI6ImNsMXBkaXpveTE4eGIzY28yY2h2bDR0aWQifQ.4BeYsKCaxz8Mzg1A1C0LrA")

# country list for dropdown 
countries = []
for country in df['Country'].unique():
    countries.append({'label':str(country),'value':country})

# ---------------------------------------------------------------------------------
# Layout of this tab

layout = html.Div([

    html.Div(
            [   
                #Buttons Production-Consumption
                dbc.Row(
                        [
                            dbc.Col([
                                            html.Button("Production",id='Production', className="mx-2 btn btn-info"),
                                            html.Button("Consumption",id='Consumption', className="btn btn-info")
                            ],width=3)
                        ]
                ),
                #Title 
                dbc.Row(
                    [
                        html.Div(html.H3(tab_string),id='ticker_header', className="mx-3 text-lg-center text-light"),
                        dbc.Col([
                            html.Div(html.P("""How much energy do countries across the world consume?
                                        The interactive visualizations show total primary energy production/consumption country by country. It is the sum of all energy sources, including coal, natural gas, crude oil, electricity, and renewable energies.
                                        kWh is a unit of energy equal to one kilowatt of power sustained for one hour, but in this case the measure is 10^9 times a kilowatt."""), className="m-3 text-lg text-light")
                        ],width={'size':8, 'offset':2})
                    ]
                ),
                #Buttons and slider
                dbc.Row(
                    [
                        dbc.Col([
                                
                                html.Button(id='buttonPlay', children='Play', className="m-1 btn btn-success"),
                                html.Button(id='buttonPause', children='Pause', className="m-1 btn btn-success"),
                                html.Button(id='buttonReset', children='Reset', className="m-1 btn btn-success"),
                                ], width=3),
                        dbc.Col([
                                dcc.Interval(id='interval-component', interval=1500, n_intervals=0),
                                dcc.Slider(id='my_slider', min = 1990, max = 2020, step = 1, value=1990, 
                                            marks = {1990: '1990', 1995: '1995', 2000: '2000', 2005: '2005', 2010: '2010', 2015: '2015', 2020: '2020'},
                                            tooltip={"placement": "bottom", "always_visible": True},
                                            )
                        ],width=9)
                    ]
                ),
                #two buttons related to bar and map
                dbc.Row([dbc.Col([
                            html.Button('Largest', id='sort_button', n_clicks=0, className="mb-2 mt-3 btn btn-light"),
                        ],width=2),
                        dbc.Col([],width=8),
                        dbc.Col([
                            html.Button('Related to Population', id='Normalized', n_clicks=0,style={"float":"right"}, className="mb-2 mt-3 btn btn-light")
                        ],width=2)
                ]),
                #Bar chart and map graph
                dbc.Row(
                    [
                        dbc.Col(dbc.Card([dbc.CardHeader("Top 10 countries"),
                                        html.Br(className="mb-6"),
                                        dcc.Graph(id="bar_hor_1"),
                                        html.Br(className="mb-6")],
                                        color="secondary", inverse=True),width=4),
                        dbc.Col(dbc.Card([dbc.CardHeader("World map"),
                                        html.Br(className="mb-6"),
                                        dcc.Graph(id="world"),
                                        html.Br(className="mb-6")],
                                        color="secondary", inverse=True),width=8),
                    ]
                ),
            ]
        ),

    ########################### CONSUMPTION ######################x
    html.P("To display the values of a specific country in the following plots, click on it in the map. To reset the statistics click on the following button"),
    html.A(html.Button(id = 'btnShowWorldT1', children = 'Show World', className="m-1 btn btn-light")),
    html.Div(
    [

        dbc.Row(
            [
                dbc.Col(dbc.Card([dbc.CardHeader(header_barplot_2_string, id='header_barplot_2'
                    #"Total energy production per continent (TWh)"
                    ), 
                                    html.Br(className="mb-6"),
                                    dcc.RangeSlider(id="range_slider",
                                                    min=1990,
                                                    max=2020,
                                                    value=[1995, 2015   ],
                                                    step = 1,
                                                    className="dcc_control",
                                                    marks = None,
                                                    tooltip={"placement": "bottom", "always_visible": True},
                                                    updatemode='drag'),
                                    html.Br(className="mb-6"),
                                dcc.Graph(id='bar_chart_2'),
                                html.Br(className="mb-6")],
                                color="secondary", inverse=True),width=8),
                dbc.Col(dbc.Card([dbc.CardHeader(header_pieplot_2_string, id='header_pieplot_2'
                    #"Total energy production per country and energy type"
                    ),
                                    html.Br(className="mb-6"),
                                    dbc.Row([dcc.Slider(id='simple_slider',
                                                        min = 1990, 
                                                        max = 2020, 
                                                        step = 1, 
                                                        value=1990,  
                                                        marks = None,
                                                        tooltip={"placement": "bottom", "always_visible": True},
                                                        updatemode='drag'),
                                            ]),
                                    html.Br(className="mb-6"),
                                dcc.Graph(id='circle_graph'),
                                html.Br(className="mb-6")],
                                color="secondary", inverse=True),width=4),
            ]
        ),
    ]
)

    
    
], className="m-3")

# ------------------------------------------------------------------------------
# Callbacks of this tab

@callback([
    Output(component_id='interval-component', component_property='disabled'),
    Output(component_id='buttonPlay', component_property='n_clicks'), 
    Output(component_id='buttonPause', component_property='n_clicks'),
    ],
    [Input(component_id='buttonPlay', component_property='n_clicks'),
    Input(component_id='buttonPause', component_property='n_clicks'),
    Input(component_id='buttonReset', component_property='n_clicks'),
    Input('my_slider', 'value'),
    Input('my_slider', 'drag_value'),
    ]
)
def enable_interval_update(buttonPlay, buttonPause, buttonReset, stepper, dragValue):
    
    if not buttonPlay:
        buttonPlay = 0
    if not buttonPause:
        buttonPause = 0

    if buttonPlay > buttonPause:
        return False, 1, 0
    
    else:
        return True, 0, 0


@callback(
    [Output('my_slider', 'value'),
    Output(component_id='buttonReset', component_property='n_clicks'),
    Output('interval-component', 'n_intervals')
    ], 
    [Input('interval-component', 'n_intervals'), 
    Input(component_id='buttonReset', component_property='n_clicks'),
    Input('my_slider', 'drag_value')])
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
    [
    Output(component_id ='world',component_property = 'figure'),
    Output(component_id ='bar_hor_1',component_property = 'figure'),
    Output(component_id = 'sort_button', component_property = 'children'),
    Output(component_id = 'Normalized', component_property = 'children'),
    Output(component_id = 'circle_graph', component_property ='figure'),
    Output(component_id ='bar_chart_2', component_property ='figure'),
    Output(component_id = 'ticker_header', component_property = 'children'),
    Output(component_id='header_barplot_2', component_property='children'),
    Output(component_id='header_pieplot_2', component_property='children'),
    Output(component_id='btnShowWorldT1', component_property='n_clicks_timestamp'),
    ],
    [Input(component_id = 'my_slider', component_property = 'value'),
    Input(component_id = 'Normalized', component_property = 'n_clicks'),
    Input(component_id = 'sort_button', component_property = 'n_clicks'),
    Input(component_id = 'Production', component_property = 'n_clicks_timestamp'),
    Input(component_id = 'Consumption', component_property = 'n_clicks_timestamp'),
    Input(component_id ='simple_slider', component_property = 'value'),
    Input(component_id = 'range_slider', component_property = 'value'),
    Input(component_id = 'ticker_header', component_property = 'children'),
    Input(component_id ='world',component_property = 'clickData'),
    Input(component_id='btnShowWorldT1', component_property='n_clicks_timestamp'),
    ])

def All_Graphs(selected_year,sort_button_value,sort_button2_value, Prod_Time_Button, Con_Time_Button, value_pie, value_bar,header_value,c_selection, btnShowWorld):
    dff = df.copy()
    dff = dff[dff["Year"]==selected_year]
    
    # initialize Timestamps if they're not clicked yet
    if Con_Time_Button is None:
        Con_Time_Button = 0
    if Prod_Time_Button is None:
        Prod_Time_Button = 0

    # initialize generic strings 
    list_1 = production
    tab_string = "Total production of Energy (Twh)"
    header_barplot_2_string = "Total energy "
    header_pieplot_2_string = "Total energy "

    header = [html.H3(tab_string)]
    
    # determine which button was clicked last by comparing timestamps
    if Prod_Time_Button<Con_Time_Button:
        list_1 = consumption
        tab_string = "Total consumption of Energy (Twh)"
        header = [html.H3(tab_string)]
        header_barplot_2_string += 'consumption '
        header_pieplot_2_string += 'consumption '

    if Prod_Time_Button >= Con_Time_Button:
        list_1 = production 
        tab_string = "Total production of Energy (Twh)"    
        header = [html.H3(tab_string)]
        header_barplot_2_string += 'production '
        header_pieplot_2_string += 'production '


    # Absolute or relative
    if sort_button_value%2:
        the_column = f"{tab_string}_div_pop"
        button2_text = "Per 10000-capita"
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
    fig.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },dragmode=False,
    margin={'r':0,'t':0,'l':15,'b':0},
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
            yaxis=dict(title="TWh")
            )

    # show world button 
    if btnShowWorld is not None:
        c_selection = None

    if c_selection is not None:
        
        location = c_selection['points'][0]['location']
        cs_name = dff[dff.iso_a3 == location]["Country"].to_list()[0]

        #create figures
        figure1 = bar_plot_cs(df,value_bar,cs_name,tab_string)
        piechart = pie_func(df,value_pie,cs_name,list_1)

        # generate header string for the barplot
        header_barplot_2_string += 'of ' + cs_name
        header_barplot_2 = [html.P(header_barplot_2_string)]

        #generate header string for the piechart
        header_pieplot_2_string += 'of ' + cs_name + ' per energy type'
        header_pieplot_2 = [html.P(header_pieplot_2_string)]
        
        return fig, bar_hor, button_text , button2_text, piechart, figure1 , header, header_barplot_2, header_pieplot_2, None
    else:
        # fig2 =  fig2
        piechart = pie_func(df,value_pie,1,list_1)

        # generate header string for the barplot
        header_barplot_2_string += 'per continent'
        header_barplot_2 = [html.P(header_barplot_2_string)] 

        #generate header string for the piechart
        header_pieplot_2_string += 'per energy type'
        header_pieplot_2 = [html.P(header_pieplot_2_string)] 

        return fig, bar_hor, button_text , button2_text, piechart, fig2 , header, header_barplot_2, header_pieplot_2, None

