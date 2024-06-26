# Big Mac Dashboard

Welcome to the Big Mac Index Dashboard! Our interactive platform unveils the intricacies of purchasing power and economic trends globally via the famed Big Mac Index and comprehensive minimum wage data.

<div style="text-align: center; width: 100%;">
    <img src="img/burger.jpg" style="width: 100%;">
</div>

## Table of Contents

- [About](#about)
- [Use the App](#use-the-app)
- [About the Data](#about-the-data)
- [Dashboard Features](#dashboard-features)
- [How to Contribute](#how-to-contribute)
- [Running the Dashboard Locally](#running-the-dashboard-locally)
- [Team](#team)

## About

**The Big Mac Dashboard** is our response to the challenge of making economic data relatable and understandable. By merging the Big Mac Index with minimum wage information, we offer a practical perspective on economic indicators that affect everyday life. Whether you're an economist, policymaker, financial analyst, or a curious learner, our dashboard translates complex data into digestible visual stories.

<div style="display: flex; justify-content: center; width: 100%;">
    <img src="img/demo.gif" style="width: 100%;">
</div>

## Use the App

Dive into the dashboard experience right here. You'll find intuitive controls and visuals that bring economic data to life. Witness the buying power of an hour's wage around the world and explore how it's changed over time. [here!](https://dsci-532-2024-12-bigmac.onrender.com/) 
Need assistance or want to report an issue? Please open an issue on our GitHub repository, and we'll be happy to help.

## About the Data

The dashboard utilizes a dataset that combines historical prices of the Big Mac in over 50 countries with their respective minimum wage data from 2000 to 2022. This includes:

- **Big Mac Prices:** Annual prices in local currencies.
- **Minimum Wage:** Minimum hourly wage in local currencies.
- **Inflation Rates:** To adjust prices to current values.
- **Currency Exchange Rates:** For USD conversion.

With approximately 1,946 entries, the dataset covers various indicators such as country, year, Big Mac price (local currency and USD), local minimum wage, and inflation rate.

## Dashboard Features

**Features include:**

- **Global Map** to show the big mac per hour in different countries. I used color density to indicate the levels of big mac per hour by countries so that ppl can have a clear understanding of global economic purchasing power comparison at a glance.
- **Time Series** Plots of Big Mac per hour in selected country over selected years to show the change in purchasing power of a specific country.
- **Time series plot** of big mac price and minimum wage trend of select country over selected year.
- **Bar Chart of Medium** hourly wage in USD across countries in selected time period to compare the wage level across countries.

We've crafted this tool using Dash to offer a user-friendly and visually compelling way to navigate economic data.

## How to Contribute

Your insights and expertise can help make the Big Mac Index Dashboard even better. For guidelines on contributions, please refer to our [Contributing Guidelines](https://github.com/UBC-MDS/DSCI-532_2024_12_bigmac/blob/main/CONTRIBUTING.md) and uphold our [Code of Conduct](https://github.com/UBC-MDS/DSCI-532_2024_12_bigmac/blob/main/CODE_OF_CONDUCT.md). Whether you're looking to update data, enhance features, or fix bugs, we welcome your involvement!

## Running the Dashboard Locally

To run the dashboard locally, clone the repository, navigate to the project directory, and execute:
```bash
conda env create -f environment.yml
```
```bash
conda activate bigmac_12 
```
The above two commands install and activate the necessary environment to run the dashboard locally. After activation, run the following command under the same project directory:
```bash
python -m src.app
```
Use the output URL to view the dashboard. The URL has a format like this: http://127.0.0.1:8050/

## Team

- [Arturo Boquin](https://github.com/arturoboquin)
- [Atabak Alishiri](https://github.com/atabak-alishiri)
- [Beth Ou Yang](https://github.com/beth-ouyang)
- [Nicole Tu](https://github.com/Nicole-Tu97)

