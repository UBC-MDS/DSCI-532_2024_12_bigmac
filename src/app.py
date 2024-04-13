import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_vega_components as dvc

import pandas as pd
import plotly.express as px
from datetime import datetime
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import data_wrangling
import geopandas as gpd
import altair as alt
alt.data_transformers.enable('vegafusion')

df = data_wrangling.main()
# pd.read_csv('data/processed/merged_data_with_inflation.csv')

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Text field

def year_slider():
    return dbc.Container(
            [
                html.H6("Year Range"),
                html.Div(
                    dcc.RangeSlider(
                        id="year-slider",
                        min=df["year"].min(),
                        max=df["year"].max(),
                        value=[
                            df["year"].min(),
                            df["year"].max(),
                        ],
                        # marks={str(year): str(year) for year in df["year"].unique()},
                        marks={
                            (str(year)): (str(year) if year % 3 == 1 else " ")
                            for year in df["year"].unique()
                        },
                        step=None,
                    )
                ),
            ],
            style={
                "margin-left": "-4rem",
                # "margin-right": "2rem",
                "padding": "2rem 1rem",
            },
    )

def country_dropdown():
    return dbc.Container(
            [
                html.H6("Country"),
                html.Div(
                    dcc.Dropdown(
                        id="country-dropdown",
                        options=[
                            {"label": i, "value": i} for i in df["country"].unique()
                        ],
                        value="United States",
                    ),
                ),
            ],
            style={
                "margin-left": "-6rem",
                "margin-right": "7rem",
                "padding": "2rem 1rem",
            },
    )


def inflation_control():
    return html.Div(
        [
            html.H6("Inflation Adjustment for Hourly Wage: "),
            # html.Br(),
            dcc.RadioItems(
                id="inflation-adjustment-toggle",
                options=[
                    {
                        "label": "Adjust for Inflation",
                        "value": "adjust",
                    },
                    {
                        "label": "Using Absolute Value",
                        "value": "absolute",
                    },
                ],
                value="absolute",
                # inline=True,
                inputStyle={"margin-right": "10px"},
            ),
        ],
        style={
            "margin-left": "10rem",
            "margin-right": "2rem",
            "padding": "2rem 0rem",
        },
    )

def currency_control():
    return html.Div(
        [
            html.H6("Currency: "),
            # html.Br(),
            dcc.RadioItems(
                id="currency-conversion-option",
                options=[
                    {
                        "label": "Local Currency",
                        "value": "local",
                    },
                    {"label": "USD", "value": "USD"},
                ],
                value="USD",
                # inline=True,
                inputStyle={"margin-right": "10px"},
            ),
        ],
        style={
            "margin-left": "3rem",
            "margin-right": "2rem",
            "padding": "2rem 0rem",
        },
    )


def key_metrics():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    id="key-metrics",
                    children=[
                        # html.Div(
                        #     html.H5("How many Bic Mac can we buy?"),
                        # ),
                        # html.Div(id="big-mac-index-metric"),
                        # html.Div(id="local-currency-metric"),
                        # Buying Power Calculator (Will be updated with callback)
                        dcc.Graph(id="buying-power-plot"),
                        dcc.Graph(id="minimum-wage-trend"),
                    ],
                )
            ],
            
        ),
        color="light",
        outline=True,
        style={
                "height":850,
                "margin-left": "5rem",
                "margin-right": "1rem",
                "margin-bottom": "2rem",
                # "padding": "2rem 1rem",
            },
    )


def global_map():
    # Define the figure for the global map view
    return dbc.Card(
        dbc.CardBody(
            [   html.Br(), 
                dvc.Vega(id='global-map', spec={})
                ],
            
        ),
        color="light",
        outline=True,
        style={
                "height":850,
                # "margin-left": "1rem",
                "margin-right": "5rem",
                "margin-bottom": "2rem",
                # "padding": "2rem 1rem",
            },
    )


def time_series_plot():
    return dbc.Card(
        dbc.CardBody(
            [
                # dbc.Row(
                #     [
                #         dbc.Col(inflation_control(), width=8),
                #         dbc.Col(currency_control(), width=4),
                #     ]
                # ),
                dcc.Graph(
                    id="time-series-plot",
                    # style={"display": "inline-block"},
                ),
            ],
            
        ),
        color="light",
        outline=True,
        style={
                "margin-left": "5rem",
                "margin-right": "1rem",
                "margin-bottom": "2rem",
            },
    )


def minimum_wage_trend_plot():
    return dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(
                    id="minimum-wage-trend",
                )
            ]
        ),
        color="light",
        outline=True,
        style={
                "margin-left": "1rem",
                "margin-right": "5rem",
                "margin-bottom": "2rem",
            },
    )


def footer():
    return html.Footer(
        [
            html.P(
                "The Big Mac Dashboard provides interactive visual insights into the purchasing power parity (PPP) and economic trends across the globe using the Big Mac Index and minimum wage data."
            ),
            html.P(
                [
                    "Authors: Arturo Boquin, Atabak Alishiri, Beth Ou Yang, Nicole Tu",
                    html.Br(),
                    html.A(
                        "Github Repo",
                        href="https://github.com/UBC-MDS/DSCI-532_2024_12_bigmac",
                        target="_blank",
                    ),
                ]
            ),
        ],
        style={
            "width": "100%",
            "bottom":"0",
            "text-align": "center",
            "margin-top": "14px",
            "margin-bottom": "0px",
            "font-size": "13px",
            "opacity": "0.6",
            "background-color": "#EBEBEB",
            "color":"#2a3f5f",
        },
    )


app.layout = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    # Header
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                                    dbc.Container(
                                                        [
                                                            html.H2(
                                                                "Big Mac Index Dashboard",
                                                                style={
                                                                        "textAlign": "center", 
                                                                       "color": "#2a3f5f",                                                                       },
                                                            ),
                                                            html.P(
                                                                """
                                                                Inflation measurements within this dashboard derive from variations in Big Mac prices, rather than the Consumer Price Index (CPI). 
                                                                The concept of buying power is visualized through 'Big Macs per hour'—the number of Big Macs one can purchase with an hour's wage. 
                                                                This unique approach offers an insightful perspective on economic conditions across different countries.
                                                                """,
                                                                style={
                                                                    'marginTop': '10px', 
                                                                    'textAlign': 'center',
                                                                     "color": "#2a3f5f"
                                                                    }  # Ensuring the text is centered and has some space above
                                                            ),
                                                            html.Hr()
                                                        ],
                                                    )
                                    ]
                                )
                            )
                        ]
                    ),
                    # Filter
                    dbc.Row(
                        [
                            dbc.Col(year_slider(), width=5),
                            dbc.Col(country_dropdown(), width=3),
                            # dbc.Col(inflation_control(), width=3),
                            # dbc.Col(currency_control(), width=2),
                        ],
                        justify="center",
                        style={"background-color": "#f3f6fa"}
                    ),
                    # World map & Key Metrics
                    dbc.Row(
                        [
                            dbc.Col(key_metrics(), width=6),
                            dbc.Col(global_map(), width=6),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(inflation_control(), width=5),
                            dbc.Col(currency_control(), width=5),
                        ],
                        justify="center",
                        style={"background-color": "#f3f6fa"}
                    ),
                    # Time Series Plots for Big Mac Price Trend and Minimum Wage Trend
                    dbc.Row(
                        [
                            dbc.Col(time_series_plot(), width=12),
                            # dbc.Col(
                            #     minimum_wage_trend_plot(),
                            #     width=6,
                            # ),
                        ]
                    ),
                    footer(),
                ]
            ),
            # color="light",
        )
    ]
)

@app.callback(
    Output("global-map", "spec"),
    [Input("year-slider", "value"), Input("country-dropdown", "value")]
)
def update_global_map(selected_year, selected_country):
    filtered_data = df[
        (df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])
    ].groupby(['country_code', 'country'])[['bigmacs_per_hour']].mean().reset_index()

    shapefile = 'data/raw/world-administrative-boundaries/world-administrative-boundaries.shp'
    gdf = gpd.read_file(shapefile)
    gdf.crs = 'EPSG:4326'

    df_map = gdf[['iso3', 'geometry']].merge(filtered_data, right_on='country_code', left_on='iso3', how='left'
                                             ).rename({'bigmacs_per_hour': 'Big Macs per Hour'}, axis=1)
    
    background = alt.Chart(df_map).mark_geoshape(color="lightgrey")
    chart_map = background + alt.Chart(df_map, width=600, height=600).mark_geoshape().encode(
            color=alt.Color('Big Macs per Hour', legend=alt.Legend(orient='bottom-right')),
            tooltip=['country', 'Big Macs per Hour']
        ).properties(height=600)

    highlight = chart_map + alt.Chart(df_map).mark_geoshape(
        fill=None,
        stroke='red',
        strokeWidth=0.5
    ).transform_filter(
        alt.FieldEqualPredicate(field='country', equal=selected_country)
    )
    
    return (highlight).to_dict(format="vega")



@app.callback(
    Output("buying-power-plot", "figure"),
    [
        Input("country-dropdown", "value"),
        Input("year-slider", "value"),
    ],
)
def update_buying_power_plot(selected_country, selected_year):
    filtered_data = df[
        (df["country"] == selected_country)
        & (df["year"] >= selected_year[0])
        & (df["year"] <= selected_year[1])
    ]

    if filtered_data.empty:
        return go.Figure()

    # line plot for buying power over time
    fig = px.line(
        filtered_data,
        x="year",
        y="bigmacs_per_hour",
        title=f"How many Bic Mac can we buy in {selected_country}?",
        # width=600,
        height=400,
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Big Macs per Hour",
        # margin={"l": 40, "b": 40, "t": 40, "r": 0},
        hovermode="closest",
    )

    fig.update_traces(line=dict(color="RoyalBlue"))

    return fig


@app.callback(
    Output("minimum-wage-trend", "figure"),
    [Input("country-dropdown", "value"), Input("year-slider", "value")],
)
def update_minimum_wage_trend(selected_country, selected_year):
    filtered_data = df[
        (df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])
    ].groupby(['country'])[['Wage in USD']].median().reset_index()

    if filtered_data.empty:
        return go.Figure()

    fig = go.Figure()

    # Add a bar for each country
    for country in filtered_data["country"].unique():
        fig.add_trace(
            go.Bar(
                x=[country],
                y=filtered_data[filtered_data["country"] == country]["Wage in USD"],
                name=country,
                marker_color="lightslategray"
                if country != selected_country
                else "crimson",  # Highlight selected country
            )
        )

    # Update the layout
    fig.update_layout(
        title=f"Median Hourly Wage from {selected_year[0]} to {selected_year[1]}",
        xaxis_title="Country",
        yaxis_title="Hourly Wage (USD)",
        xaxis={"categoryorder": "total descending"},
        # margin={"l": 40, "b": 40, "t": 40, "r": 0},
        hovermode="closest",
        height=400,
    )

    return fig

# Callback to update the time series plot
@app.callback(
    Output("time-series-plot", "figure"),
    [
        Input("country-dropdown", "value"),
        Input("year-slider", "value"),
        Input("inflation-adjustment-toggle", "value"),
        Input("currency-conversion-option", "value"),
    ],
)
def update_time_series(selected_country, selected_year, inflation, currency):
    filtered_data = df[
        (df["country"] == selected_country)
        & (df["year"] >= selected_year[0])
        & (df["year"] <= selected_year[1])
    ]

    if (inflation == "adjust") & (currency == "local"):
        wage = "Adjusted Wage in Local Currency"
        y_data = "Bigmac Price in Local Currency"

    elif (inflation == "adjust") & (currency == "USD"):
        wage = "Adjusted Wage in USD"
        y_data = "Bigmac Price in USD"

    elif (inflation == "absolute") & (currency == "local"):
        wage = "Wage in Local Currency"
        y_data = "Bigmac Price in Local Currency"

    else:  #  (inflation == "absolute") & (currency == "USD")
        wage = "Wage in USD"
        y_data = "Bigmac Price in USD"

    fig = px.line(
        filtered_data,
        x="year",
        y=[y_data, wage],
        labels={
                "year": "Year",
                 },
        title=f"Big Mac Price and Minimum Wage Trends in {selected_country}",
    ).update_yaxes(visible=False)

    return fig



# Run the app
if __name__ == "__main__":
    app.run_server(debug=False, host="127.0.0.1")
