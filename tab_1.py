from re import A
from dash import dcc, html, Input, Output, callback, callback_context
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly
import plotly.graph_objects as go


#pip install geojson
import geojson


# ---------------------------------------------------------------------------------
# Data import and cleaning

df = pd.read_csv('ActualDataset.csv')

        ### Consumption ###
tab_string = 'Total energy consumption (Mtoe)'
df[f"{tab_string}_div_pop"] = (df[tab_string]/df["pop_est"])*10000

        ### Production ###
tab_string = 'Total energy production (Mtoe)'
df[f"{tab_string}_div_pop"] = (df[tab_string]/df["pop_est"])*10000

last = 'Total energy consumption (Mtoe)'

with open("geojson11.geojson") as f:
    gj = geojson.load(f)

### Lists for lower Graphs
consumption = ['Oil products domestic consumption (Mt)','Natural gas domestic consumption (bcm)',
                'Coal and lignite domestic consumption (Mt)','Electricity domestic consumption (TWh)']

production = ['Refined oil products production (Mt)','Natural gas production (bcm)',
                'Coal and lignite production (Mt)','Electricity production (TWh)']

# Accesstoken for Mapbox-API
plotly.express.set_mapbox_access_token("pk.eyJ1IjoibWFzaGF5ZWtoaTE4IiwiYSI6ImNsMXBkaXpveTE4eGIzY28yY2h2bDR0aWQifQ.4BeYsKCaxz8Mzg1A1C0LrA")


# country list for dropdown 
countries = []
for country in df['Country'].unique():
    countries.append({'label':str(country),'value':country})


# ---------------------------------------------------------------------------------
# Layout of this tab

layout = html.Div([

    html.Div(children = [
        html.Div([
            html.Button("Production",id='Production'),
            html.Button("Consumption",id='Consumption'),
            ])
            ]),
    html.Div(html.H3(tab_string),
        id='ticker_header'
    )
    ,
    html.Div(children = [
        html.Div([
            html.Button(id='buttonPlay', children='Play'),
            html.Button(id='buttonPause', children='Pause'),
            html.Button(id='buttonReset', children='Reset'),
            dcc.Interval(id='interval-component', interval=1500, n_intervals=0)], style={'width': '15%', 'display': 'inline-block'}),
        html.Div([
            dcc.Slider(id='my_slider', min = 1990, max = 2020, step = 1, value=1990, 
                    marks = {1990: '1990', 1995: '1995', 2000: '2000', 2005: '2005', 2010: '2010', 2015: '2015', 2020: '2020'},
                    tooltip={"placement": "bottom", "always_visible": True},
                    #updatemode='drag'
                    )], style={'width': '75%', 'display': 'inline-block'}),
        html.Br(),
        html.Br(),
        html.Button('Largest', id='sort_button', n_clicks=0),
        html.Button('Related to Population', id='Normalized', n_clicks=0,style={"float":"right"})],
    ),
    html.Div(children=[
                    dcc.Graph(id="bar_hor_1", style={'display': 'inline-block','width': '34%'}),
                    dcc.Graph(id="world", style={'display': 'inline-block','width': '64%'}),
                    ]),
    html.Br(),
    html.Br(),

    ########################### CONSUMPTION ######################x
   # html.H3('Total energy consumption (Mtoe)'),
    html.Br(),
    html.Div([dcc.Slider(id='simple_slider',
                min = 1990, 
                max = 2020, 
                step = 1, 
                value=1990,  
                marks = None,
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode='drag',
                
                )],style={'width': '30%',"float":"right"}),

    html.Div(children= [
        html.Div([dcc.RangeSlider(id="range_slider",
                    min=1990,
                    max=2020,
                    value=[1995, 2015   ],
                    step = 1,
                    className="dcc_control",
                    marks = None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode='drag')],
                    style={'width': '70%', 'display': 'inline-block'}),

        
        dcc.Dropdown(
        options= countries,
        value='Portugal',
        id='country_dropdown',
        style={"width": "30%",'display': 'inline-block', "float": "right"}
        ),

    ]),
   
    
    html.Br(),
    html.Br(),
    html.Div(children= [
        dcc.Graph(id='bar_chart_2', style={"width": "70%",'display': 'inline-block'}),
        dcc.Graph(id='circle_graph', style={"width": "30%",'display': 'inline-block'})]),
    html.Br(),
    
    html.Br(),

    

    html.Br(),

    

    
    
])

# ------------------------------------------------------------------------------
# Callbacks of this tab

@callback([
    Output(component_id='interval-component', component_property='disabled'),
    Output(component_id='buttonPlay', component_property='n_clicks'), 
    Output(component_id='buttonPause', component_property='n_clicks'),
    #Output(component_id='msg-container', component_property='children')
    ],
    [Input(component_id='buttonPlay', component_property='n_clicks'),
    Input(component_id='buttonPause', component_property='n_clicks'),
    Input(component_id='buttonReset', component_property='n_clicks'),
    Input('my_slider', 'value'),
    Input('my_slider', 'drag_value'),
    ]
)
def enable_interval_update(buttonPlay, buttonPause, buttonReset, stepper, dragValue):
    #msg = 'play: {}, pause: {}, reset: {}, stepper: {}, drag: {}'.format(buttonPlay, buttonPause, buttonReset, stepper, dragValue)
    if not buttonPlay:
        buttonPlay = 0
    if not buttonPause:
        buttonPause = 0

    if buttonPlay > buttonPause:
        return False, 1, 0#, msg 
    
    else:
        return True, 0, 0#, msg


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

    Output(component_id = 'ticker_header', component_property = 'children')


    ],
    [Input(component_id = 'my_slider', component_property = 'value'),
    Input(component_id = 'Normalized', component_property = 'n_clicks'),
    Input(component_id = 'sort_button', component_property = 'n_clicks'),
    Input(component_id = 'Production', component_property = 'n_clicks_timestamp'),
    Input(component_id = 'Consumption', component_property = 'n_clicks_timestamp'),
    Input(component_id ='country_dropdown', component_property = 'value'),
    Input(component_id ='simple_slider', component_property = 'value'),
    Input(component_id = 'range_slider', component_property = 'value'),
    Input(component_id = 'ticker_header', component_property = 'children')
    ])

def All_Graphs(selected_year,sort_button_value,sort_button2_value, Prod_Time_Button, Con_Time_Button, country_dropdown, value_pie, value_bar,header_value):
    dff = df.copy()
    dff = dff[dff["Year"]==selected_year]
    
########################################################################################################################################################
    ############## 

    # Normalize Button
        # Production or Consumption
    
    # initialize Timestamps if they're not clicked yet

    if Con_Time_Button is None:
        Con_Time_Button = 0
    if Prod_Time_Button is None:
        Prod_Time_Button = 0

    list_1 = production
    tab_string = 'Total energy production (Mtoe)'

    header = [html.H3(tab_string)]
    
### determine which button was clicked last by comparing timestamps
    if Prod_Time_Button<Con_Time_Button:
        list_1 = consumption
        tab_string = 'Total energy consumption (Mtoe)'
        header = [html.H3(tab_string)]

    if Prod_Time_Button > Con_Time_Button:
        list_1 = production 
        tab_string = 'Total energy production (Mtoe)'
    
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

    
     ########################################################################################################################################
    #PieChart
 
  
    labels_dict ={list_1[0]: 'Oil',
           list_1[1]: 'Gas',
           list_1[2]: 'Coal', 
           list_1[3]: 'Electricity'}


    dff2 = df.copy()
    dff2 = dff2[dff2['Year'] == value_pie]
    dff2 = dff2[dff2['Country'] == country_dropdown]
    dff2 = dff2[list_1]

    piechart=px.pie(
                data_frame=dff2,
                values = dff2.values.tolist()[0],
                names= list(labels_dict.values()),
                hole=.8,
            color_discrete_sequence = px.colors.qualitative.Antique)
    piechart.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },margin={'r':10,'t':0,'l':0,'b':0},legend=dict(yanchor="top", y=0.6, xanchor="left", x=0.40))


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

    return fig, bar_hor, button_text , button2_text, piechart, fig2 , header


#circle graph of total consumption of all features by country

    ######################### COPMARISON GRAPHS #####################



