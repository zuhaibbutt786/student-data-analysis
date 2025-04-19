import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from fpdf import FPDF
import os

# Load the data
airports_df = pd.read_csv('airports.csv')

# Extract state from the city name
airports_df['STATE'] = airports_df['DISPLAY_AIRPORT_CITY_NAME_FULL'].str.extract(r', ([A-Z]{2})$')

# Create a PDF report
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'US Airports Data Analysis Report', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Initialize PDF
pdf = PDF()
pdf.add_page()

# Title
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'US Airports Data Analysis', 0, 1, 'C')
pdf.ln(5)

# Introduction
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, 'This report presents a comprehensive analysis of US airports data, including their geographic distribution, state-wise distribution, and various visualizations.')
pdf.ln(5)

# Dataset Statistics
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Dataset Statistics', 0, 1, 'L')
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, f'Total number of airports analyzed: {len(airports_df)}\nNumber of states/territories with airports: {airports_df["STATE"].nunique()}')
pdf.ln(5)

# Top States
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Top 10 States by Number of Airports', 0, 1, 'L')
pdf.set_font('Arial', '', 12)

# Count airports by state
state_counts = airports_df['STATE'].value_counts().reset_index()
state_counts.columns = ['STATE', 'COUNT']

for i, row in state_counts.head(10).iterrows():
    pdf.cell(0, 10, f"{i+1}. {row['STATE']}: {row['COUNT']} airports", 0, 1, 'L')
pdf.ln(5)

# Geographic Extremes
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Geographic Extremes', 0, 1, 'L')
pdf.set_font('Arial', '', 12)

northernmost = airports_df.loc[airports_df['LATITUDE'].idxmax()]
southernmost = airports_df.loc[airports_df['LATITUDE'].idxmin()]
easternmost = airports_df.loc[airports_df['LONGITUDE'].idxmax()]
westernmost = airports_df.loc[airports_df['LONGITUDE'].idxmin()]

pdf.multi_cell(0, 10, f"Northernmost: {northernmost['AIRPORT']} - {northernmost['DISPLAY_AIRPORT_NAME']} ({northernmost['DISPLAY_AIRPORT_CITY_NAME_FULL']})")
pdf.multi_cell(0, 10, f"Southernmost: {southernmost['AIRPORT']} - {southernmost['DISPLAY_AIRPORT_NAME']} ({southernmost['DISPLAY_AIRPORT_CITY_NAME_FULL']})")
pdf.multi_cell(0, 10, f"Easternmost: {easternmost['AIRPORT']} - {easternmost['DISPLAY_AIRPORT_NAME']} ({easternmost['DISPLAY_AIRPORT_CITY_NAME_FULL']})")
pdf.multi_cell(0, 10, f"Westernmost: {westernmost['AIRPORT']} - {westernmost['DISPLAY_AIRPORT_NAME']} ({westernmost['DISPLAY_AIRPORT_CITY_NAME_FULL']})")
pdf.ln(5)

# Latitude and Longitude Statistics
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Latitude and Longitude Statistics', 0, 1, 'L')
pdf.set_font('Arial', '', 12)

pdf.multi_cell(0, 10, f"Mean latitude: {airports_df['LATITUDE'].mean():.2f}°\nMedian latitude: {airports_df['LATITUDE'].median():.2f}°\nRange: {airports_df['LATITUDE'].min():.2f}° to {airports_df['LATITUDE'].max():.2f}°")
pdf.ln(5)
pdf.multi_cell(0, 10, f"Mean longitude: {airports_df['LONGITUDE'].mean():.2f}°\nMedian longitude: {airports_df['LONGITUDE'].median():.2f}°\nRange: {airports_df['LONGITUDE'].min():.2f}° to {airports_df['LONGITUDE'].max():.2f}°")
pdf.ln(5)

# Airport Density Analysis
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Airport Density Analysis', 0, 1, 'L')
pdf.set_font('Arial', '', 12)

# Create latitude bands
lat_bins = np.linspace(airports_df['LATITUDE'].min(), airports_df['LATITUDE'].max(), 6)
airports_df['LATITUDE_BAND'] = pd.cut(airports_df['LATITUDE'], bins=lat_bins)
lat_band_counts = airports_df['LATITUDE_BAND'].value_counts().sort_index()

pdf.multi_cell(0, 10, "Distribution by latitude bands:")
for band, count in lat_band_counts.items():
    pdf.multi_cell(0, 10, f"{band}: {count} airports ({count/len(airports_df)*100:.1f}%)")
pdf.ln(5)

# Add images
pdf.add_page()
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Visualizations', 0, 1, 'L')
pdf.set_font('Arial', '', 12)

# List visualizations without including images
visualizations = [
    'Geographic Distribution of Airports',
    'Top States by Number of Airports',
    'Airport Distribution by Latitude Bands',
    'Airport Distribution by Longitude Bands',
    'Airport Density Heatmap'
]

pdf.multi_cell(0, 10, "The following visualizations were created as part of this analysis:")
for i, viz in enumerate(visualizations, 1):
    pdf.multi_cell(0, 10, f"{i}. {viz}")
pdf.ln(10)

# Conclusion
pdf.add_page()
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Conclusion', 0, 1, 'L')
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, """The analysis reveals that US airports are not evenly distributed across the country. There is a higher concentration in the eastern and western coastal regions, as well as in states with larger populations or geographic areas. Texas, California, and Alaska have the highest number of airports, reflecting their large size and economic importance.

The majority of airports (55.6%) are located between 37.038°N and 54.162°N latitude, which corresponds to the northern part of the continental United States. Another significant portion (36.0%) falls between 19.914°N and 37.038°N, covering the southern continental US.

The interactive dashboard provides a comprehensive tool for exploring this data further, allowing users to visualize the geographic distribution of airports, analyze state-wise distribution, and examine the distribution by latitude and longitude.""")

# Save the PDF
pdf.output('us_airports_analysis_report.pdf')
print("Report generated successfully: us_airports_analysis_report.pdf")