# US Airports Data Analysis

This repository contains a comprehensive analysis of US airports data, including their geographic distribution, state-wise distribution, and various visualizations.

## Dataset

The dataset (`airports.csv`) contains information about 322 airports in the United States and its territories, including:
- Airport code
- Airport name
- City and state
- Geographic coordinates (latitude and longitude)

## Analysis Performed

1. **Geographic Distribution**: Visualized the spatial distribution of airports across the US
2. **State-wise Analysis**: Identified states with the highest number of airports
3. **Latitude and Longitude Distribution**: Analyzed how airports are distributed across different latitude and longitude bands
4. **Extreme Locations**: Identified the northernmost, southernmost, easternmost, and westernmost airports
5. **Density Analysis**: Created a heatmap showing the density of airports across different regions

## Key Findings

- Texas has the highest number of airports (24), followed by California (22) and Alaska (19)
- Most airports are concentrated in the latitude band between 30N and 45N
- The northernmost airport is Wiley Post/Will Rogers Memorial in Barrow, Alaska
- The southernmost airport is Pago Pago International in American Samoa
- The easternmost airport is Agana Field in Guam
- The westernmost airport is Adak NS in Adak Island, Alaska

## Visualizations

The analysis includes several visualizations:
- Geographic scatter plot of all airports
- Interactive map with airport details
- Bar charts showing the distribution of airports by state
- Histograms showing the distribution by latitude and longitude
- Heatmap showing airport density

## Interactive Dashboard

An interactive dashboard has been created using Dash and Plotly to explore the data. To run the dashboard:

```bash
python app.py
```

The dashboard will be available at http://localhost:12000 and includes:
- Interactive map of all airports
- Bar chart of top states by number of airports
- Histograms showing latitude and longitude distributions
- Detailed information about selected airports

## Files in this Repository

- `airports.csv`: The dataset containing airport information
- `app.py`: Dash application for interactive visualization
- `geographic_distribution.png`: Scatter plot showing the geographic distribution of airports
- `top_states.png`: Bar chart showing states with the most airports
- `latitude_distribution.png`: Distribution of airports by latitude bands
- `longitude_distribution.png`: Distribution of airports by longitude bands
- `airport_heatmap.png`: Heatmap showing the density of airports
- `airport_map.html`: Interactive map of all airports

## Requirements

- Python 3.x
- pandas
- matplotlib
- seaborn
- folium
- dash
- plotly

## Installation

```bash
pip install pandas matplotlib seaborn folium dash plotly
```
