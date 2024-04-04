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
    hover_data={"year": True, "bigmacs_per_hour": True, "dollar_price": True},
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
                html.Div(
                    dcc.RangeSlider(
                        id="year-slider",
                        min=df["year"].min(),
                        max=df["year"].max(),
                        value=[
                            df["year"].min(),
                            df["year"].max(),
                        ],
                        marks={str(year): str(year) for year in df["year"].unique()},
                        step=None,
                    )
                ),
            ]
        )
    )


def country_dropdown():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    dcc.Dropdown(
                        id="country-dropdown",
                        options=[
                            {"label": i, "value": i} for i in df["country"].unique()
                        ],
                        value="United States",
                    )
                )
            ]
        )
    )


def key_metrics():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    id="key-metrics",
                    children=[
                        html.Div(
                            html.H4("How many Bic Mac can we buy?"),
                            style={"textAlign": "center"},
                        ),
                        # html.Div(id="big-mac-index-metric"),
                        # html.Div(id="local-currency-metric"),
                        # Buying Power Calculator (Will be updated with callback)
                        dcc.Graph(id="buying-power-plot"),
                    ],
                )
            ]
        )
    )


def global_map():
    return dbc.Card(dbc.CardBody([dcc.Graph(id="global-map", figure=fig_map)]))


def time_series_plot():
    return dbc.Card(
        dbc.CardBody(
            [
                # Inflation Adjustment Toggle and Currency Conversion Option
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("Inflation Adjustment for Hourly Wage: ")),
                    ]),

                dbc.Row(
                    [
                        dbc.Col(
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
                                inputStyle={"margin-right": "10px"}
                            ),
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("Curreny: ")),
                    ]),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.RadioItems(
                                id="currency-conversion-option",
                                options=[
                                    {
                                        "label": "Local Currency",
                                        "value": "local",
                                    },
                                    {
                                        "label": "USD", 
                                        "value": "USD"
                                    },
                                ],
                                value="USD",
                                # inline=True,
                                inputStyle={"margin-right": "10px"}
                            )
                        ),
                    ]
                ),
                dcc.Graph(
                    id="time-series-plot",
                    # style={"display": "inline-block"},
                ),
            ]
        )
    )


def minimum_wage_trend_plot():
    return dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(
                    id="minimum-wage-trend",
                    # style={
                    #     "display": "inline-block",
                    #     "marginLeft": "4%",
                    # }
                )
            ]
        )
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
                                                                "Big Mac Index Dashboard"
                                                            ),
                                                        ],
                                                        style={"textAlign": "center"},
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
                            dbc.Col(year_slider(), width=8),
                            dbc.Col(country_dropdown(), width=4),
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
                ]
            ),
            # color="dark",
        )
    ]
)


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

    if inflation == "adjust":
        wage = "adjusted_hourly_wage"
    else:
        wage = "hourly_wage_usd"

    if currency == "local":
        y_data = "local_price"
    else:
        y_data = "dollar_price"

    fig = px.line(
        filtered_data,
        x="year",
        y=[y_data, wage],
        title=f"Big Mac Price and Minimum Wage Trends in {selected_country}",
    )

    return fig


@app.callback(
    Output("buying-power-plot", "figure"), [Input("country-dropdown", "value")]
)
def update_buying_power_plot(selected_country):
    filtered_data = df[df["country"] == selected_country]

    if filtered_data.empty:
        return go.Figure()

    # line plot for buying power over time
    fig = px.line(
        filtered_data,
        x="year",
        y="bigmacs_per_hour",
        title=f"Buying Power Over Time in {selected_country}",
        # width=400, height=340
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
    ]

    if filtered_data.empty:
        return go.Figure()

    fig = go.Figure()

    # Add a bar for each country
    for country in filtered_data["country"].unique():
        fig.add_trace(
            go.Bar(
                x=[country],
                y=filtered_data[filtered_data["country"] == country]["hourly_wage_usd"],
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
