import streamlit as st
import folium
from streamlit_folium import folium_static
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

# Define a function to set the style for each feature (district) on the map
def style_function(feature):
    district_name = feature['properties']['NAME_1']
    count = state_data[state_data['District'] == district_name]['Count'].values[0]

    # Set the color based on the count
    if count > 100:
        color = '#d73027'  # Red
    elif count > 50:
        color = '#4575b4'  # Blue
    else:
        color = '#91bfdb'  # Light blue

    return {
        'fillColor': color,
        'color': color,
        'weight': 2,
        'fillOpacity': 0.7
    }

# Add GeoJSON layer with the defined style
folium.GeoJson(
    state_geo,
    style_function=style_function,
    name="choropleth"
).add_to(m)

# Add markers for each district with district names and counts
for _, row in state_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        icon=folium.DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 10pt; font-weight: bold; color: white">{row["District"]}<br>{row["Count"]}</div>'
        )
    ).add_to(m)

# Add layer control to the map
folium.LayerControl().add_to(m)

# Streamlit map display
folium_static(m)  # Use folium_static to embed the Folium map in Streamlit
