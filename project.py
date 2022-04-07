import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go


from dash import Dash, dcc, html, Input, Output 

app = Dash(__name__)
# ---------------------------------------------------------------------------------
# Data cleaning
file = pd.ExcelFile("Dataset1.xlsx")

file_dict = {key:i for i, key in enumerate(file.sheet_names)}
sheet21 = pd.read_excel(file,file_dict['Share of renewables in electri'])



#-------------------------------------------------------------------------------------
# Building the graphs 

# GRAPH 1 - ELECTRICITY
dfElectricity = pd.read_csv('Data-Visualization/electricity.csv')
country_list = ['Portugal', 'Romania', 'Spain', 'Sweden', 'United Kingdom']

options1 = [{'label': 'Portugal', 'value': 'Portugal'},
           {'label': 'Romania', 'value': 'Romania'},
           {'label': 'Spain', 'value': 'Spain'}, 
           {'label': 'Sweden', 'value': 'Sweden'}, 
           {'label': 'United Kingdom', 'value': 'United Kingdom'}]

# GRAPH 2 - 

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("First Test for DV", style={'text-align': 'center'}),

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

    html.H3("Electricity shit", style={'text-align': 'center'}),
    html.Br(),
    html.Label('Choose a Country:'),
    dcc.Dropdown(
        id='drop1',
        options=options1,
        value='Portugal'
    ),

    dcc.Graph(
        id='electricity_graph'
    ),

    html.Br()

    ])

# ------------------------------------------------------------------------------
# Connect Dash-Components to Data
@app.callback(
    Output('output_container_slider', 'children'),
    Input('my_slider', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)



@app.callback(
    Output(component_id='electricity_graph', component_property='figure'),
    [Input(component_id='drop1', component_property='value')]
)
def callback_1(input_value):
    data1 = [dict(type='scatter',
                x=dfElectricity.index,
                y=dfElectricity[country],
                name=country)
                                for country in country_list]
    layout1 = dict(title=dict(
                            text='Electricity emissions of 5 countries between 1990-2020'
                    ),
                    xaxis=dict(title='Years'),
                    yaxis=dict(title='Electricity Emissions'))
    return go.Figure(data=data1, layout=layout1)




if __name__ == '__main__':
    app.run_server(debug=True)