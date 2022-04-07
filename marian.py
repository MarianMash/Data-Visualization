from multiprocessing.sharedctypes import Value
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash, dcc, html, Input, Output 

# stile for the app 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# ---------------------------------------------------------------------------------
# Data import and cleaning

file = pd.read_excel("Dataset_melted.xlsx")

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.H1("Global energy statistics - DV project", style={'text-align': 'center'}),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
        dcc.Tab(label='Tab three', value='tab-3'),
    ]),
    
    html.Div(id='tabs-content')
    ])
        
    # html.Div([


    # dcc.Slider(id='my_slider',
    #             min = 1990, 
    #             max = 2020, 
    #             step = 1, 
    #             value=1990,  
    #             marks = None,
    #             tooltip={"placement": "bottom", "always_visible": True},
    #             updatemode='drag'),
                
    # html.Div(id='output_container_slider'),
    
    # html.Br(),

    # dcc.Graph(id='my_bar_chart', figure={})

    # ])

# ------------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components
@app.callback(
            [Output(component_id='tabs-content', component_property='children'),
            Output(component_id='output_container_slider', component_property='text'),
            Output(component_id='my_bar_chart', component_property='figure')],
            [Input(component_id='tabs', component_property='value'), #????
            Input(component_id='my_slider', component_property='value')])

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([

            dcc.Slider(id='my_slider',
                min = 1990, 
                max = 2020, 
                step = 1, 
                value=1990,  
                marks = None,
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode='drag'),
                
            html.Div(id='output_container_slider'),
    
            html.Br(),

            dcc.Graph(id='my_bar_chart', figure={})

        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])


# @app.callback(
#     [Output(component_id='output_container_slider', component_property='children'),
#      Output(component_id='my_bar_chart', component_property='figure')],
#     [Input(component_id='my_slider', component_property='value')]
# )
def update_graph(value):

    container = 'You have selected "{}"'.format(value)

    dff = file.copy()
    dff = dff[dff["Year"]==value]
    dff = dff[["Country","Total energy production (Mtoe)","Year"]]

    # Plotly Express
    fig = px.bar(dff, x='Country', y="Total energy production (Mtoe)")
    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)