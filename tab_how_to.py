# HERE YOU DO THE IMPORTS NECESSARY FOR THE TAB
from dash import dcc, html, Input, Output, callback

# ---------------------------------------------------------------------------------
# Data import
# HERE YOU IMPORT OR GENERATE ALL THE DATA YOU NEED FOR THE TAB
    
#file = pd.read_csv("ActualDataset.csv")

# ---------------------------------------------------------------------------------
# Layout of this tab

layout = html.Div([
    html.H3('Tab content x'),
    #
    #  INSIDE THIS div YOU PUT THE LAYOUT OF THIS TAB
    #
])

# ------------------------------------------------------------------------------
# Callbacks of this tab
# HERE YOU WRITE THE CALLBACK AND THE FUNCTIONS YOU WILL NEED FOR THIS TAB

@callback(
#     [Output(component_id='my_bar_chart', component_property='figure'),.....],
#     [Input(component_id='my_slider', component_property='value'),......]
)
def function(value):
    ##Some function
    some_output=value
    ######
    return some_output
##
# !!!REMEMBER!!
##
## AFTER GENERATING A NEW TAB YOU HAVE TO ADD IT AS AN IMPORT IN THE app.py
# then, add in the layout section:
#   tabx = tab_x.layout where x is the number of this tab
# add inside app.layout:
#   dcc.Tab(id="tab-x", label='Tab XX', value='tab-x-example')
# finally add:
#       elif tab == 'tab-x-example':
#        return tabx