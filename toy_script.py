import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime

bigmac_data = pd.read_csv("data/raw/bigmac_price.csv")
wage_data = pd.read_csv("data/raw/wage.csv")

# Data Wrangling

bigmac_data['year'] = pd.to_datetime(bigmac_data['date']).dt.year

# Convert annual wage to hourly assuming 40-hour work week and 52 weeks per year
wage_data['hourly_wage_usd'] = wage_data['Value'] / (40 * 52)

bigmac_prepared = bigmac_data[['name', 'year', 'local_price', 'dollar_price']].copy()
bigmac_prepared.rename(columns={'name': 'country'}, inplace=True)

wage_prepared = wage_data[['Country', 'Time', 'hourly_wage_usd']].copy()
wage_prepared.rename(columns={'Country': 'country', 'Time': 'year'}, inplace=True)

# Ensure 'year' is integer for both datasets
bigmac_prepared['year'] = bigmac_prepared['year'].astype(int)
wage_prepared['year'] = wage_prepared['year'].astype(int)

# Merge datasets on 'country' and 'year'
merged_data = pd.merge(bigmac_prepared, wage_prepared, on=['country', 'year'], how='inner')

# Calculate 'Big Macs per hour'
merged_data['bigmacs_per_hour'] = merged_data['hourly_wage_usd'] / merged_data['dollar_price']

merged_data.head()


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


# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Big Mac Index Dashboard'),
    
    dcc.Graph(id='global-map', figure=fig_map),
    
    html.Div([
        html.Label('Select Country:'),
        dcc.Dropdown(id='country-dropdown',
                     options=[{'label': i, 'value': i} for i in merged_data['country'].unique()],
                     value='United States'),
        
        dcc.Graph(id='time-series-plot'),
        
        html.Label('Select Year:'),
        dcc.Slider(id='year-slider',
                   min=merged_data['year'].min(),
                   max=merged_data['year'].max(),
                   value=merged_data['year'].max(),
                   marks={str(year): str(year) for year in merged_data['year'].unique()},
                   step=None),
        
        html.Div(id='buying-power-calculator'),
        
        dcc.Checklist(id='inflation-adjustment-toggle',
                      options=[{'label': 'Adjust for Inflation', 'value': 'adjust'}],
                      value=[]),
        
        dcc.RadioItems(id='currency-conversion-option',
                       options=[{'label': 'Local Currency', 'value': 'local'},
                                {'label': 'USD', 'value': 'USD'}],
                       value='USD')
    ]),
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
    # Placeholder logic for filtering and adjusting data
    filtered_data = merged_data[(merged_data['country'] == selected_country) &
                                (merged_data['year'] <= selected_year)]
    
    # Placeholder for actual inflation adjustment and currency conversion
    if inflation_adjusted:
        pass  # Apply inflation adjustment
    if currency == 'local':
        y_data = 'local_price'
    else:
        y_data = 'dollar_price'
    
    fig = px.line(filtered_data, x='year', y=[y_data, 'hourly_wage_usd'],
                  title=f'Big Mac Price and Minimum Wage Trends in {selected_country}')
    
    # Update plot aesthetics
    
    return fig

# Callback to update the buying power calculator
@app.callback(
    Output('buying-power-calculator', 'children'),
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_buying_power(selected_country, selected_year):
    # Placeholder logic to calculate the buying power
    buying_power = merged_data[(merged_data['country'] == selected_country) &
                               (merged_data['year'] == selected_year)]['bigmacs_per_hour'].values[0]
    
    return f'Buying Power: {buying_power:.2f} Big Macs per hour of work'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')