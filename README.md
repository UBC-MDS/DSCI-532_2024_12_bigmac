# Big Mac Dashboard

## Table of Contents

- [About](#about)
- [Use the App](#use-the-app)
- [About the Data](#about-the-data)
- [Dashboard Features](#dashboard-features)
- [How to Contribute](#how-to-contribute)
- [Running the Dashboard Locally](#running-the-dashboard-locally)
- [Team](#team)

## About

**The Big Mac Dashboard** provides interactive visual insights into the purchasing power parity (PPP) and economic trends across the globe using the Big Mac Index and minimum wage data. Aimed at economists, policy makers, financial analysts, and the general public, the dashboard simplifies the understanding of complex economic indicators through engaging and comparative visualizations.

![sketch dashboard](https://github.com/UBC-MDS/DSCI-532_2024_12_bigmac/blob/main/img/sketch.jpg)

## Use the App

Access the live dashboard [here!](https://dsci-532-2024-12-bigmac.onrender.com/) 

## About the Data

The dashboard utilizes a dataset that combines historical prices of the Big Mac in over 50 countries with their respective minimum wage data from 2000 to 2022. This includes:

- **Big Mac Prices:** Annual prices in local currencies.
- **Minimum Wage:** Minimum hourly wage in local currencies.
- **Inflation Rates:** To adjust prices to current values.
- **Currency Exchange Rates:** For USD conversion.

With approximately 1,946 entries, the dataset covers various indicators such as country, year, Big Mac price (local currency and USD), local minimum wage, and inflation rate.

## Dashboard Features

**Features include:**

- **Global Map View:** Highlights countries with data, showing the latest Big Mac Index and minimum wage summaries.
- **Time Series Plots:** Displays Big Mac prices and minimum wage trends in both local currency and USD.
- **Buying Power Calculator:** Calculates how many Big Macs an hour of minimum wage can buy in selected countries.
- **Inflation Adjustment Toggle:** Adjusts historical prices for inflation.
- **Currency Conversion Option:** Views prices in local currency or USD.

Developed using Dash, the dashboard aims to make economic data accessible and engaging.

## How to Contribute

Interested in enhancing the Big Mac Index Dashboard? See our [Contributing Guidelines](#). Contributions can range from data updates to feature development. All contributors must adhere to our [Code of Conduct](#).

## Running the Dashboard Locally

To run the dashboard locally, ensure you have Dash installed. Clone the repository, navigate to the project directory, and execute:

```bash
python toy_script.py
```

## Team
- Arturo Boquin
- Atabak Alishiri
- Beth Ou Yang
- Nicole Tu
