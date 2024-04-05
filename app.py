import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from src import data_wrangling


df = data_wrangling.main()
# pd.read_csv('data/processed/merged_data_with_inflation.csv')

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the figure for the global map view
fig_map = px.choropleth(
    df,
    locations="country",
    locationmode="country names",
    color="bigmacs_per_hour",
    hover_name="country",
    hover_data={"year": True, "bigmacs_per_hour": True, "Dollar price": True},
    projection="natural earth",
    title="Global Big Macs per Hour",
    color_continuous_scale=px.colors.sequential.Plasma,
)

fig_map.update_geos(showcountries=True, countrycolor="RebeccaPurple")

fig_map.update_layout(coloraxis_colorbar={"title": "Big Macs/hr"})


# Text field
def drawText(text):
    return html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.H5(text),
                            ],
                            style={"textAlign": "center"},
                        )
                    ]
                )
            ),
        ]
    )


def year_slider():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5("Year Range"),
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
                "margin-left": "5rem",
                # "margin-right": "2rem",
                "padding": "2rem 1rem",
            },
        ),
        color="light",
        outline=True,
    )


def country_dropdown():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5("Country"),
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
                # "margin-left": "2rem",
                # "margin-right": "5rem",
                "padding": "2rem 1rem",
            },
        ),
        color="light",
        outline=True,
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
            # "margin-left": "2rem",
            "margin-right": "2rem",
            "padding": "2rem 0rem",
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
            "margin-left": "2rem",
            # "margin-right": "0rem",
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
                        html.Div(
                            html.H5("How many Bic Mac can we buy?"),
                            # style={"textAlign": "center"},
                        ),
                        # html.Div(id="big-mac-index-metric"),
                        # html.Div(id="local-currency-metric"),
                        # Buying Power Calculator (Will be updated with callback)
                        dcc.Graph(id="buying-power-plot"),
                    ],
                )
            ],
            style={
                "margin-left": "5rem",
                "margin-right": "2rem",
                # "padding": "2rem 1rem",
            },
        ),
        color="light",
        outline=True,
    )


def global_map():
    return dbc.Card(
        dbc.CardBody(
            [dcc.Graph(id="global-map", figure=fig_map)],
            style={
                "margin-left": "2rem",
                "margin-right": "5rem",
                # "padding": "2rem 1rem",
            },
        ),
        color="light",
        outline=True,
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
            style={
                "margin-left": "5rem",
                "margin-right": "2rem",
                "padding": "2rem 1rem",
            },
        ),
        color="light",
        outline=True,
    )


def minimum_wage_trend_plot():
    return dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(
                    id="minimum-wage-trend",
                )
            ],
            style={
                "margin-left": "2rem",
                "margin-right": "5rem",
                "padding": "2rem 1rem",
            },
        ),
        color="light",
        outline=True,
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
            "margin-top": "14px",
            "margin-bottom": "0px",
            "font-size": "13px",
            "opacity": "0.6",
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
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        [
                                                            html.H2(
                                                                "Big Mac Index Dashboard",
                                                                style={"textAlign": "center"},
                                                            ),
                                                            html.P(
                                                                """
                                                                Inflation measurements within this dashboard derive from variations in Big Mac prices, rather than the Consumer Price Index (CPI). 
                                                                The concept of buying power is visualized through 'Big Macs per hour'—the number of Big Macs one can purchase with an hour's wage. 
                                                                This unique approach offers an insightful perspective on economic conditions across different countries.
                                                                """,
                                                                style={'marginTop': '10px', 'textAlign': 'center'}  # Ensuring the text is centered and has some space above
                                                            ),
                                                        ],
                                                    )
                                                ]
                                            )
                                        ),
                                    ]
                                )
                            )
                        ]
                    ),
                    # Filter
                    dbc.Row(
                        [
                            dbc.Col(year_slider(), width=5),
                            dbc.Col(country_dropdown(), width=2),
                            dbc.Col(inflation_control(), width=3),
                            dbc.Col(currency_control(), width=2),
                        ]
                    ),
                    # World map & Key Metrics
                    dbc.Row(
                        [
                            dbc.Col(key_metrics(), width=4),
                            dbc.Col(global_map(), width=8),
                        ]
                    ),
                    # Time Series Plots for Big Mac Price Trend and Minimum Wage Trend
                    dbc.Row(
                        [
                            dbc.Col(time_series_plot(), width=6),
                            dbc.Col(
                                minimum_wage_trend_plot(),
                                width=6,
                            ),
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
        title=f"Buying Power Over Time in {selected_country}",
        width=400,
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
        wage = "Adjusted local wage"
        y_data = "Local price"

    elif (inflation == "adjust") & (currency == "USD"):
        wage = "Adjusted UDS wage"
        y_data = "Dollar price"

    elif (inflation == "absolute") & (currency == "local"):
        wage = "Local wage"
        y_data = "Local price"

    else:  #  (inflation == "absolute") & (currency == "USD")
        wage = "USD wage"
        y_data = "Dollar price"

    fig = px.line(
        filtered_data,
        x="year",
        y=[y_data, wage],
        labels={
                "year": "Year",
                "value": "Value",
                 },
        title=f"Big Mac Price and Minimum Wage Trends in {selected_country}",
    )

    return fig


@app.callback(
    Output("minimum-wage-trend", "figure"),
    [Input("country-dropdown", "value"), Input("year-slider", "value")],
)
def update_minimum_wage_trend(selected_country, selected_year):
    filtered_data = df[
        (df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])
    ]

    if filtered_data.empty:
        return go.Figure()

    fig = go.Figure()

    # Add a bar for each country
    for country in filtered_data["country"].unique():
        fig.add_trace(
            go.Bar(
                x=[country],
                y=filtered_data[filtered_data["country"] == country]["USD wage"],
                name=country,
                marker_color="lightslategray"
                if country != selected_country
                else "crimson",  # Highlight selected country
            )
        )

    # Update the layout
    fig.update_layout(
        title=f"Hourly Wage (USD) between {selected_year[0]} and {selected_year[1]}",
        xaxis_title="Country",
        yaxis_title="Hourly Wage (USD)",
        xaxis={"categoryorder": "total descending"},
        margin={"l": 40, "b": 40, "t": 40, "r": 0},
        hovermode="closest",
    )

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1")
