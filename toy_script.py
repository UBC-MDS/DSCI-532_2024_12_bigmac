import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

bigmac_data = pd.read_csv("data/raw/bigmac_price.csv")
wage_data = pd.read_csv("data/raw/wage.csv")

# Data Wrangling

bigmac_data['year'] = pd.to_datetime(bigmac_data['date']).dt.year

# Using only the hourly wage data
wage_data = wage_data[(wage_data['Pay period'] == 'Hourly') & (wage_data['Series'] == 'In 2022 constant prices at 2022 USD PPPs')]

bigmac_prepared = bigmac_data[['name', 'year', 'local_price', 'dollar_price']].copy()
bigmac_prepared.rename(columns={'name': 'country'}, inplace=True)

wage_prepared = wage_data[['Country', 'Time', 'Value']].copy()
wage_prepared.rename(columns={'Country': 'country', 'Time': 'year', 'Value':'hourly_wage_usd'}, inplace=True)

# Ensure 'year' is integer for both datasets
bigmac_prepared['year'] = bigmac_prepared['year'].astype(int)
wage_prepared['year'] = wage_prepared['year'].astype(int)

# Merge datasets on 'country' and 'year'
merged_data = pd.merge(bigmac_prepared, wage_prepared, on=['country', 'year'], how='inner')

# Calculate 'Big Macs per hour'
merged_data['bigmacs_per_hour'] = merged_data['hourly_wage_usd'] / merged_data['dollar_price']

# Calculate Inflation
bigmac_prepared.sort_values(by=['country', 'year'], inplace=True)

# Calculate the year-over-year percentage change in local_price for each country
bigmac_prepared['inflation'] = bigmac_prepared.groupby('country')['local_price'].pct_change() * 100

# Merge
merged_data = pd.merge(merged_data, bigmac_prepared[['country', 'year', 'inflation']], on=['country', 'year'], how='left')

# Saving the final dataset
merged_data.to_csv('data/processed/merged_data_with_inflation.csv', index=False)


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the figure for the global map view

fig_map = px.choropleth(merged_data,
                        locations="country",
                        locationmode="country names",
                        color="bigmacs_per_hour",
                        hover_name="country",
                        hover_data={"year": True, "bigmacs_per_hour": True, "dollar_price": True},
                        projection="natural earth",
                        title="Global Big Macs per Hour",
                        color_continuous_scale=px.colors.sequential.Plasma)

fig_map.update_geos(
    showcountries=True, countrycolor="RebeccaPurple"
)

fig_map.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    coloraxis_colorbar={
        'title':'Big Macs/hr'
    }
)


app.layout = html.Div(children=[
    html.Div(
        html.H1('Big Mac Index Dashboard'),
        style={'textAlign': 'center', 'marginTop': 50, 'marginBottom': 50}
    ),
    
    # Filters for Country and Year
    html.Div([
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': i, 'value': i} for i in merged_data['country'].unique()],
        value='United States',
        style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([  # Wrapping the slider within an html.Div for styling
        dcc.Slider(
            id='year-slider',
            min=merged_data['year'].min(),
            max=merged_data['year'].max(),
            value=merged_data['year'].max(),
            marks={str(year): str(year) for year in merged_data['year'].unique()},
            step=None,
        )
    ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'}),  # Style is applied here
], style={'marginTop': 20, 'marginBottom': 20}),


    # Global Map View and Key Metrics
    html.Div([
        dcc.Graph(id='global-map', figure=fig_map, style={'width': '65%', 'display': 'inline-block'}),
        html.Div(id='key-metrics', children=[
            # Big Mac Index and other key metrics will be added here
            html.H3('Key Metrics'),
            html.Div(id='big-mac-index-metric'),
            html.Div(id='local-currency-metric'),
            # Inflation Adjustment Toggle and Currency Conversion Option
            dcc.Checklist(
                id='inflation-adjustment-toggle',
                options=[{'label': 'Adjust for Inflation', 'value': 'adjust'}],
                value=[]
            ),
            dcc.RadioItems(
                id='currency-conversion-option',
                options=[{'label': 'Local Currency', 'value': 'local'}, {'label': 'USD', 'value': 'USD'}],
                value='USD'
            ),
            # Buying Power Calculator (Will be updated with callback)
            dcc.Graph(id='buying-power-plot'),
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'bottom', 'marginLeft': '5%'})
    ]),

    # Time Series Plots for Big Mac Price Trend and Minimum Wage Trend
    html.Div([
        dcc.Graph(id='time-series-plot', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='minimum-wage-trend', style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
    ])
])

# Callback to update the time series plot
@app.callback(
    Output('time-series-plot', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('inflation-adjustment-toggle', 'value'),
     Input('currency-conversion-option', 'value')]
)
def update_time_series(selected_country, selected_year, inflation_adjusted, currency):
    filtered_data = merged_data[(merged_data['country'] == selected_country) &
                                (merged_data['year'] <= selected_year)]
    
    if inflation_adjusted:
        pass 
    if currency == 'local':
        y_data = 'local_price'
    else:
        y_data = 'dollar_price'
    
    fig = px.line(filtered_data, x='year', y=[y_data, 'hourly_wage_usd'],
                  title=f'Big Mac Price and Minimum Wage Trends in {selected_country}')
    
    return fig


@app.callback(
    Output('buying-power-plot', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_buying_power_plot(selected_country):
    filtered_data = merged_data[merged_data['country'] == selected_country]

    if filtered_data.empty:
        return go.Figure()

    # line plot for buying power over time
    fig = px.line(filtered_data, x='year', y='bigmacs_per_hour',
                  title=f'Buying Power Over Time in {selected_country}')

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Big Macs per Hour',
        margin={'l': 40, 'b': 40, 't': 40, 'r': 0},
        hovermode='closest'
    )

    fig.update_traces(line=dict(color='RoyalBlue'))

    return fig


@app.callback(
    Output('minimum-wage-trend', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')] 
)
def update_minimum_wage_trend(selected_country, selected_year):
    filtered_data = merged_data[merged_data['year'] == selected_year]

    if filtered_data.empty:
        return go.Figure()

    fig = go.Figure()

    # Add a bar for each country
    for country in filtered_data['country'].unique():
        fig.add_trace(go.Bar(
            x=[country],
            y=filtered_data[filtered_data['country'] == country]['hourly_wage_usd'],
            name=country,
            marker_color='lightslategray' if country != selected_country else 'crimson'  # Highlight selected country
        ))

    # Update the layout
    fig.update_layout(
        title=f'Hourly Wage (USD) in {selected_year}',
        xaxis_title='Country',
        yaxis_title='Hourly Wage (USD)',
        xaxis={'categoryorder': 'total descending'},
        margin={'l': 40, 'b': 40, 't': 40, 'r': 0},
        hovermode='closest'
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')