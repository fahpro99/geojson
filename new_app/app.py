import streamlit as st
import folium
from streamlit_folium import folium_static  # Add this import
import pandas as pd
import requests

# Load GeoJSON data
state_geo = requests.get(
    "https://raw.githubusercontent.com/fahpro99/geojson/main/output.json"
).json()

# Load data
state_data = pd.read_csv(
    "https://raw.githubusercontent.com/fahpro99/geojson/main/my_country.csv"
)

# Streamlit app title
st.title("Network outages in Bangladesh")

# Create a Folium map centered on Bangladesh
m = folium.Map(location=[23.6850, 90.3563], zoom_start=7)

# Create choropleth map
choropleth = folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=state_data,
    columns=["District", "Count"],
    key_on="feature.properties.NAME_1",
    fill_color="Spectral",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Count",
    highlight=True
)
choropleth.geojson.add_to(m)

# Add labels for each district with district names and counts
for _, row in state_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],  # Replace with your actual location columns
        icon=None,
        popup=f"{row['District']} - Count: {row['Count']}",
        tooltip=f"{row['District']} - Count: {row['Count']}",
    ).add_to(m)

# Add layer control to the map
folium.LayerControl().add_to(m)

# Streamlit map display
folium_static(m)  # Use folium_static to embed the Folium map in Streamlit
