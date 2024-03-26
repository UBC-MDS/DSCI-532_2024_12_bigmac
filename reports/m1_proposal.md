# Project Proposal: Big Mac Index Dashboard

## 1. Motivation and Purpose

**Our Role:** Data Scientists in an Economic Research Institute

**Target Audience:** Economists, Policy Makers, Financial Analysts, and the General Public interested in Global Economic Trends

The Big Mac Index, introduced by The Economist as an informal way of measuring the purchasing power parity (PPP) between two currencies, provides a unique lens through which to view economic health, inflation, and buying power across the globe. Despite its simplicity, this index, when combined with minimum wage data, can offer profound insights into economic conditions, trends in inflation, and shifts in global buying power. Our proposed dashboard aims to serve a broad audience by simplifying complex economic concepts into visual, interactive, and comparative insights using a universally recognized product: the Big Mac.

The challenge many face is accessing, comparing, and understanding how the relative value of currency and economic health changes over time across different nations. By correlating the price of a Big Mac with the minimum wage in each country, we intend to provide a clearer picture of the real-world buying power and economic resilience or vulnerability. This is crucial for economists, policy makers, and analysts designing economic policies or investments and for the educated public interested in understanding economic strength and stability.

To bridge this gap, we propose the development of an interactive dashboard that visualizes the evolution of the Big Mac Index and minimum wage across various countries, adjusted for inflation and converted into USD for global comparability. This tool will not only facilitate a deeper understanding of economic indicators but also promote global economic literacy by providing an accessible platform for exploration and analysis.

## 2. Description of the Data

Our dataset combines historical prices of the Big Mac from various countries with their respective minimum wage data from 2000 to 2022. This dataset features:

- **Big Mac Prices:** The local currency price of a Big Mac in over 50 countries, collected annually.
- **Minimum Wage:** The minimum hourly wage in local currency for the corresponding countries and years.
- **Inflation Rates:** Annual inflation rates, which will allow for the adjustment of historical prices to current values for accurate comparison.
- **Currency Exchange Rates:** Historical annual exchange rates to USD, enabling price conversion for comparative analysis.

The dataset comprises approximately 1,946 rows (22 years of data for 50+ countries) and includes variables such as country, year, Big Mac price in local currency and USD, local minimum wage, and inflation rate.

We plan to derive additional variables such as the "Big Macs per hour" metric, which indicates how many Big Macs an hour of minimum wage work can buy in each country. This will provide a direct measure of buying power over time.

## 3. Research Questions and Usage Scenarios

**Example User Story: Maria, a Financial Analyst**

Maria is a financial analyst specializing in emerging markets. She's interested in understanding how real wages have evolved in response to inflation and economic policies. Maria uses our dashboard to compare the buying power of minimum wage earners in Brazil, India, and South Africa over the last decade. She filters data by country and selects variables to visualize, including Big Mac prices in USD and local currency, adjusted for inflation.

Through interactive visualizations, Maria observes trends and anomalies, such as the significant increase in buying power in India contrasted with stagnation in South Africa. She drills down into specific years to understand the impact of economic policies or global economic events. The insights gained from the dashboard enable Maria to draft a comprehensive report on emerging market economies, supported by visual data, to advise her clients on investment strategies.

## 4. App Sketch and Description

*Dashboard Sketch*

Our dashboard is designed for simplicity and interactivity, allowing users to engage with the data through:

- **Global Map View:** A world map highlighting countries with available data. Users can hover over countries to see a summary of the latest Big Mac Index and minimum wage data.
- **Time Series Plots:** Interactive line graphs showing the price of Big Macs over time in local currency and USD, alongside minimum wage trends. Users can select specific countries for a comparative view.
- **Buying Power Calculator:** A feature allowing users to calculate and visualize the number of Big Macs that can be purchased with an hour of minimum wage work in selected countries and years.
- **Inflation Adjustment Toggle:** A tool to adjust historical prices for inflation, providing a real-value comparison over time.
- **Currency Conversion Option:** Allows users to view prices in local currency or USD, facilitating global comparisons.

The dashboard will be developed using Dash and deployed for public access. It aims to transform complex economic data into accessible, engaging visual stories, enhancing global economic understanding.
