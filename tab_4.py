from dash import dcc, html, Input, Output, State, callback
import pandas as pd
import plotly.express as px
import plotly

#pip install geojson
import geojson


# ---------------------------------------------------------------------------------
# Data import and cleaning

# df = pd.read_csv('ActualDataset.csv')

# with open("geojson11.geojson") as f:
#     gj = geojson.load(f)


# Accesstoken for Mapbox-API
# plotly.express.set_mapbox_access_token("pk.eyJ1IjoibWFzaGF5ZWtoaTE4IiwiYSI6ImNsMXBkaXpveTE4eGIzY28yY2h2bDR0aWQifQ.4BeYsKCaxz8Mzg1A1C0LrA")

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)
years = list(set(df["year"]))
years.sort()
# ---------------------------------------------------------------------------------
# Layout of this tab
def make_fig(year):
    return px.scatter(
        df[df.year == year],
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=55,
    )

layout = html.Div(
    [
        dcc.Interval(id="animate", disabled=True),
        dcc.Graph(id="graph-with-slider", figure=make_fig(1952)),
        dcc.Slider(
            id="year-slider",
            min=df["year"].min(),
            max=df["year"].max(),
            value=df["year"].min(),
            marks={str(year): str(year) for year in df["year"].unique()},
            step=None,
        ),
        html.Button("Play", id="play"),
    ]
)



# ------------------------------------------------------------------------------
# Callbacks of this tab

@callback(
    Output("graph-with-slider", "figure"),
    Output("year-slider", "value"),
    Input("animate", "n_intervals"),
    State("year-slider", "value"),
    prevent_initial_call=True,
)
def update_figure(n, selected_year):
    index = years.index(selected_year)
    index = (index + 1) % len(years)
    year = years[index]
    return make_fig(year), year


@callback(
    Output("animate", "disabled"),
    Input("play", "n_clicks"),
    State("animate", "disabled"),
)
def toggle(n, playing):
    if n:
        return not playing
    return playing