from multiprocessing.sharedctypes import Value
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)


from dash import Dash, dcc, html, Input, Output 

app = Dash(__name__)
# ---------------------------------------------------------------------------------
# Data cleaning
file = pd.ExcelFile("Dataset1.xlsx")

file_dict = {key:i for i, key in enumerate(file.sheet_names)}
sheet1 = pd.read_excel(file,file_dict['Total energy production'])


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

    dcc.Graph(id='my_bar_chart', figure={})

    ])

# ------------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container_slider', component_property='children'),
     Output(component_id='my_bar_chart', component_property='figure')],
    [Input(component_id='my_slider', component_property='value')]
)
def update_graph(value):

    container = 'You have selected "{}"'.format(value)

    dff = sheet1.copy()
    dff = dff[["Total energy production (Mtoe)",value]]

    # Plotly Express
    fig = px.bar(dff, x='Total energy production (Mtoe)', y=value)
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