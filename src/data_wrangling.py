import pandas as pd

def main():
    bigmac_data = pd.read_csv("data/raw/bigmac_price.csv")
    wage_data = pd.read_csv("data/raw/wage.csv")

    # Data Wrangling

    bigmac_data["year"] = pd.to_datetime(bigmac_data["date"]).dt.year

    # Using only the hourly wage data
    wage_data = wage_data[
        (wage_data["Pay period"] == "Hourly")
        & (wage_data["Series"] == "In 2022 constant prices at 2022 USD PPPs")
    ]

    bigmac_prepared = bigmac_data[["name", "year", "local_price", "dollar_price"]].copy()
    bigmac_prepared.rename(columns={"name": "country"}, inplace=True)

    wage_prepared = wage_data[["Country", "Time", "Value"]].copy()
    wage_prepared.rename(
        columns={"Country": "country", "Time": "year", "Value": "hourly_wage_usd"},
        inplace=True,
    )

    # Ensure 'year' is integer for both datasets
    bigmac_prepared["year"] = bigmac_prepared["year"].astype(int)
    wage_prepared["year"] = wage_prepared["year"].astype(int)

    # Merge datasets on 'country' and 'year'
    merged_data = pd.merge(
        bigmac_prepared, wage_prepared, on=["country", "year"], how="inner"
    )

    # Calculate 'Big Macs per hour'
    merged_data["bigmacs_per_hour"] = (
        merged_data["hourly_wage_usd"] / merged_data["dollar_price"]
    )

    # Calculate Inflation
    bigmac_prepared.sort_values(by=["country", "year"], inplace=True)

    # Calculate the year-over-year percentage change in local_price for each country
    bigmac_prepared["inflation"] = (
        bigmac_prepared.groupby("country")["local_price"].pct_change() * 100
    )

    # Calculate the adjusted local_price based on the first year in record (2001)
    bigmac_prepared["multiplication_factor"] = bigmac_prepared.groupby("country")["local_price"].pct_change().fillna(0) + 1
    bigmac_prepared['cum_prod'] = bigmac_prepared.groupby('country')['multiplication_factor'].cumprod()

    # Merge
    merged_data = pd.merge(
        merged_data,
        bigmac_prepared[["country", "year", "cum_prod"]],
        on=["country", "year"],
        how="left",
    )
    merged_data['adjusted_hourly_wage'] = merged_data['hourly_wage_usd'] / merged_data['cum_prod']


    # Saving the final dataset
    merged_data.to_csv("data/processed/merged_data_with_inflation.csv", index=False)

    return merged_data