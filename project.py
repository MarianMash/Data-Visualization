import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)


from dash import Dash, dcc, html, Input, Output 

app = Dash(__name__)
# ---------------------------------------------------------------------------------
# Data cleaning
file = pd.ExcelFile("/Users/masha/Desktop/NOVA/Data Visualization/Project/Dataset1.xlsx")
#file = pd.ExcelFile("Enerdata_Energy_Statistical_Yearbook_2021.xlsx")

file_dict = {key:i for i, key in enumerate(file.sheet_names)}
sheet21 = pd.read_excel(file,file_dict['Share of renewables in electri'])


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
    ])

# ------------------------------------------------------------------------------
# Connect Dash-Components to Data
@app.callback(
    Output('output_container_slider', 'children'),
    Input('my_slider', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)